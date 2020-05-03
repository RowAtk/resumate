import os
from pandas import read_csv

ext_sep = {
    'csv' : ',',
    'tsv' : '\t'
}

def abv_cleaner(filename, lst=False):
    """ clean sample data """

    def transform_column(data, col):
        """ transform column data to comma separated values(csv) """
        # "dog, cat or pig"
        # output: "dog, cat, pig"
        data[col] = data[col].replace(" or", ",")
        
    data = fileToDF(filename, ext='tsv')

    for index, row in data.iterrows():
        transform_column(row, 'Abbreviation')
    if lst:
        return data.values.tolist()
    return data

def fileToDF(filename, ext="csv", lst=False):
    fpath = filepath(filename, ext=ext)
    data = read_csv(fpath, sep = ext_sep[ext])

    if lst:
        return data.values.tolist()
    return data



""" module to interact with text samples """

def filepath(filename, ext):
    spath = f"/data/{ext}/"
    src = os.getcwd() + spath
    ext = "." + ext
    return src + filename   

def get(filename, ext):
    return open(filepath(filename, ext))

def getText(filename, ext="txt", size=None):
    try:
        print(filepath(filename, ext))
        file = get(filename, ext)
        text = file.read(size) if size and type(size) == int else file.read()
        file.close()
        return text
    except IOError:
        print("Error reading file")


# data = tsv_cleaner('certabv.tsv')

    