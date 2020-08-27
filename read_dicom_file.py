# -*-coding:utf-8-*-

"""
this script is read dicom file
"""

import cv2
import numpy
import dicom
from matplotlib import pyplot as plt


def read_dcm(dcm_data):
    slices = []
    dcm = dicom.read_file(dcm_data)
    dcm.image = dcm.pixel_array * dcm.RescaleSlope + dcm.RescaleIntercept


    slices.append(dcm)
    img = slices[int(len(slices) / 2)].image.copy()
    ret, img = cv2.threshold(img, 90, 3071, cv2.THRESH_BINARY)
    img = numpy.uint8(img)

    im2, contours, _ = cv2.findContours(img, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    mask = numpy.zeros(img.shape, numpy.uint8)
    for contour in contours:
        cv2.fillPoly(mask, [contour], 255)
    img[(mask > 0)] = 255

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2, 2))
    img = cv2.morphologyEx(img, cv2.MORPH_OPEN, kernel)

    img2 = slices[int(len(slices) / 2)].image.copy()
    img2[(img == 0)] = -2000

    plt.figure(figsize=(12, 12))
    plt.subplot(131)
    plt.imshow(slices[int(len(slices) / 2)].image, 'gray')
    plt.title('Original')
    plt.subplot(132)
    plt.imshow(img, 'gray')
    plt.title('Mask')
    plt.subplot(133)
    plt.imshow(img2, 'gray')
    plt.title('Result')
    plt.show()


if __name__ == "__main__":
    dicom_root = ""
    read_dcm(dicom_root)