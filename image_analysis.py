from PIL import Image

img = Image.open("sample_images/identify_2016-02-26_20-37-59_00.bmp")
print img.getpixel((0,0))
pixels = []
for x in range(img.size[0]):
	tmp = []
	for y in range(img.size[1]):
		tmp.append(img.getpixel((x, y)))
	pixels.append(tmp)

