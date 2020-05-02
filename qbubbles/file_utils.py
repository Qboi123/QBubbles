from qbubbles import gameIO
import os
import pathlib
from typing import Optional, Union, List, Dict, Tuple


def split_path(path: str):
    return tuple(path.replace("\\", "/").split("/"))


class EditableClass(object):
    def __setattr__(self, key, value):
        self.__dict__[key] = value

    def __getattr__(self, item):
        return self.__dict__[item]


class Directory(object):
    def __init__(self, path):
        import os
        self.os = os

        self.path = path
        self.dirName = os.path.split(path)[-1]

        self.absPath: str = os.path.abspath(path)
        try:
            self.relPath: str = os.path.relpath(path)
        except ValueError:
            self.relPath: Optional[str] = None

    def delete(self, ignore_errors: bool = False):
        import shutil
        shutil.rmtree(self.path, ignore_errors)

    def copy(self, to):
        import shutil
        shutil.copy(self.path, to)

    def move(self, to):
        import shutil
        shutil.move(self.path, to)

    def rename(self, name, change_path=True):
        if not self.os.path.isabs(name):
            name = self.os.path.abspath(name)
        else:
            if not self.os.path.abspath(self.os.path.join(*self.os.path.split(name)[:-1])) == self.upper().path:
                raise IOError("Can't rename file to another directory")
        self.os.rename(self.os.path.abspath(self.path), name)

        if change_path:
            if self.os.path.isabs(self.path):
                self.path = self.os.path.abspath(name)
            else:
                self.path = self.os.path.relpath(name)

    def listdir(self):
        return self.index()

    def index(self):
        list_ = []
        list_.extend(self.listdirs())
        list_.extend(self.listfiles())
        return list_

    def listdirs(self):
        list_: List[Directory] = []
        for item in self.os.listdir(self.path):
            if self.os.path.isdir(self.os.path.join(self.path, item)):
                list_.append(Directory(self.os.path.join(self.path, item)))
        return list_

    def listfiles(self):
        list_: List[File] = []
        for item in self.os.listdir(self.path):
            if self.os.path.isfile(self.os.path.join(self.path, item)):
                list_.append(File(self.os.path.join(self.path, item)))
        return list_

    @staticmethod
    def _split_path(path: str):
        return tuple(path.replace("\\", "/").split("/"))

    def upper(self):
        s_path = self._split_path(self.path)
        print(s_path)
        if len(s_path) >= 2:
            up = self.os.path.split(self.path)[0]
            print(up)
            return Directory(up)
        return Directory(self.path)


