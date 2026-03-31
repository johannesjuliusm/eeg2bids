"""
bids_from_raw_eeg.py

Automated creation of BIDS data structure with meta data for the Memobaby Study.

Author: 
    Johannes Julius Mohn

Contact:
    johannes.j.mohn@maxplanckschools.de
    
Created:
    2024-04-22 : Creation of original script by Johannes Julius Mohn
    2026-03-26 : Updated to a full project package by Johannes Julius Mohn

License: BSD-3-Clause

Description:
    This script transforms raw EEG data from source to BIDS structure.
    
    The core pipeline BIDSifies data, copies image files (not natively part of
    BIDS), updates .json sidecars with study-specific info, creates exceptions
    for non-BIDS data types included in this study (.bidsignore file),
    creates a study description file, displays updated directory trees for each
    new subject, and finally displays the study info.
    
Notes:
    - Make sure you are working from the right environment. If using Spyder:
      Preferences → Python Interpreter
    - Better even, create a dedicated mne/mne_bids environment and start spyder
      from the console.
    - In Spyder, first, set the working directory to your project folder.
    - Set study parameters (folder paths, study name, tasks, authors, etc.) in
      the config.py file at the project root.
    - If adapting this workflow for your EEG study, change the config.py file,
      and make appropriate changes inside the update_json_sidecar function to
      reflect your tasks. Update migrate_image_files if you have image data
      other than .png or remove if not applicable.
    - Subject identifiers should be in format sub-XXXX or you need to adjust
      get_subjects_from_folders accordingly.
"""

import os
import json
from pprint import pprint

from config import raw_root, bids_root, session_combinations
from utils.io_utils import get_subjects_from_folders
from utils.pipeline import run_bids_pipeline
from utils.cleanup import update_all_channels_with_impedance, delete_redundant_captrak_files


def main(clean_up=True):
    
    # identify subjects with data to convert to BIDS
    subjects = get_subjects_from_folders(raw_root)
    
    # BIDS conversion
    for session, task, acquisition in session_combinations:
        run_bids_pipeline(
            raw_root=raw_root, bids_root=bids_root, subjects=subjects, session=session, task=task, acquisition=acquisition
        )
    
    # optional: copy impedance information for space-CapTrak files to channels.tsv
    #           and delete now redundant CapTrak files
    if clean_up:
        update_all_channels_with_impedance(bids_root=bids_root)
        delete_redundant_captrak_files(bids_root, dry_run=False)

    # display the dataset description
    dataset_description_path = os.path.join(bids_root, "dataset_description.json")
    with open(dataset_description_path, "r", encoding = "utf-8") as fid:
        pprint(json.load(fid))
        
if __name__ == "__main__":
    main(clean_up=True)
