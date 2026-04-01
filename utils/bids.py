import os
from pathlib import Path
import shutil
from mne.io import read_raw_brainvision
from mne_bids import (
    find_matching_paths,
    write_raw_bids,
    BIDSPath,
    print_dir_tree,
    update_sidecar_json
)
from config import sidecar_entries, task_info_sl, task_info_mem


def parse_bids_filename(path):
    """
    Parse BIDS entities from a filename stem.

    Examples
    --------
    sub-001_ses-01_task-sl_eeg.tsv
    sub-001_ses-01_space-Captrak_electrodes.tsv
    """
    stem = path.stem
    parts = stem.split('_')

    entities = {}
    suffix = None

    for part in parts:
        if '-' in part:
            key, value = part.split('-', 1)
            entities[key] = value
        else:
            suffix = part

    entities['suffix'] = suffix
    return entities


def update_json_sidecar(entries, bids_root, subject,
                        session=None, task=None, acquisition=None,
                        file_extension='.vhdr'):
    """
    Update .json sidecar files to reflect study-specific information.
    """
    print(f"\nUpdating the .json sidecar for session '{session}', task '{task}', acquisition '{acquisition}' ...\n")

    if entries is None:
        raise ValueError("'entries' must be a dictionary, not None.")

    if not os.path.exists(bids_root):
        raise FileNotFoundError(f"BIDS parent directory '{bids_root}' not found.")

    if task == 'mem':
        entries.update(task_info_mem)
    elif task == 'sl':
        entries.update(task_info_sl)
    else:
        raise ValueError(f"Unknown task: {task}")

    current_path = os.path.join(bids_root, subject)

    if not os.path.exists(current_path):
        raise FileNotFoundError('The .json sidecar does not exist.')

    try:
        sub_id = subject.replace('sub-', '')

        bids_path_to_update = find_matching_paths(
            bids_root,
            subjects=sub_id,
            sessions=session,
            tasks=task,
            acquisitions=acquisition,
            extensions=file_extension
        )

        if not bids_path_to_update:
            raise FileNotFoundError('No matching BIDS paths found.')

        sidecar_path = bids_path_to_update[0].copy()
        sidecar_path.update(extension='.json')

        update_sidecar_json(bids_path=sidecar_path, entries=entries)

    except Exception as e:
        print(f'An error occurred: {e}')


def migrate_image_files(raw_root, bids_root, subject=None, session=None, task=None, acquisition=None, datatype='eeg'):
    """
    Copy image files from rawdata structure to BIDS folder.

    Note that images are not usually part of the BIDS structure except for
    pictures taken of fiducial points and landmarks on the head and face.
    Images should have a "_photo" suffix to make them conform with BIDS.

    Parameters
    ----------
    raw_root : path-like
        The full path to the raw data.
    bids_root : path-like
        The full path to the bids parent directory.
    subject : str, optional
        Subject identifier. The default is None.
    session : str, optional
        Session identifier. The default is None.
    task : str, optional
        Task identifier. The default is None.
    acquisition : str, optional
        Acquisition identifier. The default is None.
    datatype : str, optional
        Datatype identifier. The default is 'eeg'.

    Raises
    ------
    FileNotFoundError
        If `raw_root` or `bids_root` directories do not exist.
    IOError
        If file copying fails.

    Returns
    -------
    None.
    """
    print("\nMigrating image files ...\n")
    
    allowed_extensions = {'.png', '.jpg', '.jpeg'}
    
    # validate parameters
    if not os.path.exists(raw_root):
        raise FileNotFoundError(f"Raw data directory '{raw_root}' not found.")
    if not os.path.exists(bids_root):
        raise FileNotFoundError(f"BIDS parent directory '{bids_root}' not found.")
    
    sub_value = subject.replace('sub-', '') if subject is not None else None
    ses_value = session.replace('ses-', '') if session is not None else None
    acq_value = acquisition.replace('acq-', '') if acquisition is not None else None

    # define paths
    dir_raw_data = os.path.join(raw_root, subject)
    dir_new_bids = os.path.join(
        bids_root,
        subject,
        f"ses-{ses_value}" if ses_value is not None else '',
        datatype
    )
    os.makedirs(dir_new_bids, exist_ok=True)
    
    # validate source directory
    if not os.path.exists(dir_raw_data):
        raise FileNotFoundError(f"Raw data directory for subject '{subject}' not found.")

    # find image files matching the criteria
    png_files = []
    
    for f in os.listdir(dir_raw_data):
        ext = Path(f).suffix.lower()
        if ext not in allowed_extensions:
            continue
    
        entities = parse_bids_filename(Path(f))
    
        if sub_value is not None and entities.get('sub') != sub_value:
            continue
    
        if ses_value is not None and entities.get('ses') != ses_value:
            continue
    
        if task is not None and entities.get('task') != task:
            continue
    
        if acq_value is not None and entities.get('acq') != acq_value:
            continue
    
        png_files.append(f)
    
    # copy image files
    for png_file in png_files:
        
        source_path = os.path.join(dir_raw_data, png_file)
        
        # rename photo to make sure end in suffix "_photo"
        base, ext = os.path.splitext(f)
        ext = ext.lower()
        
        if not base.endswith('_photo'):
            target_name = f'{base}_photo{ext}'
        else:
            target_name = f
        
        target_path = os.path.join(dir_new_bids, target_name)
        try:
            shutil.copyfile(source_path, target_path)
            print(f"Copied '{source_path}' to '{target_path}'")
        except IOError as e:
            raise IOError(f"Failed to copy '{source_path}' to '{target_path}': {e}")


