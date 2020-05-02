import os

from setuptools import setup
import shutil

if os.path.exists("build/"):
    shutil.rmtree("build/", False)
if os.path.exists("dist/"):
    shutil.rmtree("dist/", False)


s = setup(
    name='QBubbles',
    version='v1.5.0-pre5',
    packages=['qbubbles', 'qbubbles.lib', 'qbubbles.advUtils', 'qbubbles.menus', "qbubbles.init", "qbubbles",
              "qbubbles.sprite", "qbubbles/assets/", "qbubbles/config/", "qbubbles/lang/"],
    url='https://github.com/Qboi123/QplayBubbles-Releaes',
    license='Gnu GPL License - Free for use only, you are not allowed to modify the package contents (only using core-mods)',
    author='Qboi123',
    author_email='',
    description='',
    package_data={"qbubbles": ["qbubbles/__main__.py"]},
    include_package_data=True
)

print(s.include_dirs)
