from pathlib import Path
import shutil
import argparse

def all_imgs(root_path,gen_path):
    gen_p = Path(gen_path)
    root_im_p = gen_p / 'images'
    root_l_p = gen_p / 'labels'
    root_im_p.mkdir(exist_ok=True,parents=True)
    root_l_p.mkdir(exist_ok=True)

    for im_p in Path(root_path).rglob('*.jpg'):
        shutil.copy(im_p,root_im_p)    
    for l_p in Path(root_path).rglob('*.txt'):
        shutil.copy(l_p,root_l_p)    

def arg_parse():
    
    parser = argparse.ArgumentParser()
    parser.add_argument('--root_path',type=str,required=True)
    parser.add_argument('--gen_path',type=str,required=True)
    args = parser.parse_args()  
    return args
if __name__ == "__main__":
    args = argparse()
    root_path = args.root_path
    gen_path = args.gen_path
    all_imgs(root_path,gen_path)
    