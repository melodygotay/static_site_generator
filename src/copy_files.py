import os
import shutil

def copy_files(src, dst):
    copied_paths = []
    if not os.path.exists(dst):
        os.makedirs(dst)

    for file_name in os.listdir(src):
        source = os.path.join(src, file_name)
        dest = os.path.join(dst, file_name)
        if os.path.isfile(source):
            shutil.copy(source, dest)
            copied_paths.append(source)
        else:
            copied_paths.extend(copy_files(source, dest))
    
    return copied_paths