"""
Management of bad channels

Author: 
    Johannes Julius Mohn

Contact:
    johannes.j.mohn@maxplanckschools.de
    
Created:
    2026-03-31

Description:
    Helper script for bad channel annotation
    
    Accesses channels.tsv files in the BIDS directory and changes channel
    status and status description for reproducible annotation of bad channels.
    
General Notes:
    - Make sure you are working from the right environment. If using Spyder:
      Preferences → Python Interpreter
    - Better even, create a dedicated mne/mne_bids environment and start spyder
      from the console.
    - In Spyder, first, set the working directory to your project folder.
    - Study parameters are in the config.py file at the project root.
    - mne_bids.inspect_dataset() can be used to interactively explore the raw
      data and toggle the channel status (bad/good) on the channel traces. The
      user will be prompted whether chages should be saved upon closing of the
      main window. This will also update the sidecar files. Note that applying
      viewing filters can make visual data inspection easier.
      For example: mne_bids.inspect_dataset(bids_path, l_freq=1.0, h_freq=30.0)
    
Specific Notes on Bad Channel Marking:
    - Information on bad channels relies largely on previous manual checks.
    - Bad impedances can be identified automatically using
      mark_high_impedance_channels().
      This identifies all channels with an impedance higher than the set
      threshold and marks them as "out of bound" in the channels.tsv files.
      ATTENTION: Relies on having copied impedance information into the
      channels.tsv files during BIDS creation!
    - mark_bad_channels() is a wrapper for mne_bids.mark_channels() and can be
      used to mark channels as bad in the channels.tsv of a BIDS structure.
      Multiple bad channels can be defined as a list. ch_names=[] resets to blank.
    - reset_all_channel_status() can be used to reset all channel annotations
      across a BIDS directory back to 'good' with empty status_description.
      Use this function very carefully!
      For example: reset_all_channel_status(bids_root=bids_root, dry_run=False)
      Import from utils.qc first!
"""

# %% Libraries and parameters

from pathlib import Path
from config import bids_root
from utils.qc import mark_bad_channels, mark_high_impedance_channels

HIGH_IMP_THRESHOLD = 40

# %% Automatic detection of bad impedances across the BIDS directory

summary = mark_high_impedance_channels(
    bids_root=bids_root,
    impedance_threshold=HIGH_IMP_THRESHOLD,
    dry_run=False
)

# save a summary of high impedance channels to a derivatives directory
output_path = Path(bids_root) / 'derivatives' / 'qc'
output_path.mkdir(parents=True, exist_ok=True)
summary.to_csv(output_path / 'high_impedance_channel_marking_summary.csv', index=False)

# %% Mark bad channels manually

# space to manually annotate bad channels due to reasons other than impedance,
# for example a broken electrode

