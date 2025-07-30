from setuptools import setup, find_packages

setup(
    name="edazer",
    version="0.1.3",
    description="lightweight library that provides functionalities for common EDA tasks",
    long_description= open("README.md").read(),
    long_description_content_type= "text/markdown",
    author="Adarsh R",
    author_email="7adarsh9@gmail.com",
    packages=find_packages(),
    install_requires=[
    "pandas>=1.0.0",
    "ipython>=7.0.0",
    "polars>=0.19.0",
    "pyarrow>=10.0.0"
    ],
    python_requires=">=3.6",
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    )