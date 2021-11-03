langs_dict = {}

from os import listdir, path
from importlib import import_module

files_list = listdir(path.dirname(__file__))
for f in files_list:
    if f.endswith(".py") and not f.startswith("__init__"):
        file_name = f.split(".")
        module_name = import_module("." + file_name[0], package=__name__)
        langs_dict.update(module_name.langs_dict)
del files_list, file_name, module_name
