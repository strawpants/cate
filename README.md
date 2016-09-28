<img alt="ECT: ESA CCI Toolbox" align="right" src="https://raw.githubusercontent.com/CCI-Tools/ect-core/master/doc/source/_static/logo/cci-toolbox-logo-latex.jpg" />


[![Build Status](https://travis-ci.org/CCI-Tools/ect-core.svg?branch=master)](https://travis-ci.org/CCI-Tools/ect-core)
[![codecov.io](https://codecov.io/github/CCI-Tools/ect-core/coverage.svg?branch=master)](https://codecov.io/github/CCI-Tools/ect-core?branch=master)
[![Documentation Status](https://readthedocs.org/projects/ect-core/badge/?version=latest)](http://ect-core.readthedocs.io/en/latest/?badge=latest)
                
# ect-core

The Python core of the ESA CCI Toolbox (ECT).

## Contents

* `setup.py` - main build script to be run with Python 3.5
* `ect/` - main package and production code
* `test/` - test package and test code
* `doc/` - documentation in Sphinx/RST format

## Installation

ECT requires Python 3.5+ and prefers a Miniconda or Anaconda environment.

Check out latest ECT code 

    $ git clone https://github.com/CCI-Tools/ect-core.git
    $ cd ect-core

ECT can be run from sources directly, once the following module requirements are resolved:

* `xarray`
* `dask`
* `netcdf4`
* `numpy`
* `scipy`
* `matplotlib`
* `numba`
* `cartopy`
* `basemap`
* `tornado`

The most up-to-date list of module requirements is found in the project's `setup.py` file. Do not install now, please read further first.

It is recommended to install ECT into an isolated Python 3 environment, because this approach avoids clashes 
with existing versions of ECT's 3rd-party module requirements. We recommend using Conda 
([Miniconda](http://conda.pydata.org/miniconda.html) or [Anaconda](https://www.continuum.io/downloads)) 
which will usually also avoid platform-specific issues caused by module native binaries.

Note, after installing Miniconda or Anaconda on Unix and Mac OS you'll need to close and re-open your terminal window for the changes to take effect.

### Installation into a new Conda environment 

Using Conda, you can create a isolated environment for ECT like so

    $ conda create -n ect pytest pytest-cov
    
Then you activate the new environment `ect`:
     
    $ source activate ect
    
Windows users can omit the `source` command and just type 

    $ activate ect

Now we add all required packages to the activated `ect` Conda environment:

    (ect) $ conda install xarray dask numpy scipy matplotlib numba netcdf4 tornado
    (ect) $ conda install -c conda-forge cartopy
    (ect) $ conda install -c conda-forge basemap

Some packages are not available on Anaconda default channels and we have to find them on
another channel (option `-c CHANNEL`). Above we use channel `conda-forge`. 

You can now safely install ECT into the `ect` environment.
    
    (ect) $ python setup.py install
    
### Installation into an existing Python 3 environment 

To install ECT into an existing Python 3.5+ environment just for the current user, use

    $ python3 setup.py install --user
    
To install ECT for development and for the current user, use

    $ python3 setup.py develop --user

Unfortunately, the installation fails on many platforms. In most cases the failure will be caused by the 
`h5py` module dependency, which expects pre-installed HDF-5 C-libraries to be present on your computer. 

On Windows, you may get around this by pre-installing the ECT dependencies (which you'll find in `setup.py`) 
on your own, for example by using Christoph Gohlke's 
[Unofficial Windows Binaries for Python Extension Packages](http://www.lfd.uci.edu/~gohlke/pythonlibs/).

## Getting started

To test the installation, first run the ECT command-line interface. Type
    
    $ ect -h

IPython notebooks for various ECT use cases are on the way, they will appear in the project's
[notebooks](https://github.com/CCI-Tools/ect-core/tree/master/notebooks) folder.

To use them interactively, you'll need to install Jupyter and run its Notebook app:

    $ conda install jupyter
    $ jupyter notebook

Open the `notebooks` folder and select a use case.


## Development

### Contributors

Contributors are asked to read and adhere to our [Developer Guide](https://github.com/CCI-Tools/ect-core/wiki/Developer-Guide).

### Unit-testing

For unit testing we use `pytest` and its coverage plugin `pytest-cov`.

To run the unit-tests with coverage, type

    $ export NUMBA_DISABLE_JIT=1
    $ py.test --cov=ect test
    
We need to set environment variable `NUMBA_DISABLE_JIT` to disable JIT compilation by `numba`, so that 
coverage reaches the actual Python code. We use Numba's JIT compilation to speed up numeric Python 
number crunching code.


## License

The CCI Toolbox is distributed under terms and conditions of the [MIT license](https://opensource.org/licenses/MIT).
