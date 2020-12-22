import setuptools

import sliceable_generator

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sliceable-generator",
    version=sliceable_generator.__version__,
    author=sliceable_generator.__author__,
    author_email=sliceable_generator.__email__,
    description="Sliceable subscriptable reusable generator.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/panhaoyu/sliceable-generator",
    packages=['sliceable_generator'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)


