from __future__ import division
from operator import itemgetter
import matlab.engine
import math
import numpy
import matlab_to_python as mtp
from midi import *



def get_points_144(positions):
    new_indices = numpy.zeros(len(positions))
    for i in range (0, len(positions)):
        new_indices[i] = 144*positions[i][0]+positions[i][1]
    return new_indices

def map_to_piano(indices):
    my_freqs = numpy.zeros(len(indices), dtype = float)
    for i in range (0, len(indices)):
        my_freqs[i] = (indices[i]/4.95365504061)+27.5
    return my_freqs

def map_to_C_scale(my_freqs):
    notes_to_scale = numpy.zeros(len(my_freqs), dtype = float)
    my_freqs_in_C = numpy.zeros(len(my_freqs))
    C_scale = numpy.array([261.63,293.66,329.63,349.23,392,440,493.88,523.25,
                        587.33,659.25,698.46,783.99,880,987.77,1046.50])
    for i in range (0, len(my_freqs)):
        my_freqs_in_C[i] = float(my_freqs[i]/4.0)+261.63
    diff = 99999999999999999
    best_fit = -1
    for i in range (0, len(my_freqs_in_C)):
        for j in range (0, len(C_scale)):
            val = abs(my_freqs_in_C[i] - C_scale[j])
            if (val < diff):
                diff = val
                best_fit = j
        my_freqs_in_C[i] = C_scale[best_fit]
        diff = 999999999999999999999
        best_fit = -1

    return my_freqs_in_C

def change_scale(my_freqs, ratio):
    key_ratios = numpy.array([1./12., 2./12, 3./12., 4./12., 5./12., 6./12.,
                           7./12., 8./12.,9./12.,10./12.,11./12.,12./12.])
    diff = 99999999999999999
    n = -1
    for j in range (0, len(key_ratios)):
        val = abs(ratio - key_ratios[j])
        if (val < diff):
            diff = val
            n = j
    real_freqs = numpy.zeros(len(my_freqs), dtype = float)
    for i in range (0, len(my_freqs)):
        real_freqs[i] = float(2**float(n/12.))*my_freqs[i]
    return real_freqs

def freq2midi(freq):
  """
  Given a frequency in Hz, returns its MIDI pitch number.
  """
  result = int(numpy.round(12 * (numpy.log2(freq) - numpy.log2(440)) + 69))
  return nan if isinstance(result, complex) else result

def decide_tempo(spread):
    return 60 + (220/8) * (spread-27)

def set_note_length(point):
    note_lengths = [1./2, 1, 2, 4]
    return note_lengths[int(point[0] + point[1]) % 4]

def sort_by_x(my_arr):
    return sorted(my_arr, key=itemgetter(1))

def set_instrument(my_arr):
    instruments = [15, 43, 42, 17, 67, 74, 24, 80, 57, 16, 7, 11, 8, 70, 63, 20, 41, 28, 71, 68, 22, 58, 12, 73, 5, 9, 47, 110, 72, 27, 75, 10, 106, 4, 66, 23, 89, 53, 105, 79, 61, 81, 69, 65]
    return instruments[len(my_arr) % len(instruments)]

#MIDI file generator method
def make_MIDI(input_path, output_path):
    parsed_image = mtp.process_image(input_path)
    print parsed_image

    my_midi = MIDIFile(2)
    my_midi.addTempo(0, 0, decide_tempo(parsed_image.spread))
    my_midi.addTempo(1, 0, decide_tempo(parsed_image.spread))
    my_midi.addProgramChange(1, 1, 0, 1)
    my_midi.addProgramChange(0, 0, 0, set_instrument(parsed_image.bifurcations))

    parsed_image.ridges = sort_by_x(parsed_image.ridges)
    parsed_image.bifurcations = sort_by_x(parsed_image.bifurcations)

    time_run = 0
    ridge_indices = get_points_144(parsed_image.ridges)
    bifurcation_indices = get_points_144(parsed_image.bifurcations)

    ridge_freqs_raw = map_to_piano(ridge_indices)
    bifurcation_freqs_raw = map_to_piano(bifurcation_indices)

    ridge_freqs_C = map_to_C_scale(ridge_freqs_raw)
    bifurcation_freqs_C = map_to_C_scale(bifurcation_freqs_raw)

    ridge_freqs_final = change_scale(ridge_freqs_C, parsed_image.ratio)
    bifurcation_freqs_final = change_scale(bifurcation_freqs_C, parsed_image.ratio)


    for i in range(0, len(ridge_freqs_final)):
        my_midi.addNote(0, 1, freq2midi(ridge_freqs_final[i]), time_run, set_note_length(parsed_image.ridges[i]), 64)
        time_run += set_note_length(parsed_image.ridges[i])

    time_run = 0

    for j in range(0, len(bifurcation_freqs_final)):
        my_midi.addNote(1, 1, freq2midi(bifurcation_freqs_final[j]), time_run, set_note_length(parsed_image.bifurcations[j]), 64)
        time_run += set_note_length(parsed_image.bifurcations[j])

    open_file = open(output_path, 'w')

    my_midi.writeFile(open_file);

    open_file.close()