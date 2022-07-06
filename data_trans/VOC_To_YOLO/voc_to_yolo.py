# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
from tqdm import tqdm
import os
from os import getcwd

sets = ['train', 'test','val']
#这里使用要改
classes = ['glass', 'metal', 'paper','plastic']


def convert(size, box):
    dw = 1. / (size[0])
    dh = 1. / (size[1])
    x = (box[0] + box[1]) / 2.0 - 1
    y = (box[2] + box[3]) / 2.0 - 1
    w = box[1] - box[0]
    h = box[3] - box[2]
    x = x * dw
    w = w * dw
    y = y * dh
    h = h * dh
    x = round(x,6)
    w = round(w,6)
    y = round(y,6)
    h = round(h,6)
    return x, y, w, h

#后面只用修改各个文件夹的位置
def convert_annotation(image_id):
     #try:
        in_file = open('F:/Pycharm_Projects/data_trans/VOC_To_YOLO/Annotations/%s.xml' % (image_id), encoding='utf-8')
        out_file = open('F:/Pycharm_Projects/data_trans/VOC_To_YOLO/labels/%s.txt' % (image_id), 'w', encoding='utf-8')
        tree = ET.parse(in_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)
        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text),
                 float(xmlbox.find('ymax').text))
            b1, b2, b3, b4 = b
            # 标注越界修正
            if b2 > w:
                b2 = w
            if b4 > h:
                b4 = h
            b = (b1, b2, b3, b4)
            bb = convert((w, h), b)
            out_file.write(str(cls_id) + " " +
                           " ".join([str(a) for a in bb]) + '\n')
     #except Exception as e:
         #print(e, image_id)

#这一步生成的txt文件写在data.yaml文件里
wd = getcwd()
for image_set in sets:
    if not os.path.exists('F:/Pycharm_Projects/data_trans/VOC_To_YOLO/labels/'):
        os.makedirs('F:/Pycharm_Projects/data_trans/VOC_To_YOLO/labels/')
    image_ids = open('F:/Pycharm_Projects/data_trans/VOC_To_YOLO/Imagesets/%s.txt' %
                     (image_set)).read().strip().split()
    list_file = open('F:/Pycharm_Projects/data_trans/VOC_To_YOLO/%s.txt' % (image_set), 'w')
    for image_id in tqdm(image_ids):
        list_file.write('F:/Pycharm_Projects/data_trans/VOC_To_YOLO/JPEGImages/%s.jpg\n' % (image_id))
        convert_annotation(image_id)
    list_file.close()