def convert_to_bids(raw_root, bids_root, subjects,
                    session=None, task=None, acquisition=None, datatype='eeg',
                    sidecar_entries=sidecar_entries):
    """
    Converts new eeg datasets to BIDS format.
    
    Parameters
    ----------
    raw_root : path-like
        The full path to the raw data.
    bids_root : path-like
        The full path to the bids parent directory.
    subjects : list
        List of subject identifiers.
    session : str, optional
        Session identifier. The default is None.
    task : str, optional
        Task identifier. The default is None.
    acquisition : str, optional
        Acquisition identifier. The default is None.
    datatype : str, optional
        Datatype identifier. The default is 'eeg'.

    Returns
    -------
    str
        A message indicating the success of the file conversion.
    """
    # check if subjects list is empty or not defined and exit if True
    if not subjects:
        print("No subjects specified. Exiting the script ...")
        return
    
    print(f"\nConverting raw data to BIDS for {len(subjects)} specified subjects ...\n")
    
    for i, subject in enumerate(subjects):
        
        # get subject id
        sub_id = subject.replace("sub-", "")
        print(f"\nWorking on {subject} ({i+1}/{len(subjects)}) ...\n")
        
        # path to subject data
        dir_raw_data = os.path.join(raw_root, subject)
        print(f"The raw EEG data is in '{dir_raw_data}'")
        print(f"BIDS folder for {subject} will be created in '{bids_root}'\n")
        
        # define data access
        file_extension = ".vhdr"

        components = [("ses", session), ("task", task), ("acq", acquisition)]
        # filter out None values and join the non-None components with prefixes
        bids_string = "".join(f"_{prefix}-{value}" for prefix, value in components if value is not None)
        bids_string += f"_{datatype}"
        
        file_name = subject + bids_string + file_extension
        file_path = os.path.join(dir_raw_data, file_name)
    
        if os.path.exists(file_path):
            try:
                # load data
                raw_data = read_raw_brainvision(file_path, preload=False)
                
                # add information on line noise and inspect meta data
                raw_data.info["line_freq"] = 50  # specify power line frequency as required by BIDS
            
                # write the bids data
                bids_path = BIDSPath(
                    subject=sub_id, session=session, task=task, acquisition=acquisition, datatype=datatype, root=bids_root
                )
                print(f"\nWriting BIDS directory '{bids_path}'\n")
                write_raw_bids(raw_data, bids_path, overwrite=True)
                
                # copy PNG files via custom function
                migrate_image_files(
                    raw_root=raw_root, bids_root=bids_root, subject=subject, session=session, task=task, acquisition=acquisition
                )
                
                # update the .json sidecar file via custom function
                update_json_sidecar(
                    entries=sidecar_entries, bids_root=bids_root, subject=subject, session=session, task=task, acquisition=acquisition
                    )
                
                # visualize the new BIDS directory tree
                print(f"\nThis is the new BIDS directory for {subject}:\n")
                print_dir_tree(os.path.join(bids_root, subject))
                
                # check if this is the last subject
                if i != len(subjects) - 1:
                    # continue with next subject
                    input(f"\nPress <Enter> to convert the next subject ({i+2}/{len(subjects)}) to BIDS\n")
                else:
                    print("\nAll subjects have been processed.")
                
            except Exception as e:
                print(f"An error occurred: {e}")
                
        else:
            print(f"'{file_name}' does not exist.")
            
            # check if this is the last subject
            if i != len(subjects) - 1:
                # continue with next subject
                input(f"\nPress <Enter> to convert the next subject ({i+2}/{len(subjects)}) to BIDS\n")
            else:
                print("\nAll subjects have been processed.")
            
    print("\n>>>Data for all subjects have been converted.<<<\n")


def create_bidsignore(bids_root, content="**/*.png", overwrite=True):
    """
    Create a .bidsignore file at the top of the BIDS folder hierarchy,
    which specifies file types not supported by BIDS which should be ignored
    when validating the BIDS directory.
    
    Parameters
    ----------
    bids_root : path-like
        The full path to the bids parent directory.
    content : str, optional
        The content to be written to the .bidsignore file. Follows .gitignore conventions.
        The default is "**/*.png".
    overwrite : bool, optional
        Whether any existing .bidsignore should be overwritten. The default is True.

    Raises
    ------
    FileNotFoundError
        If the bids_root directory does not exist.
    PermissionError
        If there are permission issues when writing the .bidsignore.

    Returns
    -------
    str
        A message indicating the status of .bidsignore file creation.
    """
    if not os.path.exists(bids_root):
        raise FileNotFoundError(f"The directory {bids_root} does not exist.")
        
    bidsignore_path = os.path.join(bids_root, ".bidsignore")
    
    if os.path.exists(bidsignore_path) and not overwrite:
        return "Operation aborted. .bidsignore file already exists and overwrite is set to False."
    
    try:
        with open(bidsignore_path, "w") as bidsignore_file:
            bidsignore_file.write(content)
    except PermissionError as e:
        raise PermissionError(f"Permission error: {e}")
    else:
        print(f".bidsignore file created with content:\n'{content}'\n")
