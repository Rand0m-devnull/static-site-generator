import os
import shutil


def copy_static_files_recursively(source_dir_path, dest_dir_path):
    if not os.path.exists(dest_dir_path):
        os.mkdir(dest_dir_path)

    source_dir_content = os.listdir(source_dir_path)    

    for item in source_dir_content:
        from_path = os.path.join(source_dir_path, item)
        dest_path = os.path.join(dest_dir_path, item)
        print(f" * {from_path} -> {dest_path}")
        if os.path.isfile(from_path):
            shutil.copy(from_path, dest_path)
        else:
            copy_static_files_recursively(from_path, dest_path)
