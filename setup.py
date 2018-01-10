from setuptools import setup, find_packages

setup(
    name='isadream',
    author='Tyler Biggs',
    author_email='biggstd@gmail.com',
    version='0.1',
    packages=find_packages(),
    py_modules=['isadream'],
    install_requires=[
        'isatools',
        'pandas',
    ],
)
