from pathlib import Path
from typing import Callable,List
import argparse

def record(f_path:str) -> Callable:
    assert not Path(f_path).exists(),f"{f_path}文件已存在，修改路径或者删除"
    def iter(images_path:str):
        with open(f_path,'a',encoding='utf-8') as f:
            for im_p in Path(images_path).glob('*.jpg'):
                f.write(str(im_p)+'\n')
    return iter



def txt_gen(txt_gen_path:str,from_root_paths:List[str]):
    Path(txt_gen_path).mkdir(exist_ok=True)
    txt_train_p = Path(txt_gen_path) / 'train.txt' 
    txt_val_p = Path(txt_gen_path) / 'val.txt' 
    txt_record_p = Path(txt_gen_path) / 'source_record.txt'

    train_iter = record(txt_train_p)
    val_iter = record(txt_val_p)

    with open(txt_record_p,'w') as f:
        for root_path in from_root_paths:
            print(root_path)
            train_p = Path(root_path) / 'train' / 'images'
            val_p = Path(root_path) / 'val' / 'images'
            train_iter(train_p)
            val_iter(val_p)
            f.write(root_path+'\n')

def arg_parse():
    
    parser = argparse.ArgumentParser(description='input_txt输入合并路径，ouput输出结果')
    parser.add_argument('--input_txt',type=str,required=True)
    parser.add_argument('--output_txt',type=str,required=True)
    args = parser.parse_args()  
    return args

if __name__ == "__main__":
    args = arg_parse()
    output_path = args.output_txt
    with open(args.input_txt) as f:
        iter_paths = [i.strip() for i in f.readlines()]
    print(iter_paths)
    txt_gen(output_path,iter_paths)



    
            
