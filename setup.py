import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
        name="simago", 
        version="0.2.0", 
        author="Alexander Harms", 
        author_email="a.g.j.harms@protonmail.com", 
        description="Generate random populations.", 
        long_description=long_description, 
        long_description_content_type="text/markdown", 
        url="https://github.com/alexanderharms/simago", 
        packages=setuptools.find_packages(), 
        classifiers=[ 
        "Programming Language :: Python :: 3", 
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent"], 
        python_requires='>=3.6',
        install_requires=["wheel", "numpy", "scipy", "pandas", "pyYAML"] 
        )
