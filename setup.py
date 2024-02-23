from setuptools import setup, find_packages

setup(
    name='engine crawler',
    version='2.0.0',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'engine_romy = src:main'
        ]
    },
)