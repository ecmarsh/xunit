from setuptools import setup


setup(name='xunit',
      version='0.0.1',
      packages=['xunit'],
      entry_points={
          'console_scripts': [
              'xunit = xunit.__main__:main'
          ]
      },
      )
