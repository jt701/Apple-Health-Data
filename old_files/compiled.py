import tkinter as tk
from tkinter import filedialog
import src.main as m
import os


#use tkinter for GUI
def main():
    xml_path = input("Enter the path to the XML file: ")
    if xml_path:
        csv_file = m.main(xml_path)
    csv_dirname = os.path.dirname(os.path.abspath(xml_path))
    csv_filename = os.path.basename(csv_file)
    csv_filepath = os.path.join(csv_dirname, csv_filename)
    os.replace(csv_file, csv_filepath)
if __name__ == '__main__':
    while True:
        main()