from PIL import Image

#Thinning code

def neighbours(x, y, image):
    '''Return 8-neighbours of point p1 of picture, in order'''
    i = image
    x1, y1, x_1, y_1 = x+1, y-1, x-1, y+1
    #print ((x,y))
    return [i[y1][x],  i[y1][x1],   i[y][x1],  i[y_1][x1],  # P2,P3,P4,P5
            i[y_1][x], i[y_1][x_1], i[y][x_1], i[y1][x_1]]  # P6,P7,P8,P9
 
def transitions(neighbours):
    n = neighbours + neighbours[0:1]    # P2, ... P9, P2
    return sum((n1, n2) == (0, 1) for n1, n2 in zip(n, n[1:]))
 
def thinning(image):
    changing1 = changing2 = [(-1, -1)]
    while changing1 or changing2:
        # Step 1
        changing1 = []
        for y in range(1, len(image) - 1):
            for x in range(1, len(image[0]) - 1):
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, image)
                if (image[y][x] == 1 and    # (Condition 0)
                    P4 * P6 * P8 == 0 and   # Condition 4
                    P2 * P4 * P6 == 0 and   # Condition 3
                    transitions(n) == 1 and # Condition 2
                    2 <= sum(n) <= 6):      # Condition 1
                    changing1.append((x,y))
        for x, y in changing1: image[y][x] = 0
        # Step 2
        changing2 = []
        for y in range(1, len(image) - 1):
            for x in range(1, len(image[0]) - 1):
                P2,P3,P4,P5,P6,P7,P8,P9 = n = neighbours(x, y, image)
                if (image[y][x] == 1 and    # (Condition 0)
                    P2 * P6 * P8 == 0 and   # Condition 4
                    P2 * P4 * P8 == 0 and   # Condition 3
                    transitions(n) == 1 and # Condition 2
                    2 <= sum(n) <= 6):      # Condition 1
                    changing2.append((x,y))
        for x, y in changing2: image[y][x] = 0
        #print changing1
        #print changing2
    return image

def to_array(image_data, image_width, image_height):
	image_array = [[image_data[(j * image_height + i)] for i in range(image_width)] for j in range(image_height)]
	return image_array


def analysis(image_path):
	# col = Image.open("cat-tied-icon.png")
	# gray = col.convert('L')
	# bw = gray.point(lambda x: 0 if x<128 else 255, '1')
	# bw.save("result_bw.png")
	col = Image.open(image_path)
	gray = col.convert('L')
	bw = gray.point(lambda x: 0 if x<128 else 255, '1')
	bw_array = to_array(list(bw.getdata()), bw.width, bw.height)
	image = thinning(bw_array)
	
	s = (len(image), len(image[0]))
	N = 3
	n = (N - 1) / 2
	r = s[0] + 2 * n
	c = s[1] + 2 * n

	temp = image
	mat = [[0 for j in range(3)] for i in range(3)]
	bifurcation = [[0 for j in range(c)] for i in range(r)]
	ridge = [[0 for j in range(c)] for i in range(r)]

	for x in range((n + 11), (s[0] + n - 9)):
		for y in range((n + 11), (s[1] + n - 9)):
			e = 0
			for k in range((x - n), (x + n + 1)):
				f = 0
				for l in range((y - n), (y + n + 1)):
					mat[e][f] = (temp[k][l]) / 255
					f += 1
				e += 1
			if mat[1][1] == 0:
				ridge[x][y] = sum(map(sum, mat))
				bifurcation[x][y] = sum(map(sum, mat))
			mat = [[0 for j in range(3)] for i in range(3)]

	print ridge, bifurcation
	ridge_x = []
	ridge_y = []
	bifurcation_x =[]
	bifurcation_y =[]

	for i in range(c):
		for j in range(r):
			if ridge[i][j] == 2:
				ridge_x.append(i)
				ridge_y.append(j)
			if bifurcation[i][j] == 4:
				bifurcation_x.append(i)
				bifurcation_y.append(j)

	return ridge_x, ridge_y, bifurcation_x, bifurcation_y


print analysis("sample.bmp")
