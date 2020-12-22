import os
import shutil

os.system('python setup.py sdist bdist_wheel')
os.system('twine upload dist/*')
shutil.rmtree('dist')
shutil.rmtree('build')
shutil.rmtree('sliceable_generator.egg-info')
