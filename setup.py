from setuptools import setup

setup(name='Raw2NetcdfConverter',
      version='1.0',
      description='This package provides functionality for converting simrad RAW to ICES netcdf in PYTHON.',
      url='https://github.com/sindrevatnehol/Raw2NetcdfConverter',
      author='Sindre Vatnehol',
      author_email='sindre.vatnehol@hi.no',
      license='GPL3',
      packages=['Raw2NetcdfConverter'],
#      install_requires=['pynmea2','pytz'],
      package_data={'':['data/*.nc']},
      zip_safe=False)

