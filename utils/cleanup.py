from pathlib import Path
import pandas as pd


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


def find_matching_electrodes_file(channels_path, electrodes_files):
    """
    Find the best matching Captrak electrodes.tsv for one channels.tsv.

    Matching priority:
    - same subject
    - same session (if present)
    - same acquisition (if present)
    """
    ch_entities = parse_bids_filename(channels_path)

    candidates = []
    for elec_path in electrodes_files:
        elec_entities = parse_bids_filename(elec_path)

        if elec_entities.get('sub') != ch_entities.get('sub'):
            continue

        if elec_entities.get('ses') != ch_entities.get('ses'):
            continue

        if elec_entities.get('acq') != ch_entities.get('acq'):
            continue

        candidates.append(elec_path)

    if len(candidates) == 0:
        raise FileNotFoundError(
            f'No matching electrodes.tsv found for {channels_path.name}'
        )

    if len(candidates) > 1:
        raise RuntimeError(
            f'Ambiguous match for {channels_path.name}: '
            f'{[p.name for p in candidates]}'
        )

    return candidates[0]


def get_column_case_insensitive(df, candidates):
    """
    Return the first matching column name from candidates, case-insensitive.
    """
    lower_map = {col.lower(): col for col in df.columns}

    for candidate in candidates:
        if candidate.lower() in lower_map:
            return lower_map[candidate.lower()]

    raise KeyError(f'None of these columns found: {candidates}')


def add_impedance_to_channels(channels_path, electrodes_path, overwrite=True):
    """
    Add impedance values from electrodes.tsv into channels.tsv.

    Assumptions
    -----------
    - channels.tsv has a channel-name column, usually 'name'
    - electrodes.tsv has a name column and an impedance column
    """
    channels_df = pd.read_csv(channels_path, sep='\t')
    electrodes_df = pd.read_csv(electrodes_path, sep='\t')

    ch_name_col = get_column_case_insensitive(channels_df, ['name'])
    elec_name_col = get_column_case_insensitive(electrodes_df, ['name'])
    elec_imp_col = get_column_case_insensitive(
        electrodes_df,
        ['impedance', 'impedances', 'imp', 'electrode_impedance']
    )

    impedance_map = (
        electrodes_df[[elec_name_col, elec_imp_col]]
        .dropna(subset=[elec_name_col])
        .drop_duplicates(subset=[elec_name_col])
        .assign(**{
            elec_name_col: lambda df: df[elec_name_col].astype(str).str.strip()
        })
        .set_index(elec_name_col)[elec_imp_col]
        .to_dict()
    )
    
    # delete impedance column from the CapTrak file
    if elec_imp_col in electrodes_df.columns:
        electrodes_df.drop(columns=[elec_imp_col], inplace=True)
        electrodes_df.to_csv(electrodes_path, sep='\t', index=False)

    channels_df[ch_name_col] = channels_df[ch_name_col].astype(str).str.strip()
    
    # map impedance
    impedance_values = channels_df[ch_name_col].map(impedance_map)
    
    # remove existing column if present (safe for reruns)
    if 'impedance' in channels_df.columns:
        channels_df.drop(columns=['impedance'], inplace=True)
        
    # insert before 'status'
    if 'status' in channels_df.columns:
        insert_idx = channels_df.columns.get_loc('status')
    else:
        insert_idx = len(channels_df.columns)
        
    channels_df.insert(insert_idx, 'impedance', impedance_values)

    if overwrite:
        channels_df.to_csv(channels_path, sep='\t', index=False)

    return channels_df


def update_all_channels_with_impedance(bids_root):
    """
    Update all channels.tsv files in a BIDS dataset with impedance values
    from matching space-Captrak_electrodes.tsv files.
    """
    bids_root = Path(bids_root)
    
    print("\nMoving impedance information to _channels.tsv files ...\n")

    channels_files = sorted(bids_root.rglob('*_channels.tsv'))
    electrodes_files = sorted(bids_root.rglob('*space-CapTrak_electrodes.tsv'))

    if not channels_files:
        raise FileNotFoundError('No *_channels.tsv files found.')

    if not electrodes_files:
        raise FileNotFoundError('No *space-Captrak_electrodes.tsv files found.')

    results = []

    for channels_path in channels_files:
        try:
            electrodes_path = find_matching_electrodes_file(
                channels_path,
                electrodes_files
            )

            updated_df = add_impedance_to_channels(
                channels_path,
                electrodes_path,
                overwrite=True
            )

            n_missing = updated_df['impedance'].isna().sum()

            results.append({
                'channels_file': str(channels_path),
                'electrodes_file': str(electrodes_path),
                'n_rows': len(updated_df),
                'n_missing_impedance': int(n_missing),
                'status': 'ok'
            })

        except Exception as e:
            results.append({
                'channels_file': str(channels_path),
                'electrodes_file': None,
                'n_rows': None,
                'n_missing_impedance': None,
                'status': f'error: {e}'
            })

    return pd.DataFrame(results)


def delete_redundant_captrak_files(bids_root, dry_run=True):
    """
    Delete redundant CapTrak files while keeping the shortest-named file in each
    folder for both:
    - *space-Captrak_electrodes.tsv
    - *space-Captrak_coordinatesystem.json

    Parameters
    ----------
    bids_root : str or Path
        Root of the BIDS dataset.
    dry_run : bool, default=True
        If True, only report what would be deleted.

    Returns
    -------
    list of dict
        Summary of kept and deleted files.
    """
    bids_root = Path(bids_root)
    
    print("\nDeleting redundant CapTrak files ...\n")

    patterns = [
        '*space-CapTrak_electrodes.tsv',
        '*space-CapTrak_coordsystem.json'
    ]

    results = []

    for pattern in patterns:
        files = sorted(bids_root.rglob(pattern))

        # group by parent folder
        groups = {}
        for path in files:
            groups.setdefault(path.parent, []).append(path)

        for folder, folder_files in groups.items():
            if len(folder_files) == 1:
                results.append({
                    'file_type': pattern,
                    'folder': str(folder),
                    'kept': str(folder_files[0]),
                    'deleted': []
                })
                continue

            # keep shortest filename, break ties alphabetically
            folder_files_sorted = sorted(
                folder_files,
                key=lambda p: (len(p.name), p.name)
            )

            keep_file = folder_files_sorted[0]
            delete_files = folder_files_sorted[1:]

            if not dry_run:
                for file_path in delete_files:
                    file_path.unlink()

            results.append({
                'file_type': pattern,
                'folder': str(folder),
                'kept': str(keep_file),
                'deleted': [str(p) for p in delete_files]
            })

    return results
