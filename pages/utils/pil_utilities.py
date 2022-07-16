import concurrent.futures
from PIL import Image
from os import listdir


# load las file from a folder
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


# load las files from a folder multiprocessing enabled
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


# load las files from a folder
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
    pass


if __name__ == "__main__":
    main()
