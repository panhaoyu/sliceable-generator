import os
import shutil

[print(i) for i in os.popen('python setup.py sdist bdist_wheel').read()]
[print(i) for i in os.popen('twine upload dist/*').read()]
shutil.rmtree('dist')
shutil.rmtree('build')
shutil.rmtree('sliceable_generator.egg-info')
