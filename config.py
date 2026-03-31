import os


# directories
#raw_root = "/Users/jjm/sci/memobaby/data/newdata"
#bids_root = "/Users/jjm/sci/memobaby/data/rawdata"
raw_root = "/Users/jjm/Desktop/newdata"
bids_root = "/Users/jjm/Desktop/rawdata"


# define bids information
# sessions, tasks, acquisitions
session_combinations = [
    ("m1", "sl", None),
    ("m12", "sl", None),
    ("m12", "mem", "learn"),
    ("m12", "mem", "recall"),
    ("m1", "rest", None),
    ("m12", "rest", None)
]
datatype = 'eeg'


# define content of the .bidsignore file
bidsignore_content = "**/*.png\n**/*.xlsx"


# define the .json sidecar update as a dictionary
# this update cannot be undone easily; make sure the entries are defined with the proper fields
sidecar_entries = {
    "EEGReference": "Cz",
    "EEGGround": "Single electrode placed on FPz",
    "InstitutionName": "Charité – Universitätsmedizin Berlin, Germany",
    "InstitutionalDepartmentName": "Institute of Medical Psychology",
    "InstitutionAddress": "Luisenstr. 57, 10117 Berlin, Germany",
    "Manufacturer": "Brain Products",
    "ManufacturersModelName": "actiCHamp Plus",
    "CapManufacturer": "EasyCap",
    "CapManufacturersModelName": "actiCAP snap 32",
    "SoftwareVersions": "BrainVision Recorder"
    }

task_info_sl = {
    "TaskName": "Statistical Learning",
    "TaskDescription": """\
This task was adapted from Saffran et al. (1996) and Choi et al. (2020). \
Auditory playback of 12 Malay syllables concatenated into 4 tri-syllabic pseudowords. \
Block design with 5 blocks: Resting state pre (2min), random playback of syllables (2min), \
structured playback of syllables as pseudowords (7min), \
random playback of syllables (2min), resting state post (2min).\
""",
    "Instructions": "Passive listening"
    }
    
task_info_mem = {
    "TaskName": "Associative Memory",
    "TaskDescription": """This task was adapted from Friedrich et al. (2015), doi: 10.1038/ncomms7004. \
During the experimental sessions, infants sat on their caregiver's lap. \
In each trial a coloured image of a single unfamiliar object appeared on the screen for 3,200 ms. \
These objects were created from geometric shapes. \
800 ms after image onset, the German indefinite article 'ein' (masculine/neuter) was acoustically presented \
to direct the infant's attention to the presented pseudoword that followed the article presentation \
at 1,600 ms after image onset. Note that the pseudoword audio file started with 50 ms silence! \
6 object-word pairs were presented consistently as pairs. \
6 object-word pairs were presented inconsistently where every word appeared once with every image of this category. \
""",
    "Instructions": """Children attentively watch the screen. Parents are instructed to withhold any reaction \
unless to bring their child's attention back to the screen when excessively fussy.
"""
}


# data set description content
authors = {
    "Data Management": "Johannes Julius Mohn", 
    "PI (Frankfurt)": "Yee Lee Shing",
    "PI (Berlin)": "Claudia Buss",
    "Others": "The Memobaby Study Team 2022-2026"
}
study_name = "Memobaby: The development of statistical learning and episodic memory during the first year of life"
acknowledgements_1 = """If you use this dataset in analyses or publications, please acknowledge its creators: \
The Memobaby Study, Project B04, SFB1315 (2nd funding period), Berlin, Germany. \
The study was conducted between 2022 and 2026 at Charité – Universitätsmedizin Berlin, \
Institut für Medizinische Psychologie. \
PIs: Prof. Dr. Claudia Buss, Charité – Universitätsmedizin Berlin, \
Prof. Dr. Yee Lee Shing, Goethe-Universität Frankfurt am Main. \
Study team: Johannes Julius Mohn, Martin Bauer, Franziska Gronow, Katharina Pittner, Amy Halbing, Isabelle Anne-Claire Périard. \
Students: Janna Pauline Dirks, Valentina Pittol Nercolini, Joseph Ventura Kieninger, Lea Lowak, Moritz Doerr.\
""",
acknowledgements_2 = """Thank you to the student interns who helped with data collection: \
Collin Brennan, Anna Mangels, Anna Melnik, Lea Nierlich, Svenja Otter, Eliana Ramos, Kira Raedler, \
Tom Schroeder, Aldiyar Sopybek, Alaa Tabaa, Nhu Ha Tran.
""",
data_license_type = "CCO"
ethics = "Goethe-Universität Frankfurt am Main, Geschäfts-Nr. 2021-412"
funding = "DFG – project number 327654276 SFB 1315"
references_and_links = "https://www.sfb1315.de/research/b04/"


# some fun
try:
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
except NameError:
    BASE_DIR = os.getcwd()
ASCII_ART_PATH = os.path.join(BASE_DIR, 'utils', 'ascii_art.txt')