class File(object):
    def __init__(self, path):
        import os
        import mimetypes

        self.directory = Directory(os.path.abspath(os.path.join(*os.path.split(path)[:-1])))
        self.path: str = path
        self.fileName = os.path.split(path)[-1]
        self.absPath: str = os.path.abspath(path)
        try:
            self.relPath: str = os.path.relpath(path)
        except ValueError:
            self.relPath: Optional[str] = None
        self.os = os

        self._fd: Optional[gameIO.IOBase] = None
        self._fileOpen = False

        try:
            self.mimeType = mimetypes.read_mime_types(self.path)
        except UnicodeDecodeError:
            pass

    def get_json(self):
        return JsonFile(self.path)

    def start_file(self):
        self.os.startfile(self.path)

    def open(self, mode="w"):
        file_was_open = self._fileOpen
        if not self._fileOpen:
            self._fd = open(self.path, mode)
            self._fileOpen = True
        else:
            pass
        return file_was_open

    def close(self):
        self._fd.close()
        self._fileOpen = False

    def exists(self):
        return self.os.path.exists(self.path)

    def read(self, size=None):
        file_was_open = self._fileOpen
        if not self._fileOpen:
            self.open(mode="r")

        self._fd.read(size)

        if not file_was_open:
            self.close()

    def write(self, data):
        if type(data) == str:
            data: str
            self._fd.write(data.encode())
        elif type(data) in [bytes, bytearray]:
            self._fd.write(data)
        elif type(data) in [int, float, bool]:
            self._fd.write(str(data).encode())
        elif type(data) in [dict, list]:
            import json
            self._fd.write((json.JSONEncoder().encode(data)).encode())
        elif type(data) in [tuple]:
            import json
            self._fd.write((json.JSONEncoder().encode(list(data))).encode())
        else:
            self._fd.write(repr(data))

    def subprocess(self, *args):
        import subprocess
        subprocess.call([self.absPath, *args], cwd=self.directory.absPath)

    def execute(self, *args):
        self.os.system(" ".join([*args]))

    def write_lines(self, data: Union[List, Tuple]):
        for obj in data:
            self.write(obj)

    def write_yaml(self, data):
        import yaml

        file_was_open = self._fileOpen
        if not self._fileOpen:
            self.open(mode="r")

        yaml.dump(data, self._fd)

        if file_was_open:
            self.close()

    def write_at(self, offset: int, data):
        file_was_open = self.open(mode="r+b")
        self._fd.seek(offset)

        if type(data) == str:
            data: str
            self._fd.write(data.encode())
        elif type(data) in [bytes, bytearray]:
            self._fd.write(data)
        elif type(data) in [int, float, bool]:
            self._fd.write(str(data).encode())

        if not file_was_open:
            self.close()

    def read_at(self, offset: int, size: int = -1) -> bytes:
        file_was_open = self.open(mode="r+b")
        self._fd.seek(offset)

        data = self._fd.read(size)
        if not file_was_open:
            self.close()

        return data

    def create(self, size=0):
        file_was_open = self.open("w+")

        if size == 0:
            self.close()
            return
        self._fd.seek(size - 1)
        self._fd.write(chr(0))

        if not file_was_open:
            self.close()

    def remove(self):
        self.os.remove(self.path)

    def delete(self):
        self.remove()

    def rename(self, name, change_path=True):
        if not self.os.path.isabs(name):
            name = self.os.path.abspath(name)
        else:
            if not self.os.path.abspath(self.os.path.join(*self.os.path.split(name)[:-1])) == self.directory.path:
                raise IOError("Can't rename file to another directory")
        self.os.rename(self.os.path.abspath(self.path), name)

        if change_path:
            if self.os.path.isabs(self.path):
                self.path = self.os.path.abspath(name)
            else:
                self.path = self.os.path.relpath(name)

    def get_size(self):
        return self.os.path.getsize(self.path)

    def get_ctime(self):
        return self.os.path.getctime(self.path)

    def get_atime(self):
        return self.os.path.getatime(self.path)

    def get_mtime(self):
        return self.os.path.getmtime(self.path)

    def get_dev(self):
        return os.lstat(self.path).st_dev

    def get_uid(self):
        return os.lstat(self.path).st_uid

    def get_gid(self):
        return os.lstat(self.path).st_gid

    def get_mode(self):
        return os.lstat(self.path).st_mode

    def get_owner(self):
        return pathlib.Path(self.path).owner()


class JsonFile(File):
    def __init__(self, path):
        super().__init__(path)

        del self.subprocess
        del self.execute

        import json
        self._mJson = json

        self.nzt: Optional[Union[List, Dict]] = None
        self.nzt = self._mJson.JSONDecoder().decode(self.read())

    def read_json(self):
        self.nzt = self._mJson.JSONDecoder().decode(self.read())

        return self.nzt

    def write_json(self):
        self.write(self._mJson.JSONEncoder().encode(self.nzt))

        return self.nzt


class DataFile(File):
    def __init__(self, path):
        super().__init__(path)

        del self.subprocess
        del self.execute

        import pickle
        self._pickle = pickle

        self.data: Optional[object] = None
        self.read_data()

    def read_data(self):
        file_was_open = self._fileOpen
        if not file_was_open:
            self.open("rb")

        self.data = self._pickle.load(self._fd)

        if not file_was_open:
            self.close()

    def write_data(self, o: object):
        file_was_open = self._fileOpen
        if not file_was_open:
            self.open("wb")

        self.data = self._pickle.dump(o, self._fd)

        if not file_was_open:
            self.close()
