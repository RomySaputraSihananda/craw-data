from setuptools import setup, find_packages

setup(
    name='engine crawler',
    version='3.1.6',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'engine_romy = src.__init__:main'
        ]
    },
)