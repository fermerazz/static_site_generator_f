import os
import shutil

def copy_static(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.mkdir(dst)
    _copy_recursive(src, dst)

def _copy_recursive(src, dst):
    for entry in os.listdir(src):
            src_path = os.path.join(src, entry)
            dst_path = os.path.join(dst, entry)

            if os.path.isfile(src_path):
                shutil.copy(src_path, dst_path)
            else:
                os.mkdir(dst_path)
                _copy_recursive(src_path, dst_path)