# qc-codar-radialmetric

This python code applies several quality control (QC) functions based CODAR SeaSonde Radialmetric data. There are two aspects to this code. The main code (qcutil.py) runs the QC functions and generates formatted RadialShort output.  The second piece (qcviz.py) is graphical tool to assess different threshold values and size of weighting window on weighted average of radial currents.

### System Requirements

- Python 2.7.x
- Numpy 1.9.x
    - https://pypi.python.org/pypi/numpy
    - Data read into memory are stored in the N-dimensional array datatype (ndarray) for indexing and computation.
- geopy 1.11.0
    - https://pypi.python.org/pypi/geopy
    - geopy.distance.vincenty()
    - Used to compute (LAT, LON) based on range and bearing from site origin in generating RadialShorts file
- matplotlib 1.4.3
- Ipython

### Usage qcutil.py:

    qcutil.py \<datadir\> \<PatternType\>

### Usage qcviz.py:

Use IPython console and use magic to run code as if at unix prompt and provide datadir, patterntype, fn

    e.g. %run qcviz.py [datadir] [patterntype] [fn]
    In[]: cd workspace/qc-codar-radialmetric/
    In[]: %run qcviz.py /Users/codar/Documents/reprocessing_2014_11/Reprocess_HATY_70_35/ IdealPattern RDLv_HATY_2013_11_05_0000.ruv
    In[]: plt.show()

Using test dataset defaults, the input file is ./test/files/codar_raw/Radialmetric/IdealPattern/RDLv_HATY_2013_11_05_0000.ruv

    In[]: cd workspace/qc-codar-radialmetric/
    In[]: %run qcutil.py 
    In[]: plt.show()

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
 
