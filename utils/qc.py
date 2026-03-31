import os
from pathlib import Path
import pandas as pd

from mne_bids import (
    BIDSPath,
    read_raw_bids,
    mark_channels
)


def parse_bids_entities_from_filename(path):
    """
    Extract common BIDS entities from a filename.

    Parameters
    ----------
    path : str or pathlib.Path
        Path to a BIDS file.

    Returns
    -------
    dict
        Dictionary with parsed BIDS entities, e.g. sub, ses, task, acq.
    """
    path = Path(path)
    stem = path.name

    # remove known suffixes
    if stem.endswith('.tsv'):
        stem = stem[:-4]
    elif stem.endswith('.json'):
        stem = stem[:-5]

    parts = stem.split('_')

    entities = {}
    for part in parts:
        if '-' in part:
            key, value = part.split('-', 1)
            entities[key] = value

    return entities


def mark_bad_channels(bids_root, subject, bad_ch_names, bad_ch_descriptions=None, ch_status='bad', session=None, task=None, acquisition=None, run=None, datatype='eeg'):
    """
    Mark bad channels in the channels.tsv of a defined BIDS structure.
    This function is a wrapper for mne_bids.mark_channels().
    It uses mne_bids.BIDSPath() to define access to the eeg data saved in BIDS
    and marks defined channels as bad using mne_bids.mark_channels().
    For more information, see the official mne_bids documentation.
    
    Parameters
    ----------
    bids_root : path-like
        Path to where the EEG data is stored in BIDS.
    subject : str
        Subject identifier. If provided with the 'sub-' prefix, will be handled internally.
    bad_ch_names : str | list of str
        Channel name(s) to mark.
    bad_ch_descriptions : str | list of str, optional
        Descriptions of why the channels are bad. Must be same length as bad_ch_names
    ch_status : str
        Status to mark selected channels as: 'good' or 'bad'. The default is 'bad'.
        This status is applied to all listed channels.
    session : str, optional
        Session identifier. The default is None.
    task : str, optional
        Task identifier. The default is None.
    acquisition : str, optional
        Acquisition identifier. The default is None.
    run : str, optional
        Run number. The default is None.
    datatype : str, optional
        Datatype identifier. The default is 'eeg'.
        
    Raises
    ------
    FileNotFoundError
        If the bids_root directory does not exist.

    Returns
    -------
    None.
    """
    # validate parameters
    if not os.path.exists(bids_root):
        raise FileNotFoundError(f"BIDS parent directory '{bids_root}' not found.")
        
    # get subject id
    sub_id = subject.replace("sub-", "")

    # define data to read
    bids_path = BIDSPath(
        subject=sub_id,
        session=session,
        task=task,
        acquisition=acquisition,
        datatype=datatype,
        root=bids_root,
        )

    # read the data
    raw = read_raw_bids(bids_path=bids_path, verbose=False)

    # read bad channels
    bads = raw.info["bads"]
    
    print(
        f"\n{subject}: The following channels are currently marked as bad:\n"
        f'    {", ".join(bads) if bads else "none"}'
    )
    
    # mark channels as bad and save to the channels.tsv
    mark_channels(bids_path=bids_path,
                  ch_names=bad_ch_names,
                  status=ch_status,
                  descriptions=bad_ch_descriptions,
                  verbose=False)
    
    raw = read_raw_bids(bids_path=bids_path, verbose=False)
    print(
        f"{subject}: Updated bad channels list:\n"
        f'    {", ".join(raw.info["bads"])}\n'
    )


