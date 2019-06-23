import os

class Files:
    def __init__(self):
        self.data_path = "data/"
        self.file_list_ = open("file_list.data", "r")
        self.file_list = self.file_list_.readlines()


    pass

