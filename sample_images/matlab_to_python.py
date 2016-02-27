import matlab.engine

eng = matlab.engine.start_matlab()
eng.cd(r'C:\Users\ah299_000\Documents\GitHub\Synaptify')
outputs = eng.analysis('identify_2016-02-26_20-37-59_00.bmp',nargout=4)
for i in range(4):
	print outputs[i]