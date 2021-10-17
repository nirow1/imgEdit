import PIL.Image

#změna velikosti obrázku
def grayify(image):
    grayscale_image = image.convert("L")
    return(grayscale_image)

def main(): 
	image = PIL.Image.open('40.2_54.2_dem.png')
	grey_img = grayify(image)
	data = list(grey_img.getdata())
	#print(data)
	
	newimg = PIL.Image.new('L', (480, 480))

	for x, pixel in enumerate(data):
		if data[x] <= 140 : #ideal je 134 cca
			data[x] = 0
		else :
			data[x] = 255

	newimg.putdata(data)
	newimg.show()




main()