from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in komal_scientific/__init__.py
from komal_scientific import __version__ as version

setup(
	name="komal_scientific",
	version=version,
	description="komal scientific",
	author="Finbyz Tech Pvt Ltd",
	author_email="info@finbyz.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
