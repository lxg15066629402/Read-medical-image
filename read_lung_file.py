# -*- coding:utf-8 -*-

'''
this script is used for basic process of lung in Data Science Bowl
'''

import SimpleITK as sitk
from skimage.morphology import ball, disk, dilation, binary_erosion, remove_small_objects, erosion, closing, \
    reconstruction, binary_closing
from skimage.measure import label, regionprops
from skimage.filters import roberts
from skimage.segmentation import clear_border
from scipy import ndimage as ndi
import matplotlib.pyplot as plt


def get_segmented_lungs(im, plot=False):
    '''
    This funtion segments the lungs from the given 2D slice.


    Step 1: Convert into a binary image.
    Step 2: Remove the blobs connected to the border of the image.
    Step 3: Label the image.
    Step 4: Keep the labels with 2 largest areas.
    Step 5: Erosion operation with a disk of radius 2. This operation is
    seperate the lung nodules attached to the blood vessels.
    Step 6: Closure operation with a disk of radius 10. This operation is
    to keep nodules attached to the lung wall.
    Step 7: Fill in the small holes inside the binary mask of lungs.
    Step 8: Superimpose the binary mask on the input image.
    '''

    if plot == True:
        f, plots = plt.subplots(8, 1, figsize=(5, 40))

    binary = im < -600
    if plot == True:
        plots[0].axis('off')
        plots[0].imshow(binary, cmap=plt.cm.bone)

    cleared = clear_border(binary)
    if plot == True:
        plots[1].axis('off')
        plots[1].imshow(cleared, cmap=plt.cm.bone)

    label_image = label(cleared)
    if plot == True:
        plots[2].axis('off')
        plots[2].imshow(label_image, cmap=plt.cm.bone)

    areas = [r.area for r in regionprops(label_image)]
    areas.sort()
    if len(areas) > 2:
        for region in regionprops(label_image):
            if region.area < areas[-2]:
                for coordinates in region.coords:
                    label_image[coordinates[0], coordinates[1]] = 0

    binary = label_image > 0
    if plot == True:
        plots[3].axis('off')
        plots[3].imshow(binary, cmap=plt.cm.bone)

    selem = disk(2)
    binary = binary_erosion(binary, selem)
    if plot == True:
        plots[4].axis('off')
        plots[4].imshow(binary, cmap=plt.cm.bone)

    selem = disk(10)
    binary = binary_closing(binary, selem)
    if plot == True:
        plots[5].axis('off')
        plots[5].imshow(binary, cmap=plt.cm.bone)

    edges = roberts(binary)
    binary = ndi.binary_fill_holes(edges)
    if plot == True:
        plots[6].axis('off')
        plots[6].imshow(binary, cmap=plt.cm.bone)

    get_high_vals = binary == 0
    im[get_high_vals] = 0
    if plot == True:
        plots[7].axis('off')
        plots[7].imshow(im, cmap=plt.cm.bone)

    plt.show()

    return im


if __name__ == '__main__':
    filename = './raw_data/1.3.6.1.4.1.14519.5.2.1.6279.6001.108197895896446896160048741492.mhd'
    # read.mhd文件
    itkimage = sitk.ReadImage(filename)
    # get data of array
    numpyImage = sitk.GetArrayFromImage(itkimage)
    data = numpyImage[50]
    plt.figure(50)
    plt.imshow(data, cmap='gray')
    im = get_segmented_lungs(data, plot=True)
    plt.figure(200)
    plt.imshow(im, cmap='gray')
    plt.show()