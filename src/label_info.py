from pathlib import Path
from typing import List, Dict, Union

# 处理单例
class LabelInfo():

    def __init__(self,labels_path:str,class_path:str=None) -> None:
        self.class_map = None
        self.labels_path = labels_path
        self.class_path = class_path
        if class_path is None:
            self.class_path = Path(labels_path) / 'classes.txt'

    def parse_classes(self) -> Dict[int,str]:
        class_p = Path(self.class_path)
        with class_p.open('r') as f:
            self.class_map = {i:cla.strip() for i,cla in enumerate(f.readlines())}
        return self.class_map
    
    def gen_label(self):
        """
            label_p:Path,labels:list[list]
            如果label为空,返回数据可能为空,需要做进一步判断
        """
        for label_path in Path(self.labels_path).glob('*.txt'):
            if label_path.name in ('classes.txt',):
                continue
            with Path(label_path).open('r') as f:
                label = [i.strip().split() for i in f.readlines()]
            yield label_path,label
            
    def __len__(self):
        return len(list(Path(self.labels_path).glob('*.txt')))

if __name__ == "__main__":
    
    label_info = LabelInfo('train/labels')
    class_txt = label_info.parse_classes()
    print(class_txt)
    for i in label_info.gen_label():
        print(i)
