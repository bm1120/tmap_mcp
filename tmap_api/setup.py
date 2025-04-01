from setuptools import setup, find_packages

setup(
    name="tmap_api",
    version="0.1.0",
    author="TMAP API 사용자",
    author_email="example@example.com",
    description="TMAP API를 쉽게 사용할 수 있는 Python 모듈",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/tmap_api",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.0",
    ],
) 