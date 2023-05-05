import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import main as m
import csv

class XmlToCsvConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Health Data from XML") 

        # Create widgets
        self.input_label = tk.Label(self.master, text="Select an XML file:")
        self.input_label.pack()

        self.input_button = tk.Button(self.master, text="Select XML File", command=self.browse_input_file)
        self.input_button.pack()

        self.convert_button = tk.Button(self.master, text="Get Health Data", command=self.convert_to_csv)
        self.convert_button.pack()

        # Initialize variables
        self.input_file_path = None
        
        

    def browse_input_file(self):
        self.input_file_path = filedialog.askopenfilename(
            title="Select an XML file",
            filetypes=[("XML files", "*.xml")]
        )

    #try except block, except with this xml is not configured correctly
    #write correctly
    def convert_to_csv(self):
        progress  = ttk.Progressbar(root, orient='horizontal', length=200, mode='indeterminate')
        progress.pack()
        progress.start()
        tk.messagebox.showinfo("Conversion started")
        if self.input_file_path:
            input_file_dir, input_file_name = os.path.split(self.input_file_path)
            input_file_base_name, input_file_ext = os.path.splitext(input_file_name)
            output_file_name = input_file_base_name + ".csv"
            output_file_path = os.path.join(input_file_dir, output_file_name)
            try:
                stat_df = m.main(self.input_file_path)
                stat_df.to_csv(output_file_path, index=False)
                progress.stop()
                progress.destroy()
                tk.messagebox.showinfo("Conversion Complete", f"CSV file saved as {output_file_path}")
            except:
                progress.stop()
                progress.destroy()
                tk.messagebox.showinfo("XML file is not of the proper configuration. Choose an alternative XML file if possible")

if __name__ == "__main__":
    # Create the Tkinter window
    root = tk.Tk()

    # Create the XML to CSV converter object
    converter = XmlToCsvConverter(root)

    # Start the Tkinter event loop
    root.mainloop()