def mark_high_impedance_channels(
    bids_root,
    impedance_threshold,
    dry_run=True,
    status_description='impedance out of bound',
    only_if_not_already_bad=True,
    verbose=True
):
    """
    Mark high-impedance channels as bad across a BIDS dataset.

    This function scans all *_channels.tsv files, identifies channels with
    impedance above the specified threshold, and calls mark_bad_channels()
    with the appropriate BIDS entities.

    Parameters
    ----------
    bids_root : str or pathlib.Path
        Root of the BIDS dataset.
    impedance_threshold : float
        Channels with impedance greater than this value are marked bad.
    dry_run : bool, default=True
        If True, only report what would be changed and do not modify files.
    status_description : str, default='impedance out of bound'
        Description to assign to marked bad channels.
    only_if_not_already_bad : bool, default=True
        If True, skip channels whose current status is already 'bad'.
    verbose : bool, default=True
        If True, print progress information.

    Returns
    -------
    pandas.DataFrame
        Summary table with one row per processed channels.tsv file.
    """
    bids_root = Path(bids_root)

    if not bids_root.exists():
        raise FileNotFoundError(f'BIDS root does not exist: {bids_root}')

    channels_files = sorted(bids_root.rglob('*_channels.tsv'))

    if not channels_files:
        raise FileNotFoundError(f'No *_channels.tsv files found in: {bids_root}')

    summary_rows = []

    for channels_path in channels_files:
        row = {
            'channels_file': str(channels_path),
            'subject': None,
            'session': None,
            'task': None,
            'acquisition': None,
            'n_channels_total': None,
            'n_channels_above_threshold': 0,
            'bad_channels': '',
            'action': 'skipped',
            'reason': ''
        }

        try:
            df = pd.read_csv(channels_path, sep='\t')
            row['n_channels_total'] = len(df)

            required_cols = {'name', 'impedance'}
            missing_cols = required_cols.difference(df.columns)
            if missing_cols:
                row['reason'] = f'missing required columns: {sorted(missing_cols)}'
                summary_rows.append(row)
                if verbose:
                    print(f"Skipping {channels_path.name}: {row['reason']}")
                continue

            # make impedance numeric
            df['impedance'] = pd.to_numeric(df['impedance'], errors='coerce')

            # start with high-impedance channels
            bad_df = df[df['impedance'] > impedance_threshold].copy()

            # optionally exclude channels already marked bad
            if only_if_not_already_bad and 'status' in df.columns:
                bad_df = bad_df[bad_df['status'].fillna('').str.lower() != 'bad']

            row['n_channels_above_threshold'] = len(bad_df)

            if bad_df.empty:
                row['action'] = 'none'
                row['reason'] = 'no channels above threshold'
                summary_rows.append(row)
                if verbose:
                    print(f"No high-impedance channels in {channels_path.name}")
                continue

            bad_ch_names = bad_df['name'].astype(str).tolist()
            bad_ch_descriptions = [status_description] * len(bad_ch_names)

            entities = parse_bids_entities_from_filename(channels_path)
            subject = entities.get('sub')
            session = entities.get('ses')
            task = entities.get('task')
            acquisition = entities.get('acq')

            row['subject'] = f'sub-{subject}' if subject else None
            row['session'] = session
            row['task'] = task
            row['acquisition'] = acquisition
            row['bad_channels'] = ', '.join(bad_ch_names)

            if subject is None:
                row['action'] = 'skipped'
                row['reason'] = 'no subject entity found in filename'
                summary_rows.append(row)
                if verbose:
                    print(f"Skipping {channels_path.name}: {row['reason']}")
                continue

            if dry_run:
                row['action'] = 'dry_run'
                row['reason'] = 'no file modified'
                if verbose:
                    print(
                        f"[DRY RUN] {channels_path.name} -> "
                        f"{', '.join(bad_ch_names)}"
                    )
            else:
                mark_bad_channels(
                    bids_root=bids_root,
                    subject=f'sub-{subject}',
                    bad_ch_names=bad_ch_names,
                    bad_ch_descriptions=bad_ch_descriptions,
                    ch_status='bad',
                    session=session,
                    task=task,
                    acquisition=acquisition
                )
                row['action'] = 'marked'
                row['reason'] = 'channels marked bad'
                if verbose:
                    print(
                        f"Marked high impedance channels in {channels_path.name}:\n"
                        f"    {', '.join(bad_ch_names)}\n"
                    )

            summary_rows.append(row)

        except Exception as e:
            row['action'] = 'error'
            row['reason'] = str(e)
            summary_rows.append(row)
            if verbose:
                print(f"Error processing {channels_path.name}: {e}")

    summary_df = pd.DataFrame(summary_rows)

    if verbose:
        print('\nSummary:')
        print(summary_df['action'].value_counts(dropna=False))

    return summary_df


def reset_all_channel_status(
    bids_root,
    dry_run=True,
    verbose=True
):
    """
    Reset all channel status entries to 'good' and clear status_description
    in all *_channels.tsv files in a BIDS dataset.

    Parameters
    ----------
    bids_root : str or Path
        Root of the BIDS dataset.
    dry_run : bool, default=True
        If True, only report what would be changed.
    verbose : bool, default=True
        If True, print progress.

    Returns
    -------
    pandas.DataFrame
        Summary of processed files.
    """
    bids_root = Path(bids_root)

    if not bids_root.exists():
        raise FileNotFoundError(f'BIDS root does not exist: {bids_root}')

    channels_files = sorted(bids_root.rglob('*_channels.tsv'))
    summary_rows = []

    for channels_path in channels_files:
        row = {
            'channels_file': str(channels_path),
            'n_channels': None,
            'action': 'skipped',
            'reason': ''
        }

        try:
            df = pd.read_csv(channels_path, sep='\t')
            row['n_channels'] = len(df)

            if 'status' not in df.columns:
                df['status'] = 'good'
            else:
                df['status'] = 'good'

            if 'status_description' not in df.columns:
                df['status_description'] = ''
            else:
                df['status_description'] = ''

            if dry_run:
                row['action'] = 'dry_run'
                row['reason'] = 'no file modified'
                if verbose:
                    print(f'[DRY RUN] Would reset {channels_path.name}')
            else:
                df.to_csv(channels_path, sep='\t', index=False)
                row['action'] = 'reset'
                row['reason'] = 'status set to good and status_description cleared'
                if verbose:
                    print(f'Reset {channels_path.name}')

        except Exception as e:
            row['action'] = 'error'
            row['reason'] = str(e)
            if verbose:
                print(f'Error processing {channels_path.name}: {e}')

        summary_rows.append(row)

    summary_df = pd.DataFrame(summary_rows)

    if verbose:
        print('\nSummary:')
        print(summary_df['action'].value_counts(dropna=False))

    return summary_df
