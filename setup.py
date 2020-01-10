import setuptools

with open("README.md", "r") as f:
    long_description = f.read()

setuptools.setup(
    name="cnlunardate",
    version="0.0.4",
    author="Y.B. Pan",
    author_email="yb.pan@yahoo.com",
    description="A Chinese lunar date Python library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YuBPan/cnlunardate",
    py_modules=['cnlunardate'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords="Chinese lunar date",
)
