from setuptools import setup, find_packages

def reader(file_name: str) -> str:
	with open(file_name, "r") as file:
		reqs = file.read()
	return reqs

setup(
    name='engine crawler',
    author="Romy",
    version='3.1.7',
    packages=find_packages(),
    provides_extra=reader( "requirements.txt" ).split( "\x0a" ),
    entry_points={
        'console_scripts': [
            'engine_romy = src.__init__:main'
        ]
    },
)