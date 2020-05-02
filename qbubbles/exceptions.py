import traceback as tb
import sys


class DuplicateAddonError(Exception):
    __name__ = "DuplicateAddonError"

    def __init__(self, addonid, name, version, filename, func):
        self.__class__.__name__ = "DuplicateAddonError"
        super(DuplicateAddonError, self).__init__(f"Duplicate addon found: {addonid}, "
                                                f"version: {version}, "
                                                f"filename: {filename}")
        self.args = (addonid, name, version, filename, func)

    def __str__(self):
        addonid = self.args[0]
        version = self.args[2]
        filename = self.args[3]
        return f"Duplicate addon found: {addonid}, " \
               f"version: {version}, " \
               f"filename: {filename}"

    def __repr__(self):
        return self.__class__.__name__


class ParserError(Exception):
    __name__ = "ParserError"

    def __init__(self, *args):
        self.__class__.__name__ = "ParserError"
        super(ParserError, self).__init__(*args)

    def __repr__(self):
        return self.__class__.__name__


class SceneNotFoundError(Exception):
    __name__ = "SceneNotFoundError"

    def __init__(self, *args: object):
        self.__class__.__name__ = "SceneNotFoundError"
        super(SceneNotFoundError, self).__init__(*args)

    def __repr__(self):
        return self.__class__.__name__


class ModeNotFoundError(Exception):
    __name__ = "ModeNotFoundError"

    def __init__(self, *args: object):
        self.__class__.__name__ = "ModeNotFoundError"
        super(ModeNotFoundError, self).__init__(*args)

    def __repr__(self):
        return self.__class__.__name__


class UnlocalizedNameError(Exception):
    __name__ = "UnlocalizedNameError"

    def __init__(self, *args: object):
        self.__class__.__name__ = "UnlocalizedNameError"
        super(UnlocalizedNameError, self).__init__(*args)

    def __repr__(self):
        return self.__class__.__name__


# class ModernError(Exception):
#     def __init__(self, text: str):
#         pass
#         # import os
#         #
#         # print(tuple(tb.FrameSummary.__dict__.keys()))
#         # print("%s exception Thrown:" % self.__repr__()[:-2])
#         #
#         # a = tb.extract_stack(self.__traceback__)
#         # a = a[:-1]
#         # for j in list(a):
#         #     # print()
#         #     # print(a[j].lineno)
#         #
#         #     print("    %s: (%s:%s)" % (j.name, j.filename.split("/")[-1], j.lineno))
#         #
#         #     # b = ""
#         #     # for i in a:
#         #     #     b += i
#         #     # print(i)
#         # exit(1)


# def modern_error(type, value, traceback):
#     import os
#
#     print(tuple(tb.FrameSummary.__dict__.keys()))
#     print("%s: %s" % (type()[:-2], value))
#
#     a = tb.extract_stack(traceback)
#     a = a[:-1]
#     for j in list(a):
#         # print()
#         # print(a[j].lineno)
#
#         print("    %s: (%s:%s)" % (j.name, j.filename.split("/")[-1], j.lineno))
#
#         # b = ""
#         # for i in a:
#         #     b += i
#         # print(i)
#     exit(1)


# # print(modern_error(None, None, None))
# def my_excepthook(exc_type, exc_value, _tb):
#     import random
#     import sys, os
#     import time
#     import wx
#     import wx._core as wx_core
#
#     try:
#         c = wx.Frame()
#     except wx_core.PyNoAppError:
#         wx.App()
#         c = wx.Frame()
#     c.Show(False)
#
#
#     tme = time.strftime
#     filename1 = tme("crashreport_%d_%m_%Y_-_%H_%M_%S.log")
#     save_path = "crashes/" + filename1
#
#     try:
#         os.makedirs("crashes")
#     except FileExistsError:
#         pass
#     with open(save_path, "w+") as file:
#         stdout_bak = sys.stdout
#         sys.stdout = file
#
#         # print(type(_tb))
#
#         # print(tuple(tb.FrameSummary.__dict__.keys()))
#         print("Python exception %s: %s:" % (exc_type.__name__, exc_value))
#
#         a = _tb
#         while _tb:
#             # print()
#             # print(a[j].lineno)
#
#             filename = _tb.tb_frame.f_code.co_filename
#             name = _tb.tb_frame.f_code.co_name
#             lineno = _tb.tb_lineno
#             print("    %s: (%s:%s)" % (name, filename.split("/")[-1], lineno))
#
#             # b = ""
#             # for i in a:
#             #     b += i
#             # print(i)
#             _tb = _tb.tb_next
#
#         a = str(sys.getwindowsversion())
#
#         print()
#         print('Overview of the error:')
#         print("  Game arguments: %s" % sys.argv)
#         print("  Windows Version: %s.%s, build: %s" % (a[0], a[1], a[2]))
#         print("  Platform: %s" % sys.platform)
#
#         sys.stdout = stdout_bak
#         # exit(1)
#
#     with open(save_path, "r") as file:
#         wx.MessageBox("Take a look in the crashes folder of the game.\n"
#                       "Filename: "+filename1, exc_type.__name__, wx.OK|wx.CENTRE|wx.ICON_ERROR)
#         # b.Show()
#         os.system("notepad ..\\..\\crashes\\"+filename1)
#
#
# def divide_zero():
#     1 / 0  # raise ZeroDivisionError
#
#
# def f():
#     divide_zero()
#
#
# # if __name__ == '__main__':
# #     sys.excepthook = my_excepthook
# #     import error
#
#
# class SyntaxError(ModernError):
#     pass
#
#
# class ImportError(ModernError):
#     pass
#
#
# class NameError(ModernError):
#     pass
#
#
# class IndexError(ModernError):
#     pass


# sys.excepthook = ModernError
#
# ClassRequirementInvalid = ModernError
#
# def error4():
#     error3()
#
#
# def error3():
#     ClassRequirementInvalid()
#
#
# def error2():
#     error4()
#
#
# def error1():
#     error2()

# a = []
# print(a[0])
