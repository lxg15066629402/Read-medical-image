# -*- coding: utf-8 -*-

import SimpleITK as sitk
import matplotlib.pyplot as plt
import numpy as np

def read_data(filename):

    itkimage = sitk.ReadImage(filename)  #读取.mhd文件
    OR=itkimage.GetOrigin()
    print(OR)
    SP=itkimage.GetSpacing()
    print(SP)
    numpyImage = sitk.GetArrayFromImage(itkimage)  #获取数据，自动从同名的.raw文件读取

    return OR, SP, numpyImage

def show_nodules(ct_scan, nodules, Origin, Spacing, pad=2, max_show_num=4): # radius是正方形边长一半，pad是边的宽度,max_show_num最大展示数
    show_index = []
    for idx in range(nodules.shape[0]): # lable是一个nx4维的数组，n是肺结节数目，4代表x,y,z,以及直径
        if idx < max_show_num:
            if abs(nodules[idx, 0]) + abs(nodules[idx, 1]) + abs(nodules[idx, 2]) + abs(nodules[idx, 3]) == 0:
                continue

            x, y, z = int((nodules[idx, 0]-Origin[0])/Spacing[0]), int((nodules[idx, 1]-Origin[1])/Spacing[1]), int((nodules[idx, 2]-Origin[2])/Spacing[2])
        print(x, y, z)
        data = ct_scan[z]
        radius= int(nodules[idx, 3]/Spacing[0]/2)
        # pad = 2*radius
        # 注意 y代表纵轴，x代表横轴
        data[max(0, y - radius):min(data.shape[0], y + radius),
        max(0, x - radius - pad):max(0, x - radius)] = 3000 # 竖线
        data[max(0, y - radius):min(data.shape[0], y + radius),
        min(data.shape[1], x + radius):min(data.shape[1], x + radius + pad)] = 3000 # 竖线
        data[max(0, y - radius - pad):max(0, y - radius),
        max(0, x - radius):min(data.shape[1], x + radius)] = 3000 # 横线
        data[min(data.shape[0], y + radius):min(data.shape[0], y + radius + pad),
        max(0, x - radius):min(data.shape[1], x + radius)] = 3000 # 横线

        if z in show_index: # 检查是否有结节在同一张切片，如果有，只显示一张
            continue
        show_index.append(z)
        plt.figure(idx)
        plt.imshow(data, cmap='gray')

    plt.show()


if __name__ == "__main__":

    file_root = ""
    OR, SP, numpyImage = read_data(file_root)
    b = np.array([[-116.2874457,21.16102581,-124.619925,10.88839157],[-111.1930507,-1.264504521,-138.6984478,17.39699158],[73.77454834,37.27831567,-118.3077904,8.648347161]])
    show_nodules(numpyImage,b,OR,SP)

