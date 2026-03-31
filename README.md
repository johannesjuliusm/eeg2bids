# EEG to BIDS conversion

## Automated creation of BIDS data structure with meta data for the Memobaby Study.

Author: Johannes Julius Mohn  
Contact: johannes.j.mohn@maxplanckschools.de  
Date created: 2026-03-26  
License: BSD-3-Clause  
The study: https://www.sfb1315.de/research/b04/  

## Description  
This pipeline transforms raw EEG data from source to BIDS structure.  
The core pipeline BIDSifies data, copies image files (not natively part of BIDS), updates .json sidecars with  
study-specific info, creates exceptions for non-BIDS data types included in this study (.bidsignore file),  
creates a study description file, displays updated directory trees for each new subject, and finally displays  
the study info.  

## Important user notes
- MNE Python and MNE BIDS libraries must be installed.  
- Ideally, create a dedicated MNE environment and start your IDE (e.g., spyder) from the console.  
- Set study parameters (folder paths, study name, tasks, authors, etc.) in the config.py file at the project root.  
- If adapting this workflow for your EEG study, primarily change the config.py file and make appropriate changes  
  inside the update_json_sidecar function to reflect your task(s). Optionally, update migrate_image_files if you  
  have image data other than .png or if this does not apply.  
- Subject IDs should be in format sub-XXXX or adjust get_subjects_from_folders accordingly.  