from mne_bids import make_dataset_description
from utils.io_utils import query_yes_no, some_fun_first
from utils.bids import convert_to_bids, create_bidsignore
from config import (
    datatype, bidsignore_content,
    study_name, authors, acknowledgements_1, acknowledgements_2,
    data_license_type, ethics, funding, references_and_links,
    ASCII_ART_PATH
    )


def run_bids_pipeline(raw_root, bids_root, subjects, session, task, acquisition):
    """
    Ask user to confirm script execution upon checking of parameters.
    
    Parameters
    ----------
    raw_root : path-like
        The full path to the raw data.
    bids_root : path-like
        The full path to the BIDS parent directory.
    subjects : list
        List of subject identifiers.
    session : str
        Session identifier.
    task : str
        Task identifier.
    acquisition : str
        Acquisition identifier.

    Returns
    -------
    str
        Message indicating the status of the pipeline execution.
    """
    # but first, some fun
    some_fun_first(ASCII_ART_PATH)
    
    # start question that summarizes the script specifications
    start_question = (
        f"\nGetting ready to convert {datatype} data of {len(subjects)} subjects to BIDS.\n"
        f"Specified session is '{session}' ; specified task is '{task}' ; specified acquisition is '{acquisition}'.\n\n"
        "Continue?"
    )
    
    # ask for user input
    if query_yes_no(start_question):
        try:
            # BIDSify data, copy image files, update .json sidecars with study-specific info
            convert_to_bids(raw_root, bids_root, subjects, session, task, acquisition)
            
            # create exceptions for non-BIDS data types included in this study
            create_bidsignore(bids_root=bids_root, content=bidsignore_content, overwrite=True)
            
            # create a study description file
            make_dataset_description(
                path = bids_root,
                name = study_name,
                authors = authors,
                how_to_acknowledge = acknowledgements_1,
                acknowledgements = acknowledgements_2,
                data_license = data_license_type,
                ethics_approvals = ethics,
                funding = funding,
                references_and_links = references_and_links,
                doi = None,
                overwrite = True,
            )
            
        except Exception as e:
            print(f"An error occurred during pipeline execution: {e}")
    else:
        print("\nPipeline execution aborted by user.\n")
