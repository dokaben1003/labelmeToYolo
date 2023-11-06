'''
Created on Nov 6, 2023
Updated to handle specific directory JSON files and store output in the corresponding output directory

@author: xiaosonh
'''
import os
import json
import argparse
import numpy as np
from labelme import utils
import PIL.Image


class Labelme2YOLO(object):

    def __init__(self, json_dir, to_seg=False):
        self._json_dir = json_dir
        self._to_seg = to_seg

    def _get_yolo_object_list(self, json_data, img_path):
        height, width, _ = np.array(PIL.Image.open(img_path)).shape
        yolo_obj_list = []
        
        yolo_format_list = []
        for shape in json_data['shapes']:
            tmp_yolo_format_list = []
            # 後ほどclassを入れれるようにする
            class_target = 0
            tmp_yolo_format_list.append(class_target)

            label = shape['label']
            points = shape['points']
            # Labelmeのポイントは[x1, y1, x2, y2]形式
            # YOLOのフォーマット [x_center, y_center, width, height]
            for point in points:
                tmp_yolo_format_list.append(point[0] / width)
                tmp_yolo_format_list.append(point[1] / height)

            yolo_format_list.append(tmp_yolo_format_list)

        return yolo_format_list

    def _save_yolo_label(self, json_name, output_dir, yolo_obj_list):
        txt_path = os.path.join(output_dir, json_name.replace('.json', '.txt'))
        
        with open(txt_path, 'w+') as f:
            for yolo_obj in yolo_obj_list:
                yolo_obj_line = ' '.join(map(str, yolo_obj))
                f.write(yolo_obj_line + '\n')

    def _save_yolo_image(self, json_data, json_name, output_dir):
        img_name = json_name.replace('.json', '.png')
        img_path = os.path.join(output_dir, img_name)
        
        if not os.path.exists(img_path):
            img = utils.img_b64_to_arr(json_data['imageData'])
            PIL.Image.fromarray(img).save(img_path)
        
        return img_path
    
    def convert_all(self, output_dir):
        json_files = [f for f in os.listdir(self._json_dir) if f.endswith('.json')]
        for json_file in json_files:
            self.convert_one(json_file, output_dir)

    def convert_one(self, json_name, output_dir):
        json_path = os.path.join(self._json_dir, json_name)
        json_data = json.load(open(json_path))
        
        print('Converting %s ...' % json_name)
        
        img_path = self._save_yolo_image(json_data, json_name, output_dir)
        yolo_obj_list = self._get_yolo_object_list(json_data, img_path)
        print(yolo_obj_list)
        self._save_yolo_label(json_name, output_dir, yolo_obj_list)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--json_dir', type=str, required=True, help='Path of the labelme json files.')
    parser.add_argument('--output_dir', type=str, required=True, help='Output directory to store YOLO txt files.')
    parser.add_argument('--seg', action='store_true', help='Convert to YOLOv5 v7.0 segmentation dataset')
    args = parser.parse_args()

    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)

    converter = Labelme2YOLO(args.json_dir, to_seg=args.seg)
    converter.convert_all(args.output_dir)
