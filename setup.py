from setuptools import setup, find_packages

setup(name='boring_battery',
      version='1.0.0',
      packages=find_packages(),
      install_requires=[
        'openmdao',
        'dymos',
        #'pyoptsparse @ git+https://github.com/mdolab/pyoptsparse@v1.2',  # install manually
        'matplotlib',
        'scipy',
        'pandas',
        'pyspice',
        'testflo',
        'openpyxl',
        'more_itertools',
      ]
)
