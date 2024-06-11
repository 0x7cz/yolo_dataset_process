from label_info import LabelInfo
from typing import Dict,Union
from pathlib import Path
from tqdm import tqdm
import argparse

def unify_filter(class_filter_str:Dict[str,int],class_txt:Dict[int,str])->Dict[int,int]:
    """
        将以中文输入的筛选索引转为具体的class_index
    """
    class_filter_int = {}
    class_swap = {v:k for k,v in class_txt.items()}
    for k,v in class_filter_str.items():
        class_filter_int[class_swap[k]]=v
    return class_filter_int


def gen_classes(class_txt:Dict,class_filter:Dict,gen_cls:str):
    """
        生成新的classes.txt文件
    """
    cls_v = sorted(class_filter.items(),key=lambda x:x[1])  #以value排序
    f = open(gen_cls,'w') 
    for i,(key,val) in enumerate(cls_v):
        if i!=val:
            print("索引和val不相同")
            f.write(f'{class_txt[key]}:{val}\n')
        else:
            f.write(class_txt[key]+'\n')
    f.close()


def run(labels_path:str,class_filter:Union[Dict[str,int],Dict[int,int]],
                  label_name,rm_empty=False,gen_path:str=None):
    
    gen_p = Path(labels_path).parent / label_name if gen_path is None else Path(gen_path)
    gen_p.mkdir(exist_ok=True) 

    label_info = LabelInfo(labels_path)
    class_txt = label_info.parse_classes()
    if isinstance(list(class_filter.keys())[0],str):
        class_filter = unify_filter(class_filter,class_txt)
    for l_p,label in tqdm(label_info.gen_label(),total=len(label_info)):
        n_p = gen_p / l_p.name
        label_str = ''
        for row in label:
            if int(row[0]) in class_filter.keys():
                row[0]=str(class_filter[int(row[0])])
                label_str+=' '.join(row)+'\n'
        if len(label_str) or not rm_empty:
            with open(str(n_p),'w') as f:
                f.write(label_str)
    gen_classes(class_txt,class_filter,gen_p / 'classes.txt')


def filter_parse(x:str):
    import json
    if Path(x).is_file():
        with open(x) as f:
            x = json.load(f)
        return x 
    else:
        return json.loads(x)

def arg_parse():
    parser = argparse.ArgumentParser(description='rewrite label')
    parser.add_argument('--labels_path',type=str,required=True)
    parser.add_argument('--class_filter',type=filter_parse,required=True)
    parser.add_argument('--label_name',type=str,required=False,default='labels2')
    parser.add_argument('--rm_empty',action='store_true')
    args = parser.parse_args()  
    return args


if __name__ == "__main__":
    opt = arg_parse()
    labels_path = opt.labels_path
    class_filter = opt.class_filter
    label_name = opt.label_name
    run(labels_path,class_filter,label_name)
