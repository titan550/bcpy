import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bcpy",
    version="0.1.5",
    author="John Shojaei",
    author_email="titan550@gmail.com",
    description="Microsoft SQL Server bcp (Bulk Copy) wrapper",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/titan550/bcpy",
    packages=setuptools.find_packages(),
    keywords="bcp mssql",
    classifiers=[
        "Topic :: Database",
        "Programming Language :: Python :: 3",
        "Programming Language :: SQL",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
