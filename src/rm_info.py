from pathlib import Path
from datetime import datetime
import argparse
import shutil

class RmAnnInfo:
    def __init__(self,labels_path,images_path) -> None:
        self.labels_p = Path(labels_path)
        self.images_p = Path(images_path)
        self.remove_p = None
        self.remove_im = set()
        self.remove_label = set()
    def remove_info(self):
        for l_p in self.labels_p.rglob('*.txt'):
            if l_p.name == 'classes.txt':
                continue
            im_p = self.images_p / l_p.with_suffix('.jpg').name
            if not im_p.exists() :
                self.remove_label.add(l_p)
        for im_p in self.images_p.rglob('*.jpg'):
            l_p = self.labels_p / im_p.with_suffix('.txt').name
            if not l_p.exists():
                self.remove_im.add(im_p)
        print(f'1.有{len(self.remove_im)} images需要被移除')
        print(f'2.有{len(self.remove_label)} labels需要被移除')
    
    def move_tmp(self):
        self.remove_p = self.labels_p.parent / ('remove_'+datetime.now().strftime('%Y%m%d%H%M'))
        tmp_im_p = self.remove_p /  'images'
        tmp_l_p = self.remove_p / 'labels'
        tmp_im_p.mkdir(parents=True)
        tmp_l_p.mkdir(parents=True)

        for i in self.remove_im:
            shutil.move(str(i),tmp_im_p)
        for i in self.remove_label:
            shutil.move(str(i),tmp_l_p)
    
    def rm(self):
        pass

def arg_parse():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--labels_path',type=str,required=True)
    parser.add_argument('--images_path',type=str,required=False)
    args = parser.parse_args()  
    if args.images_path is None:
        args.images_path = Path(args.labels_path).parent / 'images'
    return args

if __name__ == "__main__":
    args = arg_parse()
    rm_ann= RmAnnInfo(args.labels_path,args.images_path)
    rm_ann.remove_info()
    rm_ann.move_tmp()
