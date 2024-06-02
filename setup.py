from setuptools import setup, find_namespace_packages

setup(
    name='dbxview', 
    version='0.1', 
    packages=find_namespace_packages(), 
    install_requires=open('requirements.txt').read().splitlines(), 
)
