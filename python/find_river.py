import matplotlib.pyplot as plt
from skimage.color import rgb2gray
from skimage.io import imread
from skimage.filters.thresholding import threshold_minimum, threshold_yen
from skimage.morphology import skeletonize, thin, medial_axis

#výběr trasholdu
def get_binary(image):    
    thresh = threshold_yen(image)
    #thresh = threshold_minimum(image)
    binary = image > thresh
    return binary

#úprava obrázku
path = '40.2_50.6_dem.png'
rem_suff = path.removesuffix('.png')
img = imread(f'img_base/{path}')
img_binary = get_binary(rgb2gray(imread(f'img_base/{path}')))
img_cr = img_binary[0:480, 59:355]
plt.imsave(f'img_binary/{rem_suff}_B.png', img_binary, cmap = plt.cm.gray)

#úplná kostra
img_skel = skeletonize(img_cr)
plt.imsave(f'img_skelet/{rem_suff}_S.png', img_skel, cmap = plt.cm.gray)

#částešně zůžené
img_thin = thin(img_cr, 12)
plt.imsave(f'img_thin/{rem_suff}_T.png', img_thin, cmap = plt.cm.gray)

#za použítí souřadnic
img_ax = medial_axis(img_cr)
plt.imsave(f'img_ax/{rem_suff}_AX.png', img_ax, cmap = plt.cm.gray)

fig, axes = plt.subplots(nrows=1, ncols=4, sharex=True, sharey=True,
                        figsize=(8,8))

ax = axes.ravel()

ax[0].imshow(img_cr, cmap=plt.cm.gray)
ax[0].set_title('Binary image')

ax[1].imshow(img_skel, cmap=plt.cm.gray)
ax[1].set_title('River skeleton')

ax[2].imshow(img_thin, cmap=plt.cm.gray)
ax[2].set_title('Parcialy thined')

ax[3].imshow(img_ax, cmap=plt.cm.gray)
ax[3].set_title('with axes')

for a in ax:
    a.axis('off')

plt.tight_layout()
plt.show()