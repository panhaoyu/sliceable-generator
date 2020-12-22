import os
import shutil

[print(i.encode('gbk').decode('utf-8'), end='') for i in os.popen('python setup.py sdist bdist_wheel').readlines()]
[print(i.encode('gbk').decode('utf-8'), end='') for i in os.popen('twine upload dist/*').readlines()]
shutil.rmtree('dist')
shutil.rmtree('build')
shutil.rmtree('sliceable_generator.egg-info')
