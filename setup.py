# setup.py
import setuptools

setuptools.setup(
    name="shyn_data_works", # pip install
    version="0.0.1",
    packages=setuptools.find_packages(include=['shyn_data_works', 'shyn_data_works.*']), # from shyn_data_works import 
)