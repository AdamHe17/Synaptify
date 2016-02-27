import matlab.engine

eng = matlab.engine.start_matlab()
eng.cd(r'~/Documents/myStuff/HackTech2016/Synaptify')
outputs = eng.analysis('identify_2016-02-26_20-37-59_00.bmp',nargout=4)

ridges, bifurcations = [], []
for i in range(len(outputs[0])):
	ridges.append([outputs[0][i][0], outputs[1][i][0]])
for i in range(len(outputs[2])):
	bifurcations.append([outputs[2][i][0], outputs[3][i][0]])

print ridges
print bifurcations