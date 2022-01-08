# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

from tkinter import filedialog
from tkinter import *
from pathlib import Path
import logging
import os
import hashlib


def md5(fname):
    hash_md5 = hashlib.md5()
    file_name = Path(fname)
    with open(file_name, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)

    return hash_md5.hexdigest()


def get_1000_files(path):
    i = 0
    for row in os.walk(path):  # row beinhaltet jeweils einen Ordnerinhalt
        for filename in row[2]:  # row[2] ist ein tupel aus Dateinamen
            full_path: Path = Path(row[0]) / Path(filename)  # row[0] ist der Ordnerpfad
            i += 1
            filesurvey.append(
                [full_path, full_path.stat().st_size, hashlib.md5(Path(full_path).read_bytes()).hexdigest()])
            if i >= 1000:
                break
    try:
        catalog_file = open("catalog_file.txt", 'w')
        for one_file in filesurvey:
            #file_fullpath = str(one_file[0]) + "\\" + one_file[1]
            #file_fullpath = Path(one_file[0])
            #file_md5_summ = hashlib.md5(Path(one_file[0]).read_bytes()).hexdigest()
            catalog_file.write(str(one_file[0]) + " size:" + str(one_file[1]) + " md5=" + str(one_file[2]) + "\n")
    finally:
        catalog_file.close()
    #logging.info(filesurvey)

def duplicates_remover():
    for etalon in filesurvey:
        if etalon[2] != 0:  # md5 != 0
            i = 0
            for exepmle in filesurvey:
                if exepmle[2] != 0:  # md5 != 0
                    if exepmle[1] == etalon[1]:  # same size
                        if exepmle[2] == etalon[2]:  # same md5
                            if exepmle[0] != etalon[0]:  # not the same path
                                logging.info("dublicate:" + str(exepmle[0]))
                                filesurvey[i][2] = 0
                                os.rename(str(exepmle[0]), str(exepmle[
                                                                   0]) + "1")  # here need to compare pathes and findout how to relocate the file

                i += 1

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    logging.basicConfig(filename="sample.log", level=logging.INFO, filemode="w")
    logging.info("test run 080122")

    root = Tk()
    root["bg"] = "#CCCCCC"
    root.geometry("600x700+200+200")
    root.title("RoboLeg")
    root.resizable(False, False)

    canvas = Canvas(root, height=700, width=600)
    canvas.pack()

    path: Path = Path(filedialog.askdirectory())
    logging.info(str(path))
    canvas.create_text(30, 30, text=str(path), justify="left")
    filesurvey = []
    get_1000_files(path)

    logging.info("summs")
    duplicates_remover()


    canvas.create_text(150, 50, text="DONE!", justify="left")
    root.mainloop()

