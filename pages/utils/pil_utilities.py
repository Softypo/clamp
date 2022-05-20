import concurrent.futures
#import pandas as pd
#import numpy as np
from PIL import Image
from os import listdir
#from tqdm.notebook import tqdm

# def filt_m(df, look=()):
#     name = df[0]
#     d = df[1]
#     add = []
#     for col in d.columns:
#         if col.startswith(look):
#             add.append(col)
#     if len(add)>=1: return [name, d[add]]


# # look for mnemonics
# def filter_multiprocess(df, look=()):
#     """load well logs las files from a folder and store them in a dictionary.

#     parameters
#     ----------
#     path : folder path containg the desired las files.
#     ext: bol, include extention in file name
#     """

#     look_lst = [look for _ in range(len(df))]

#     with concurrent.futures.ProcessPoolExecutor() as executor:
#         filtered = {f[0]: f[1] for f in tqdm(executor.map(filt_m, df.items(), look_lst), total=len(df), desc='Searching') if isinstance(f, list)}
#         #df_files = {f[0]: f[1] for f in tqdm(executor.map(todf, list(las_files.items())), total=len(list(las_files.items())))}
#     return filtered

# # look for mnemonics
# def filter(df, look=(), mean=True):
#     filtered = {}
#     for name, d in tqdm(df.items(), desc='Searching'):
#         add = []
#         for col in d.columns:
#             if col.startswith(look):
#                 add.append(col)
#         if len(add)>=1:
#             filtered[name] = d[add]

#     if mean==True:
#         filteredmean = {}
#         for name, d in tqdm(filtered.items(), desc='Calculating mean'):
#             nd = pd.DataFrame(index=d.index)
#             for mnemonic in look:
#                 add = []
#                 for col in d.columns:
#                     if isinstance(look, (str)):
#                         if col.startswith(look): add.append(col)
#                     elif col.startswith(mnemonic):
#                         add.append(col)
#                 if isinstance(look, (str)):
#                     nd[look] = d[add].mean(axis=1)
#                     break
#                 else: nd[mnemonic] = d[add].mean(axis=1)
#             filteredmean[name] = nd
#         return filteredmean
#     else: return filtered


# # transform lasio to dataframe
# def todf(las_file):
#     """transform lasio object to pandas dataframe.

#     parameters
#     ----------
#     las_file : lasio object.
#     """
#     if isinstance(las_file, (list, tuple)):
#         name = las_file[1].well.uwi.value
#         unit = las_file[1].well.step.unit
#         return [name, unit, las_file[1].df()]
#     else: return las_file.df()

# load las file from a folder for lasio
def load(filename, path=None, ext=False):
    """load las file.

    parameters
    ----------
    filename : name of the file including extension.
    path : file path.
    ext : bol, default False. include extencion.
    """
    if ext == False:
        name = filename.rpartition('.')[0].replace(' ', '_')
    else:
        name = filename.replace(' ', '_')
    if filename.endswith(('.jpeg', '.JPEG', '.png', '.PNG')):
        return [name, Image.open(path+'\\'+filename)]


# load las files from a folder for lasio multiprocessing enabled
def loader_pil_multiprocess(path=None, ext=False, todrop=None):
    """load well logs las files from a folder and store them in a dictionary.

    parameters
    ----------
    path : folder path containg the desired las files.
    ext: bol, include extention in file name
    todrop: list/tuple of filenames not to be included in the dataframe dictionary
    """
    path_lst = [path for _ in range(len(listdir(path)))]
    ext_lst = [ext for _ in range(len(listdir(path)))]
    if todrop == None:
        todrop = []

    with concurrent.futures.ProcessPoolExecutor() as executor:
        images = {f[0]: f[1] for f in executor.map(
            load, listdir(path), path_lst, ext_lst) if f[0] not in todrop}
    return images


# load las files from a folder for lasio
def loader_pil(path=None, ext=False):
    """load well logs las files from a folder and store them in a dictionary.

    parameters
    ----------
    path : folder path containg the desired las files.
    ext: bol, include extention in file name
    """
    try:
        images = {}
        for filename in listdir(path):
            if ext == False:
                name = filename.rpartition('.')[0].replace(' ', '_')
            else:
                name = filename.replace(' ', '_')
            if filename.endswith(('.jpeg', '.JPEG', '.png', '.PNG')):
                images[name] = Image.open(path+'\\'+filename)
        return images
    except:
        print('No files loaded for \\', path)


def main():
    images = loader_pil_multiprocess('data/446/tubeviews/cdc')
    #filter(lasdf, ('GR', 'DT'))
    pass


if __name__ == "__main__":
    main()
