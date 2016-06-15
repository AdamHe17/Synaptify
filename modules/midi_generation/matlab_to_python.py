from __future__ import division
import matlab.engine
import math
import numpy

def compute_spread(points):
    x_ave = 0
    y_ave = 0
    spread = 0.0
    for i in range(0, len(points)):
        x_ave += points[i][0]
        y_ave += points[i][1]
    x_ave /= len(points)
    y_ave /= len(points)
    for j in range(0, len(points)):
        spread += ((points[j][0] - x_ave) ** 2) + ((points[j][1] - y_ave) ** 2)
    spread /= len(points)
    spread = math.sqrt(spread)
    return spread

class Parsed_Image:
	def __init__(self, r, b, spr):
		self.ridges = r
		self.bifurcations = b
		self.spread = spr
		self.ratio = float(len(r)) / (len(r) + len(b))

def filter_list(lst):
    lst.sort()
    limit = 5
    res = [lst[0]]
    for i in range(len(lst)-1):
        m, n = lst[i], lst[i+1]
        if (abs(m[0]-n[0]) < limit and abs(m[1]-n[1]) < limit):
            pass
        else:
            res.append(n)
    return res

def process_image(path):
	eng = matlab.engine.start_matlab()

	outputs = eng.analysis(path, nargout=4)

	ridges, bifurcations = [], []
	for i in range(len(outputs[0])):
		ridges.append([outputs[0][i][0], outputs[1][i][0]])
	for i in range(len(outputs[2])):
		bifurcations.append([outputs[2][i][0], outputs[3][i][0]])

	ridges = filter_list(ridges)
	bifurcations = filter_list(bifurcations)

	if len(ridges) != 0 and len(bifurcations) != 0:
		minutiae = numpy.concatenate([ridges,bifurcations])
	elif len(ridges) != 0:
		minutiae = ridges
	elif len(bifurcations) != 0:
		minutiae = bifurcations

	data = Parsed_Image(ridges, bifurcations, compute_spread(minutiae))

	return data;