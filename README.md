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

## References  
For more information on the EEG BIDS format, see the online documentation:  
https://bids-specification.readthedocs.io/en/stable/modality-specific-files/electroencephalography.html  

and the original publications describing the EEG BIDS format:  

Appelhoff, S., Sanderson, M., Brooks, T., Vliet, M., Quentin, R., Holdgraf, C., Chaumon, M., Mikulan, E., Tavabi, K., Höchenberger, R., Welke, D., Brunner, C., Rockhill, A., Larson, E., Gramfort, A. and Jas, M. (2019). MNE-BIDS: Organizing electrophysiological data into the BIDS format and facilitating their analysis. Journal of Open Source Software 4: (1896). https://doi.org/10.21105/joss.01896  

Pernet, C. R., Appelhoff, S., Gorgolewski, K. J., Flandin, G., Phillips, C., Delorme, A., Oostenveld, R. (2019). EEG-BIDS, an extension to the brain imaging data structure for electroencephalography. Scientific Data, 6, 103. https://doi.org/10.1038/s41597-019-0104-8  