# sub-2400
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2400",
    bad_ch_names=[
        "P8"
        ],
    bad_ch_descriptions=[
        "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub 2402
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2402",
    bad_ch_names=[
        "P4", "CP6", "CP2", "T8"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2404
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2404",
    bad_ch_names=[
        "C3", "CP1"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2407
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2407",
    bad_ch_names=[
        "Fz", "F3", "F7", "FT9",
        "FC5", "FC1", "C3", "T7",
        "CP5", "CP1", "P3", "P7",
        "O1", "Oz", "O2", "P4",
        "P8", "TP10", "CP6", "CP2",
        "C4", "T8", "FT10", "FC6",
        "FC2", "F4", "F8"
        ],
    bad_ch_descriptions=[
        "excessive bridging", "excessive bridging", "excessive bridging", "excessive bridging",
        "excessive bridging", "excessive bridging", "excessive bridging", "excessive bridging",
        "excessive bridging", "excessive bridging", "excessive bridging", "excessive bridging",
        "excessive bridging", "excessive bridging", "excessive bridging", "excessive bridging",
        "excessive bridging", "excessive bridging", "excessive bridging", "excessive bridging",
        "excessive bridging", "excessive bridging", "excessive bridging", "excessive bridging",
        "excessive bridging", "excessive bridging", "excessive bridging"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2408
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2408",
    bad_ch_names=[
        "P3", "FC2", "F4"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2410
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2410",
    bad_ch_names=[
        "TP9", "P7", "P8", "TP10",
        "FC2"
        ],
    bad_ch_descriptions=[
        "lost contact with scalp", "aberrant channel", "aberrant channel", "aberrant channel",
        "lost contact with scalp"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )


# sub-2411
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2411",
    bad_ch_names=[
        "F7", "FT9", "FC5", "T7",
        "CP5", "P3", "P7", "O1",
        "Oz", "O2", "P4", "P8",
        "CP6", "CP2", "FC6", "F8"
        ],
    bad_ch_descriptions=[
        "excessive bridging", "excessive bridging", "excessive bridging", "excessive bridging",
        "excessive bridging", "excessive bridging", "excessive bridging", "excessive bridging",
        "excessive bridging", "excessive bridging", "excessive bridging", "excessive bridging",
        "excessive bridging", "excessive bridging", "excessive bridging", "excessive bridging"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2412
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2412",
    bad_ch_names=[
        "P8", "TP10", "T8", "FT10"
        ],
    bad_ch_descriptions=[
        "noise", "noise", "noise", "noise"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2413
# no channel exclusions

# sub-2414
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2414",
    bad_ch_names=[
        "FC1", "T8"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2415
# no channel exclusions

# sub-2416
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2416",
    bad_ch_names=[
        "CP1", "TP10", "T8", "FT10",
        "F8"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "physiological artifacts", "aberrant channel", "physiological artifacts",
        "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2417
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2417",
    bad_ch_names=[
        "FC1", "T7"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2418
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2418",
    bad_ch_names=[
        "C4", "F8"
        ],
    bad_ch_descriptions=[
        "lost contact with scalp", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2420
# no channel exclusions

# sub-2422
# no channel exclusions

# sub-2423
# no channel exclusions

# sub-2424
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2424",
    bad_ch_names=[
        "Fp1", "F3", "F7", "FC5",
        "FC1", "T7", "TP9", "CP5",
        "CP1", "P7", "O1", "Oz",
        "O2", "P4", "P8", "TP10",
        "CP6", "T8", "FT10", "FC6",
        "F4", "F8"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2426
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2426",
    bad_ch_names=[
        "TP9", "Oz", "T8", "TP10"
        ],
    bad_ch_descriptions=[
        "lost contact with scalp", "aberrant channel", "aberrant channel", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2429
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2429",
    bad_ch_names=[
        "FT9", "T7", "TP9"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "aberrant channel", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2430
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2430",
    bad_ch_names=[
        "Fz", "F3", "FT9", "FC5",
        "FC1", "T7", "TP9", "CP5",
        "CP1", "P3", "P7", "O1",
        "Oz", "O2", "P4", "P8",
        "TP10", "CP6", "CP2", "C4",
        "T8", "FT10", "FC6"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2431
# no channel exclusions

# sub-2432
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2432",
    bad_ch_names=[
        "FT9", "CP1", "Fp2"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "aberrant channel", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2433
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2433",
    bad_ch_names=[
        "Fp1", "F3", "FC1", "TP9",
        "P8", "TP10"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "bridged with Ref Cz", "bridged with Ref Cz", "aberrant channel",
        "aberrant channel", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2434
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2434",
    bad_ch_names=[
        "TP10"
        ],
    bad_ch_descriptions=[
        "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2436
# no channel exclusions

# sub-2437
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2437",
    bad_ch_names=[
        "FT9", "C3"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2438
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2438",
    bad_ch_names=[
        "TP10"
        ],
    bad_ch_descriptions=[
        "physiological artifacts"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2439
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2439",
    bad_ch_names=[
        "Fz", "F3", "FC1", "C3",
        "CP1", "Pz", "P3", "FC2",
        "F4"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2441
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2441",
    bad_ch_names=[
        "P3", "C4", "FT10", "FC2"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "impedance out of bound", "aberrant channel", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2444
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2444",
    bad_ch_names=[
        "Fp1", "Fp2", "O1"
        ],
    bad_ch_descriptions=[
        "noise", "noise", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2445
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2445",
    bad_ch_names=[
        "Fp1", "TP9", "CP5", "P3",
        "P7", "O2", "TP10", "CP6",
        "T8", "FT10"
        ],
    bad_ch_descriptions=[
        "noise", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "aberrant channel", "aberrant channel", "impedance out of bound", "aberrant channel",
        "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2447
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2447",
    bad_ch_names=[
        "Fp1", "Fp2"
        ],
    bad_ch_descriptions=[
        "noise", "noise"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2449
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2449",
    bad_ch_names=[
        "Fp1", "TP10"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2450
# no channel exclusions

# sub-2451
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2451",
    bad_ch_names=[
        "T7", "TP9", "FT10", "F8"
        ],
    bad_ch_descriptions=[
        "physiological artifacts", "physiological artifacts", "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2452
# no channel exclusions

# sub-2453
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2453",
    bad_ch_names=[
        "TP9"
        ],
    bad_ch_descriptions=[
        "noise"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2454
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2454",
    bad_ch_names=[
        "Fp1", "C3", "F7", "TP10",
        "Fp2"
        ],
    bad_ch_descriptions=[
        "noise", "impedance out of bound", "aberrant channel", "aberrant channel",
        "noise"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2456
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2456",
    bad_ch_names=[
        "Fp1", "Fp2"
        ],
    bad_ch_descriptions=[
        "noise", "noise"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2457
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2457",
    bad_ch_names=[
        "Fp1", "FT9", "TP9", "O2",
        "Fp2"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "aberrant channel", "aberrant channel", "impedance out of bound",
        "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2458
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2458",
    bad_ch_names=[
        "FT9"
        ],
    bad_ch_descriptions=[
        "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2459
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2459",
    bad_ch_names=[
        "Fz", "FC5", "FC1", "C3",
        "CP5", "Pz", "P3", "P7",
        "O1", "Oz", "O2", "CP6",
        "CP2", "C4", "FT10", "FC6",
        "FC2"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "aberrant channel", "impedance out of bound",
        "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2460
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2460",
    bad_ch_names=[
        "Fp1", "TP10", "Fp2"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "aberrant channel", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2461
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2461",
    bad_ch_names=[
        "Fp2"
        ],
    bad_ch_descriptions=[
        "noise"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2463
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2463",
    bad_ch_names=[
        "TP9", "TP10", "FC2"
        ],
    bad_ch_descriptions=[
        "artifacts", "artifacts", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2465
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2465",
    bad_ch_names=[
        "T7", "CP6"
        ],
    bad_ch_descriptions=[
        "lost contact with scalp", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2469
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2469",
    bad_ch_names=[
        "P8"
        ],
    bad_ch_descriptions=[
        "noise"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2474
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2474",
    bad_ch_names=[
        "P7"
        ],
    bad_ch_descriptions=[
        "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2474
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2474",
    bad_ch_names=[
        "P7"
        ],
    bad_ch_descriptions=[
        "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2476
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2476",
    bad_ch_names=[
        "P4", "TP10", "T8"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "aberrant channel", "lost contact with scalp"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2478
# no channel exclusions

# sub-2479
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2479",
    bad_ch_names=[
        "TP9", "F3", "FC1", "F8"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "impedance out of bound", "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2480
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2480",
    bad_ch_names=[
        "FT9", "P7"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2481
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2481",
    bad_ch_names=[
        "F7", "FC5", "FC1", "C3",
        "P3", "CP2", "C4", "FC2"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "aberrant channel", "aberrant channel", "aberrant channel",
        "aberrant channel", "aberrant channel", "aberrant channel", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2482
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2482",
    bad_ch_names=[
        "Fp1"
        ],
    bad_ch_descriptions=[
        "noise"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2483
# no channel exclusions

# sub-2484
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2484",
    bad_ch_names=[
        "F3", "C3", "C4"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "impedance out of bound", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2485
# no channel exclusions

# sub-2486
# no channel exclusions

# sub-2487
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2487",
    bad_ch_names=[
        "P4", "T8", "FC6"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "aberrant channel", "aberrant channel"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2488
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2488",
    bad_ch_names=[
        "F3", "FT9", "FC5", "FC1",
        "C3", "TP9", "CP1", "Oz",
        "CP2", "FC2"
        ],
    bad_ch_descriptions=[
        "aberrant channel", "aberrant channel", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "aberrant channel", "aberrant channel", "impedance out of bound",
        "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2489
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2489",
    bad_ch_names=[
        "P3"
        ],
    bad_ch_descriptions=[
        "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )

# sub-2490
mark_bad_channels(
    bids_root=bids_root,
    subject="sub-2490",
    bad_ch_names=[
        "Fp1", "F3", "F7", "FC5",
        "FC5", "FC1", "C3", "T7",
        "CP5", "P3", "P7", "O1",
        "Oz", "O2", "P4", "P8",
        "TP10", "CP6", "CP2", "C4",
        "T8", "FT10", "FC6", "FC2",
        "F4", "F8", "Fp2"
        ],
    bad_ch_descriptions=[
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound", "impedance out of bound",
        "impedance out of bound", "impedance out of bound", "impedance out of bound"
        ],
    ch_status="bad",
    session="m1",
    task="sl"
    )
