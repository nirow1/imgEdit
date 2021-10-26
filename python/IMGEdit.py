import PIL.Image
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.filters import threshold_otsu
from skimage.morphology import skeletonize, medial_axis, thin



#změna velikosti obrázku
def grayify(image):
    grayscale_image = image.convert("L")
    return(grayscale_image)

#nastavitelné proměné
	#jmeno obrázku ke zpracování
path = '40.2_50.6_dem.png'
	#nastavování tresholdu 
tresh = 5				 #-10,10 
	#počet iterací při částečné iteraci
thin_it = 7


rem_suff = path.removesuffix('.png')

def main():
	L_crop = 0
	R_crop = 480

	image = PIL.Image.open(f'img_base/{path}')
	grey_img = grayify(image)
	data = list(grey_img.getdata())

	for pos, val in enumerate(data):
		if pos <250 and val == 255:
			L_crop += 1
		elif pos >250 and pos<480 and val == 255:
			R_crop -=1


	for x, pixel in enumerate(data):
		if data[x] <= 135 + tresh : 
			data[x] = 0
		else :
			data[x] = 255

	newimg = PIL.Image.new('1', (480, 480))
	newimg.putdata(data)
	cropImg = newimg.crop(box = (L_crop,0,R_crop,480))
	cropImg.show()
	cropImg.save(f'img_mybin/{rem_suff}B.png')	

def get_binary(image):    
    thresh = threshold_otsu(image)
    binary = image > thresh
    return binary


def sharpening():

	im = get_binary(imread(f'img_mybin/{rem_suff}B.png'))
	im_ax = medial_axis(im)
	im_sk = skeletonize(im)
	im_thin = thin(im, thin_it)

	fig, axes = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=True,
                        figsize=(8,8))

	ax = axes.ravel()

	ax[2].imshow(im_ax, cmap=plt.cm.gray)
	ax[2].set_title('With axes')

	ax[0].imshow(im_sk, cmap=plt.cm.gray)
	ax[0].set_title('River skeleton')

	ax[1].imshow(im_thin, cmap=plt.cm.gray)
	ax[1].set_title('Parcialy thined')

	plt.tight_layout()
	plt.show()	

main()
sharpening()