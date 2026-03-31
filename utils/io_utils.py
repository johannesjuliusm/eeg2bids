import sys


def query_yes_no(question, default="yes"):
    """
    Ask a yes/no question via raw_input() and return the answer.
    
    Parameters
    ----------
    question : str
        A string that is presented to the user.

    Raises
    ------
    ValueError
        If the default answer is specified incorrectly.

    Returns
    -------
    choice : bool
        The choice return value is True for "yes" or False for "no".
    """
    
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)
    
    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'y' or 'n' " "(or 'yes' or 'no').\n")


import os


def get_subjects_from_folders(raw_root):
    """
    Get a list of subjects from their BIDS-conforming folder names within the 
    directory where raw data is saved.

    Parameters
    ----------
    raw_root : path-like
        The full path to the raw data.

    Raises
    ------
    FileNotFoundError
        If the raw_root directory does not exist.
    NotADirectoryError
        If raw_root is not a directory.
    ValueError
        If no folders with the pattern 'sub-XXXX' exist.

    Returns
    -------
    subjects : list
        A list of subject identifiers.
    """
    print("\nGathering subject identifiers from folders ...\n")
    
    # validate parameters
    if not os.path.exists(raw_root):
        raise FileNotFoundError(f"The directory {raw_root} does not exist.")
    if not os.path.isdir(raw_root):
        raise NotADirectoryError(f"{raw_root} is not a directory.")
    
    subjects = [folder_name for folder_name in os.listdir(raw_root) if folder_name.startswith("sub-") and os.path.isdir(os.path.join(raw_root, folder_name))]
    print(f"Found {len(subjects)} subjects:\n" + "\n".join(subjects))
    
    if not subjects:
        raise ValueError("No folders named 'sub-xxxx' found. Check your raw data file structure or rename accordingly.")
    
    return subjects


def some_fun_first(file_path):
    """
    Make the pipeline more fun to execute. Best, JJ.
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            print(f.read())
    except FileNotFoundError:
        print("Good luck, have fun, don't die.")