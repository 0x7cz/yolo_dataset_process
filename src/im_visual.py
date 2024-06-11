from label_info import LabelInfo
from ultralytics.utils.plotting import Annotator,colors
from typing import List,Union
import numpy as np
import cv2
from pathlib import Path
from tqdm import tqdm
import argparse

class LabelPaint():
    """
        根据标签索引图片,然后进行绘制
    """
    def __init__(self,labels_path,class_path=None) -> None:
        self.label_info = LabelInfo(labels_path,class_path=class_path)
        names = self.label_info.parse_classes()
        self.paint = PaintProc(names)

    def _xywh2xyxy(self,x,shape):
        y = np.copy(x)
        y[..., 0] = x[..., 0] - x[..., 2] / 2 
        y[..., 1] = x[..., 1] - x[..., 3] / 2 
        y[..., 2] = x[..., 0] + x[..., 2] / 2 
        y[..., 3] = x[..., 1] + x[..., 3] / 2 
        return y*[shape[1],shape[0],shape[1],shape[0]]

    def visual(self,images_path,visuals_path=None,interval=1):
        Path(visuals_path).mkdir(exist_ok=True)
        len_ls = len(self.label_info)
        pbar = tqdm(self.label_info.gen_label(),total=len_ls)
        pbar.set_description(f"处理图片{len_ls}张，可视化图片{len_ls//interval}张")
        
        for i,(label_path,label) in enumerate(pbar):
            if i%interval!=0:
                continue
            image_p = Path(images_path) / Path(label_path).with_suffix('.jpg').name
            im = cv2.imread(str(image_p))
            im_shape = im.shape[:2]
            label = np.array(label,dtype=float)
            if len(label):  # 如果标注信息为空
                bbox = self._xywh2xyxy(label[...,1:],im_shape)
                det = np.concatenate((bbox,np.expand_dims(label[:,0], axis=-1)),axis=-1)
                im=self.paint(im,det)
            visual_p = Path(visuals_path) / image_p.name
            cv2.imwrite(str(visual_p),im)
            
class PaintProc():
    """
        对单张图片进行绘制。输入im,bboxs,labels
    """
    def __init__(self,names:Union[List,str]) -> None:
        if isinstance(names,str) and names.endswith('txt'):
            with open(names,'r',encoding='utf-8') as f:
                names = f.readlines()
        self.names = names

    def proc(self,im,det):
        annotator = Annotator(im,line_width=3)
        for *xyxy,label in det:
            label = int(label)
            bbox_tag = f'{self.names[label]}'
            annotator.box_label(xyxy,bbox_tag,color=colors(label,True))
        im0 = annotator.result()
        return im0
    

    __call__ = proc

def arg_parse():
    parser = argparse.ArgumentParser(description='图片可视化')
    parser.add_argument('--labels_path',type=str,required=True)
    parser.add_argument('--images_path',type=str,required=False)
    parser.add_argument('--visuals_path',type=str,required=False)
    parser.add_argument('--class_path',type=str,required=False)
    parser.add_argument('--interval',type=int,required=False,default=1)
    args = parser.parse_args()  
    if args.visuals_path is None:
        args.visuals_path = Path(args.labels_path).parent / 'visuals'
    if args.images_path is None:
        args.images_path = Path(args.labels_path).parent / 'images'

    return args

if __name__ == "__main__":
    args = arg_parse()
    lp = LabelPaint(args.labels_path,args.class_path)
    lp.visual(args.images_path,args.visuals_path,interval=args.interval)