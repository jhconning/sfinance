from setuptools import setup, find_packages

setup(
    name='socialfinance',  # This is a good name
    version='0.1.0',
    packages=find_packages(include=['src', 'src.*']),
    install_requires=['numpy', 'matplotlib', 'ipywidgets', 'Ipython'],  # Correctly formatted list of dependencies
)