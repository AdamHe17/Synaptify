# Synaptify

### Music from your fingertips

Synaptify performs analysis algorithms on fingerprint bitmaps to output a unique audio track, in MIDI format, based on the fingerprint's unique characteristics.

The algorithm starts with identifying what points make a fingerprint "unique" - that is, the location of ridge bifurcations and ridge terminations (i.e. where ridges on the finger split and where they end). The indices of the splits and ends are mapped to piano frequencies between C4 - C6. After this, the ratio of ridge ends to splits is determined to modulate the key the pitches are in. We use spread, or the average distance of unique points from one another, to determine the tempo of the piece. The number of ridges and splits determines what instrument we combine with a piano track. Note lengths are put into an array, and we mod in order select the duration for each note. This is how we determine rhythm. After all of this, a .mid file is created and played that gives a consistent, deterministic output for each fingerprint every time.
