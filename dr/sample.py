""" module to interact with text samples """
import os   

def filepath(filename, ext):
    spath = f"/dr/samples/{ext}/"
    src = os.getcwd() + spath
    ext = "." + ext
    return src + filename + ext

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