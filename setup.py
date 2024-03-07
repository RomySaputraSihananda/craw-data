from setuptools import setup, find_packages

from src import __version__, __url__, __author_email__, __autor__, __description__, __license__, __title__ 

def reader(file_name: str) -> str:
	with open(file_name, "r") as file:
		reqs = file.read()
	return reqs

setup(
    name=__title__,
	description=__description__,
    author=__autor__,
    author_email=__author_email__,
    url=__url__,
    version=__version__,
    long_description=reader( "README.md" ),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    include_package_data=True,
    package_dir={"": "src"},
    python_requires=">=3.11",
    install_requires=reader( "requirements.txt" ).split( "\x0a" ),
    license=__license__,
    zip_safe=False,
    entry_points={
        'console_scripts': [
            'engine_romy = src.__init__:main'
        ]
    },
)
