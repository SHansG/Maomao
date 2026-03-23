import os
import glob
import collections

def is_sequence(obj):
    return isinstance(obj, collections.abc.Sequence) and not isinstance(obj, str)

def pack_varargs(args):
    assert isinstance(args, tuple), "please input the tuple `args` as in *args"
    if len(args) == 1 and is_sequence(args[0]):
        return args[0]
    else:
        return args
    
def f_exists(*paths):
    return os.path.exists(f_join(*paths))


def f_join(*fpaths):
    fpaths = pack_varargs(fpaths)
    fpath = f_expand(os.path.join(*fpaths))
    if isinstance(fpath, str):
        fpath = fpath.strip()
    return fpath
    

def f_expand(fpath):
    return os.path.expandvars(os.path.expanduser(fpath))


def f_mkdir(*fpaths):
    fpath = f_join(*fpaths)
    os.makedirs(fpath, exist_ok=True)
    return fpath

def f_abspath(fpath, dir=False):
    if dir:
        return os.path.dirname(os.path.abspath(fpath))
    return os.path.abspath(fpath)

def f_listdir(*fpaths, filter_ext=None, filter=None, sort=True, full_path=False):
    dir_path = f_join(*fpaths)
    if not os.path.exists(dir_path):
        return []
    
    files = os.listdir(dir_path)
    
    if filter is not None:
        files = [f for f in files if filter(f)]
    elif filter_ext is not None:
        files = [f for f in files if f.endswith(filter_ext)]
    
    if sort:
        files.sort()
    
    if full_path:
        return [os.path.join(dir_path, f) for f in files]
    else:
        return files
    
def text_dump(text, *fpath):
    fpath = f_join(*fpath)
    with open(fpath, "w", encoding="utf-8") as f:
        f.write(text)

def text_load(*fpath, by_lines=False) -> str:
    fpath = f_join(*fpath)
    with open(fpath, "r", encoding="utf-8") as f:
        if by_lines:
            return f.readlines()
        else:
            return f.read()