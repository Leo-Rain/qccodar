# qccodar

This python code applies several quality control (QC) functions based
on CODAR SeaSonde (COS) Radialmetric data currently output in COS
RadialSuite version 7.x. There are two modes to this code: an auto-
and manual-mode.  Auto-mode is for realtime processing. Manual-mode is
for processing all RadialMetric files in a specified folder in
post-processing. qccodar is intended to run beside (in parallel) to
SeaSonde Analysis and not supplant any processing.  In fact, qccodar
uses the LLUVMerger.app provided by SeaSonde to merge the data back
into standard SeaSonde processing methodology.

## Quickstart

If you are familiar with Python and your system Python installation,
you can install the latest version using
[pip](http://pypi.python.org/pypi/pip). Otherwise follow the detailed
installation procedures provided below. After [installing
pip](http://www.pip-installer.org/en/latest/installing.html) you can
install qccodar with this command:

```bash
   $ pip install qccodar
```

This will install qccodar together with all the required
dependencies. After RadialMetric output is generated, you can run
qccodar either in realtime (auto-mode) processing data found in
CODAR's default data directory /Codar/SeaSonde/Data:

```
   $ qccodar auto
```
*Note:  place command in crontab entry to rerun 

or manually (manual-mode) to process data in other locations, for
example after running CODAR's SpectraOfflineProcessor:

```
   $ qccodar manual --pattern IdealPattern --datadir ./reprocess_HATY/2014_08
```

and for a little help with available options:
```
   $ qccodar --help
```


## Installation

qccodar is a python package and runs under Python 2. Eventhough Mac
OS X comes with Python 2 installed or you can install Python
directly from
[python.org](https://wiki.python.org/moin/BeginnersGuide/Download), it
is recommended to use the lightweight option from
[Conda](https://conda.io/docs/index.html) called
[miniconda](https://conda.io/miniconda.html).  Miniconda contains only
Python and other libraries needed to run Conda itself; other packages
will be downloaded and installed as requested.  Conda has a package
manager which makes this installation easy.  Conda also supports
virtual environments where qccodar can run independently from the
system-installed Python. 

The following instructions show how to install and configure Miniconda2
and qccodar to provide QC'd Radial data based on RadialMetric output.  

While logged on as user `codar`, open a terminal to download (curl) and run the installer script. 

```bash
   $ cd ~/Downloads
   $ curl https://repo.continuum.io/miniconda/Miniconda2-latest-MacOSX-x86_64.sh -o "miniconda.sh"
   $ bash ~/Downloads/miniconda.sh -b -p $HOME/miniconda
   $ export PATH="$HOME/miniconda/bin:$PATH"
```

Refer to the [Conda Installation
Guide](https://conda.io/docs/user-guide/install/index.html) for more
details on installing Conda, making the appropriate adjustments for Miniconda2. 

Creating a conda environment allows the qccodar module and its
dependencies to run isolated from the installed Python avoiding
potential module version conflicts.  While this is not a requirement
to get qccodar running, it is recommended.

As user `codar`, open a new terminal window to source the .bash_profile.

```bash
   $ conda create --name qccodar python
```

Activate the environment:
```bash
   $ source activate qccodar
   (qccodar) $ which python
   /Users/codar/miniconda/envs/qccodar/bin/python
```

1. Install qccodar using pip:
```bash
   (qccodar) $ pip install qccodar
```

2. Alternatively, grab source, unpack, and install using sourced setup.py

Use `git` to retrieve latest repo from the github repo:
```bash
   (qccodar) $ git clone https://github.com/nccoos/qccodar.git
```

Use `curl` to grab the source distribution:
```bash
   $ curl -L -o "qccodar.tar.gz" http://github.com/nccoos/qccodar/tarball/master/
```

Install from source
```bash
   (qccodar) $ cd qccodar
   (qccodar) $ python setup.py install
```

Either method will install qccodar together with all the required
dependencies.  After configuring CODAR RadialSuite to ouput
RadialMetric data, you can then run qccodar in either auto- or
manual-mode. 

## Configuration and Crontab Entry for Realtime QC

First, enable RadialMetric output:

1. Edit line 21 of `AnalysisOptions.txt` in /Codar/SeaSonde/Configs/RadialConfigs.
1. Restart AnalyzeSpectra

```
   1           !21 Enable Radial Metric Output: 0(Off), 1(Enable), 2(Enable MaxVel.)
```

Second, set crontab entry to run qccodar:

1. Make a place to log data, e.g. `$ mkdir ~/logs`
1. Place entry in crontab to run every 15 minutes and log the output

```
$ crontab -l
1,11,21,31,41,51 * * * * /Codar/SeaSonde/Users/Scripts/collect/collect.pl
00,15,30,45 * * * * PATH=$PATH:/sbin /Users/codar/miniconda/envs/qccodar/bin/qccodar auto >> /Users/codar/logs/qccodar-auto.log 2>&1
```

If you get `sh: sysctl: command cannot be found` in output or log,
sysctl might be in another path.  qccodar still runs even when this
cannot be found.  In MacOS -- sysctl is sometimes located in /usr/bin
(or /sbin) and may not be in the path under cron.  Placing
`PATH=$PATH:/usr/sbin` in the task entry, adds the path.

## Background

### Notes

| QC Function        | Description |
| -----------        | ----------- |
| Threshold Tests    | badflag any values that fall below or above a single threshold |
| Weighted Averaging | average several values with weights based on signal quality parameters |

#### QC Threshold Tests:
1. DOA peak power (MSR1, MDR1, MDR2) < 5 dB default 
1. DOA 1/2 power width (3dB down) (MSW1, MDW1, MDW2) > 50 deg default
1. SNR on monopole (MA3S) < 5 dB default
1. SNR on both loops (MA1S and MA2S) < 5 dB

#### Weighted Averaging:
1. Weighting based on Music Power (MSP1, MDP1, MDP2)
1. Weighting based on SNR on monopole (MA3S)
1. No weight function (None) 
 
### System Requirements

- Python 2.7.x
- Numpy 1.9.x
    - https://pypi.python.org/pypi/numpy
    - Data read into memory are stored in the N-dimensional array datatype (ndarray) for indexing and computation.
- geopy 1.11.0
    - https://pypi.python.org/pypi/geopy
    - geopy.distance.vincenty()
    - Used to compute (LAT, LON) based on range and bearing from site origin in generating RadialShorts file
- watchdog 0.8.2
    - Used to monitor a directory for new files and trigger qc and merge process when new RadialMetric file is created
- CODAR SeaSonde RadialSuite 7.x (version 8 does not support RadialMetric output unless requested from CODAR)
    - /Codar/SeaSonde/Apps/Bin/LLUVMerger.app
    - Used to merge spatial and temporal RadialShorts data to final Radial
