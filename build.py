import os
import shutil
from contextlib import closing
from py_compile import compile
from zipapp import create_archive
from zipfile import ZipFile, ZIP_DEFLATED


def compile_file(from_, to_):
    compile(from_, cfile=to_, optimize=2)


def compile_dir(dir: str, to: str):
    os.makedirs(to, exist_ok=True)
    for item in os.listdir(dir):
        i_path = os.path.join(dir, item).replace("\\", "/")
        t_path = os.path.join(to, item).replace("\\", "/")
        if os.path.isdir(i_path):
            compile_dir(i_path, t_path)
        elif os.path.isfile(i_path):
            if i_path.endswith(".py"):
                compile_file(i_path, t_path+"c")


def create_pyz(folder, to_, compressed=False):
    create_archive(folder, to_, compressed=compressed, filter=lambda path: True, main=None)


def copy_file(src, dst):
    shutil.copy2(src, dst)


# def create_dataarchive(from_, to_):
#     zipfile = ZipFile(to_, "w")
#
#     def add_file(from__, to__):
#         with zipfile.open(to__, "w") as stream:
#             with open(from__, "rb") as file:
#                 data = file.read()
#                 file.close()
#             stream.write(data)
#             stream.close()
#
#     def add_folder(from__, to__):
#         for item in os.listdir(from__):
#             i_path = os.path.join(from__, item).replace("\\", os.sep)
#             t_path = os.path.join(to__, item).replace("\\", os.sep)
#             if os.path.isdir(i_path):
#                 add_folder(i_path, t_path)
#             elif os.path.isfile(i_path):
#                 add_file(i_path, t_path)
#
#     add_folder(from_, "")


def create_dataarchive(basedir, archivename):
    assert os.path.isdir(basedir)
    with closing(ZipFile(archivename, "w", ZIP_DEFLATED)) as z:
        for root, dirs, files in os.walk(basedir):
            #NOTE: ignore empty directories
            for fn in files:
                absfn = os.path.join(root, fn)
                zfn = absfn[len(basedir)-1+len(os.sep)-1:] #XXX: relative path
                z.write(absfn, zfn)


def copy_folder(src, dst):
    shutil.rmtree(dst, False)
    shutil.copytree(src, dst)


def build():
    os.makedirs("obj/code/", exist_ok=True)
    os.makedirs("obj/data/", exist_ok=True)
    os.makedirs("bin/", exist_ok=True)
    os.makedirs("bin/code/", exist_ok=True)
    os.makedirs("bin/data/", exist_ok=True)
    compile_dir("qbubbles/", "obj/code/qbubbles/")
    # compile_file("__main__.py", "obj/__main__.pyc")
    copy_file("__main__.py", "obj/code/__main__.py")
    create_pyz("obj/code/", "bin/QBubbles-1.0_alpha2.pyz")

    copy_folder("qbubbles/config", "obj/data/config")
    copy_folder("qbubbles/lang", "obj/data/lang")
    copy_folder("qbubbles/assets", "obj/data/assets")
    create_dataarchive("obj/data/", "bin/QBubbles-1.0_alpha2-data.zip")


if __name__ == '__main__':
    build()
