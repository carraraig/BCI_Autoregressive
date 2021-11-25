"""
Script to download the Raw Dataset (https://mne.tools/dev/generated/mne.datasets.eegbci.load_data.html)
"""

import mne
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci

# Define variable
subject = 1
runs = [6, 10, 14]  # motor imagery: hands vs feet

#download data
raw_fnames = mne.datasets.eegbci.load_data(subject, runs , path='Data_Raw')
raw = concatenate_raws([read_raw_edf(f, preload=True) for f in raw_fnames])

# set channel names
eegbci.standardize(raw)
montage = make_standard_montage('standard_1005')
raw.set_montage(montage)

# strip channel names of "." characters
raw.rename_channels(lambda x: x.strip('.'))

# Save the Raw File in the Data_Out folder
raw.save('Data_Out/fixed_raw.fif', overwrite=True)


