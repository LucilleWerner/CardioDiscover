import pandas as pd
import dask.dataframe as dd
import os

study_id = str
path = str
sep = str
headers = list
header_idx = list
pickle = bool


def init(this_study, pickle=False):
    global study_id, path, sep, headers, header_idx

    study_id = this_study.studyID
    path = this_study.path
    sep = this_study.sep
    headers = this_study.headers
    header_idx = this_study.head_idx
    # chunk file into dataframes of 5000 lines
    if pickle:
        chunk_to_pickle()
    else:
        return chunk_iterator()


def make_study_dir():

    def checkdir(study_dir):
        # dirname = os.path.dirname(os.path.abspath(study_dir))
        dirname = os.path.dirname(study_dir)
        print(dirname)
        if not os.path.exists(dirname):
            os.makedirs(dirname)

    study_dir = "../Temp/Chunks/{}/".format(study_id)
    checkdir(study_dir)
    return study_dir


def chunk_iterator():
    ch_iter = pd.read_csv(filepath_or_buffer=path, sep=sep, header=0,
                          names=headers, usecols=header_idx, chunksize=500)
    return ch_iter


def chunk_to_pickle():
    study_dir = make_study_dir()
    for i, chunk in enumerate(pd.read_csv(filepath_or_buffer=path, sep=sep, header=0,
                                          names=headers, usecols=header_idx, chunksize=500)):
        chunk.to_pickle('{}/{}_{}.pk'.format(study_dir, study_id, str(i)))


# function used for 'classify_columns', may be reused whenever small chunks are of use
def small_chunk(sep='\t', path='', ch=25):
    df = pd.read_csv(filepath_or_buffer=path, sep=sep, header=0, chunksize=ch)
    chunk = df.get_chunk()

    return chunk

def dask_dataframe(sep='\t', path="", ch=500):
    df = dd.read_csv(filepath_or_buffer=path, sep=sep, header=0, chunksize=ch)
    return df


