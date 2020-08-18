import platform
import getpass
import os

DATA_DIR = '/Dropbox/NetCorDenStream/process_data/'
RAWDATA_DIR = '/Dropbox/NetCorDenStream/Raw_Data/'

if platform.system() == 'Darwin' and getpass.getuser() == 'Far_Ross(Rostand)':
    # Rostand - laptop
    EXPR_FOLDER = '/Users/rostand/Google Drive File Stream/Shared drives/{}'.format(DATA_DIR)
elif platform.system() == 'Linux' and getpass.getuser() == 'ross':
    # Rostand - Desktop
    EXPR_FOLDER = '/home/ross/PycharmProjects/ai-5g/data/'
    RESULTS_FOLDER = '/home/ross/PycharmProjects/ai-5g/data/'
    RESULTS_FOLDER1 = '/home/ross/PycharmProjects/ai-5g/data/ML_Data/'
elif platform.system() == 'Darwin' and getpass.getuser() == 'rostandarmelfezeu':
    # Rostand - Desktop
    DATA_FOLDER = '/Users/rostandarmelfezeu{}'.format(DATA_DIR)
    RAWDATA_FOLDER = '/Users/rostandarmelfezeu{}'.format(RAWDATA_DIR)
