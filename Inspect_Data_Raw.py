"""
Script to load the Raw data in the BIDS Format
"""
##
# ---------------------------------------------------------------------------------------------------------------------
# Cell to Import Libraries
# ---------------------------------------------------------------------------------------------------------------------
import matplotlib
import matplotlib.pyplot as plt
import pathlib
import mne
from mne import Epochs, pick_types, events_from_annotations
from mne.channels import make_standard_montage
from mne.io import concatenate_raws, read_raw_edf
from mne.datasets import eegbci
from mne.decoding import CSP
import mne_bids

# Define variable
from mne.datasets import eegbci

subject = 1
runs = [6, 10, 14]  # motor imagery: hands vs feet
tmin, tmax = -0.5, 0.5
event_id = dict(rest=1,
                hands=2,
                feet=3)

##
# ---------------------------------------------------------------------------------------------------------------------
# Cell to Import dataset of the subject for the motor imagery: hands vs feet
# ---------------------------------------------------------------------------------------------------------------------
# Load the raw data after the fixing
raw_path = 'Data_Out/fixed_raw.fif'
raw = mne.io.read_raw_fif(raw_path, preload=True)

# Create Events
events, _ = events_from_annotations(raw, event_id=dict(T0=1, T1=2, T2=3))

# Define the picks
picks = pick_types(raw.info, meg=False, eeg=True, stim=False, eog=False, exclude='bads')

# Select only the EEG channel (create a copy of our raw data)
raw_eeg = raw.copy().pick_types(meg=False, eeg=True, eog=False, exclude='bads')

# Filter the data between [7, 30] Hertz
raw_eeg_filtered = raw_eeg.copy().filter(7., 30., fir_design='firwin', skip_by_annotation='edge')

##
# ---------------------------------------------------------------------------------------------------------------------
# Display the information about the raw file
# ---------------------------------------------------------------------------------------------------------------------
print(raw_eeg_filtered.info)

print(raw_eeg_filtered.ch_names)

##
# ---------------------------------------------------------------------------------------------------------------------
# Plot Raw data
# ---------------------------------------------------------------------------------------------------------------------
# Plot data channel
# raw_eeg_filtered.plot()
# plt.show()

# Plot Sensors eeg
# raw_eeg_filtered.plot_sensors(ch_type='eeg')
# plt.show()

# Plot Sensors eeg 3D
# raw_eeg_filtered.plot_sensors(kind='3d', ch_type='eeg')
# plt.show()

# Plot with events id
# raw_eeg_filtered.plot(events=events, event_id=event_id)
# plt.show()

##
# ---------------------------------------------------------------------------------------------------------------------
# TODO Save data in bids mode
# ---------------------------------------------------------------------------------------------------------------------
"""
out_path = pathlib.Path('Data_BIDS/sample_BIDS')

# Define the BIDS path, we need only to specify the entities.
bids_path = mne_bids.BIDSPath(subject='01',
                              session='01',
                              task='motor imagery: hands vs feet',
                              run='01',
                              root=out_path)

# Write the BIDS files
mne_bids.write_raw_bids(raw_eeg_filtered,
                        bids_path=bids_path,
                        events_data=events,
                        event_id=event_id,
                        overwrite=True,
                        allow_preload=True)
"""

##
# ---------------------------------------------------------------------------------------------------------------------
# Epoch and Evoked
# ---------------------------------------------------------------------------------------------------------------------
epochs = Epochs(raw_eeg_filtered,
                events,
                event_id,
                tmin,
                tmax,
                proj=True,
                baseline=None,
                preload=True)

print(epochs)

# Plot Epochs
# epochs.plot()
# plt.show()

# epochs.plot_image()
# plt.show()

# Save the Epoch (note that _epo.fif is quite a convention)
epochs.save('Data_Out/epochs_epo.fif', overwrite=True)

#Create the Evoked
evoked_hands = epochs['hands'].average()
evoked_feet = epochs['feet'].average()

#Plot Evoked
# evoked_hands.plot(spatial_colors=True)
# plt.show()

# evoked_hands.plot_topomap()
# plt.show()

# evoked_hands.plot_joint()
# plt.show()

# mne.viz.plot_compare_evokeds([evoked_hands, evoked_feet])
# plt.show()

# Save the evoked
mne.write_evokeds('Data_Out/evokeds_ave.fif', evoked=[evoked_hands, evoked_feet])


##
# ---------------------------------------------------------------------------------------------------------------------
# TODO Preprocessing
# ---------------------------------------------------------------------------------------------------------------------
