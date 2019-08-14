from setuptools import setup, find_packages
import sys

__version__ = '1.0.1'

install_requires = [
    'docopt', 
    'numpy',
    'geopy',
    ]

qcviz_requires=[
    'matplotlib',
    ]

tests_requires= [
    'nose',
    ]

setup(name='qccodar',
      version=__version__,
      description="Apply quality controls to improve CODAR ouput",
      long_description="",
      classifiers=[
    "Programming Language :: Python :: 2",
    "Programming Language :: Python :: 2.7",
    ],
      keywords='qc codar radials currents ocean science data',
      author='Sara Haines',
      author_email='sarahaines@unc.edu',
      maintainer='Sara Haines',
      maintainer_email='sarahaines@unc.edu',

      url='http://nccoos.unc.edu',
      license='GNU',
      packages=find_packages('src'),
      package_dir={'': 'src'},
      include_package_data=True,
      zip_safe=False,
      namespace_packages=["qccodar", "qccodar.qcviz", "qccodar.test"],
      install_requires=install_requires,
      extras_require={
        'tests' : tests_requires,
        'qcviz' : qcviz_requires
        },
      test_suite="qccodar.test",
      entry_points="""
        [console_scripts]
        qccodar = qccodar.app:main
      """
      )
