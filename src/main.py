import os, shutil, sys
from copy_static_content import copy_static_files_recursively
from generate_content import generate_pages_recursive


dir_path_static = "./static"
dir_path_public = "./docs"
dir_path_content = "./content"
template_path = "./template.html"
default_basepath = "/"

def main():
    basepath = default_basepath
    if len(sys.argv) > 1:
        basepath = sys.argv[1]

    print("Deleting public directory...")
    if os.path.exists(dir_path_public):
        shutil.rmtree(dir_path_public)

    print("Copying static files to public directory...")
    copy_static_files_recursively(dir_path_static, dir_path_public)

    print("Copying content files to public directory...")
    generate_pages_recursive(dir_path_content, template_path, dir_path_public, basepath)

if __name__ == "__main__":
    main()
   