from setuptools import setup, find_packages
from codecs import open  # To use a consistent encoding
import os.path

here = os.path.abspath(os.path.dirname(__file__))
NAME = 'peps_download'
# Read the version from the relevant file
# with open(os.path.join(here, 'VERSION'), encoding='utf-8') as f:
#     version = f.readline()
# version = version.rstrip('\n')

setup(
    name=NAME,

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='1.0.0',

    description="Python API to download products from  [PEPS](https://peps.cnes.fr)",
    long_description='Python API to download products from  [PEPS](https://peps.cnes.fr)',

    # Project's main homepage.
    url='https://github.com/olivierhagolle/peps_download',

    # Author details
    author='Olivier Hagolle',
    author_email='olivier.hagolle@cesbio.cnes.fr',

    # License
    # license='GPLv3',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        # Project maturity:
        #   2 - Pre-Alpha
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Execution environment
        'Environment :: Console',

        # Indicate who your project is intended for
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: GIS',
        'Topic :: Scientific/Engineering :: Information Analysis',

        # License
        # 'License :: OSI Approved :: '
        # 'GNU General Public License v3 or later (GPLv3+)',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    # What does your project relate to?
    keywords=['CNES', 'Sentinel', 'Remote Sensing'],

    # You can just specify the packages manually here if your project is
    # simple. Or you can use find_packages().
    # find_packages(exclude=['doc', 'tests', 'scripts', 'examples']),
    # packages=find_packages(),

    # List run-time dependencies here.  These will be installed by pip when your
    # project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    # List additional groups of dependencies here (e.g. dev dependencies).
    # You can install these using the following syntax, for example:
    # $ pip install -e .[dev,test]
    extras_require={},

    # If there are data files included in your packages that need to be
    # installed, specify them here.  If using Python 2.6 or less, then these
    # have to be included in MANIFEST.in as well.
    package_data={},  # 'pytools4dart/templates':'templates/plots.xml'
    include_package_data=True,

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages.
    # see
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],  # ('templates', ['templates/plots.xml'])

    # Where to find tests
    # test_suite="tests",

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    scripts=['peps_download.py'],

    py_modules=['peps_download'],

)
