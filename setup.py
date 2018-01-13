from setuptools import setup, find_packages

setup(
    name='isaDream',
    author='Tyler Biggs',
    author_email='biggstd@gmail.com',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    py_modules=['isaDream'],
    install_requires=[
        'isatools',
        'pandas',
    ],
)
