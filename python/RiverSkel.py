from os import path
from numpy.lib.npyio import save
from skimage.io import imread
from skimage.color import rgb2gray
from skimage import color, feature, restoration, filters, data, io, img_as_bool, morphology, img_as_float
from matplotlib import pyplot as plt
from skimage.filters import threshold_otsu, try_all_threshold
from skimage.filters import meijering, sato, frangi, hessian, roberts, sobel, scharr, prewitt
from skimage import img_as_uint
from skimage.filters.thresholding import threshold_isodata, threshold_mean, threshold_minimum, threshold_triangle, threshold_yen, try_all_threshold
import numpy as np
from skimage.morphology import skeletonize, convex_hull_image
from skimage.filters import threshold_otsu, threshold_local
from skimage.restoration import denoise_nl_means, estimate_sigma


def get_binary(image):    
    thresh = threshold_minimum(image)
    binary = image > thresh
    return binary

path = 'obraz.png'

img = rgb2gray(imread(path))
cropped_img2 = img[0:480, 59:355]
binary = get_binary(rgb2gray(imread(path)))
chull = convex_hull_image(binary)
edges2 = feature.canny(binary, sigma=1)
cropped_img = binary[0:480, 59:355]
skeletonized = skeletonize(cropped_img)
morped = morphology.medial_axis(cropped_img)

fig, ax = try_all_threshold(img, figsize=(10, 8), verbose=False)
plt.show()

imgf = img_as_float(cropped_img2)
sigma_est = np.mean(estimate_sigma(imgf, multichannel= False))

denoised = denoise_nl_means(imgf, h=2 * sigma_est, fast_mode=True,
                           patch_size=5,
                           patch_distance=3,
                           multichannel=False)

#plt.imsave(f'{b}', skeletonized, cmap = plt.cm.gray)

fig, axes = plt.subplots(nrows=1, ncols=3, sharex=True, sharey=True,
                        figsize=(8,8))

ax = axes.ravel()

ax[0].imshow(morped, cmap=plt.cm.gray)
ax[0].contour(cropped_img, [0.5], colors='blue')
ax[0].set_title('Original image')

ax[1].imshow(denoised, cmap=plt.cm.gray)
ax[1].set_title('Denoised')

ax[2].imshow(cropped_img2, cmap=plt.cm.gray,)
ax[2].set_title('Original')

#ax[3].imshow(skeletonized, cmap=plt.cm.gray)
#ax[3].set_title('skeletonized')


for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()