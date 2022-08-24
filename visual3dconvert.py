import pandas as pd
import numpy as np


def get_name_row(file, name_row_index):
    for c in pd.read_csv(file, sep=None, header=None, chunksize=1, low_memory=False):
        name_row = c.iloc[name_row_index]
        break
    
    assert len(name_row) > 0
    
    return name_row


def create_header(name_row):
    column_names = pd.Series(['','ANALOGTIME']).append(name_row)
    number_of_columns = len(name_row)
    
    globalheader = pd.DataFrame([''] + ['GLOBAL'] * (number_of_columns+1), index=column_names).T
    typeheader = pd.DataFrame([''] + ['FRAME_NUMBERS'] + ['ANALOG'] * (number_of_columns), index=column_names).T
    originalheader = pd.DataFrame([''] + ['ORIGINAL'] * (number_of_columns+1), index=column_names).T
    itemheader = pd.DataFrame(['ITEM'] + [0] * (number_of_columns+1), index=column_names).T
    nameheader = column_names.to_frame().T
    nameheader.columns = column_names
    zeroheader = pd.DataFrame(['1'] + [0] * (number_of_columns+1), index=column_names).T

    concatheader = pd.concat([globalheader, nameheader, typeheader, originalheader, itemheader, zeroheader], ignore_index=True)
    
    return concatheader


def write_header_to_file(header, export_name):
    header.to_csv(export_name, sep='\t', index=False, header=False)


def write_data_to_file(file, rate, export_name):
    for chunk in pd.read_csv(file, sep=None, skiprows=1,dtype=str, header=None, chunksize=50000, low_memory=False):
        chunk.reset_index(level=chunk.index.names, inplace=True)
        chunk.reset_index(level=chunk.index.names, inplace=True)
        chunk['level_0'] = chunk['index']
        chunk['level_0'] += 2
        chunk['index'] += 1
        chunk['index'] *= 1/rate
        chunk['index'] = round(chunk['index'],4)
        chunk.to_csv(export_name, sep='\t', index=False, header=False,mode='a')


def visual3dconvert(file, rate, name_row_index, **kwargs):
    '''Input: a file, Output: c3d formatted ascii
    '''

    export_name = os.path.basename(file)[0:-4] + "_converted.txt"   
    for k,v in kwargs.items():
        if k == "export_name":
            export_name = v
        
    name_row = get_name_row(file, name_row_index)
    header = create_header(name_row)
    write_header_to_file(header, export_name)
    write_data_to_file(file, rate, export_name)


if __name__ == "__main__":
    from tkinter import Tk
    from tkinter.filedialog import askopenfilenames

    pd.options.mode.chained_assignment = None
    Tk().withdraw()
    filenames = askopenfilenames()
    
    sample_rate = 2000
    name_row_index = 0
    
    for i in filenames:
        visual3dconvert(i, sample_rate, name_row_index)
