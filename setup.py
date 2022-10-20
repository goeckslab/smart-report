from os.path import realpath, dirname, join
from setuptools import find_namespace_packages
from distutils.core import setup


VERSION = '0.1.dev0'
PROJECT_ROOT = dirname(realpath(__file__))

with open(join(PROJECT_ROOT, 'jinja_report', 'requirements.txt'), 'r', encoding="utf-8") as f:
    install_reqs = [line.strip() for line in f if line]

long_description = """

This tool generate an HTML summary report from various file sources, like image, table, raw html and so on.

"""

setup(name='smart-report',
      version=VERSION,
      description='A tool to generate HTML report from file sources.',
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/goeckslab/smart-report/',
      packages=find_namespace_packages(include=['jinja_report'], exclude=['data*']),
      package_data={
          '': ['README.md']},
      include_package_data=True,
      install_requires=install_reqs,
      platforms='any',
      classifiers=[
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.7',
          'Programming Language :: Python :: 3.8',
          'Programming Language :: Python :: 3.9',
          'License :: OSI Approved :: MIT License',
          'Operating System :: Unix',
          'Operating System :: MacOS',
          'Topic :: Scientific/Engineering',
      ])
