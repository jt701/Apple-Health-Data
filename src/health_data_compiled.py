import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import src.main as m
import sys

"""
Graphical user interface that allows you to select xml apple health file from computer. 
You can then obtains its stats. These stats are saved as a csv in the same folder as the
apple health data. 
"""
#loading icon when opening program
if getattr(sys, 'frozen', False):
    import pyi_splash
    
class XmlToCsvConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("Health Data from XML") 

        # Create widgets
        self.input_button = tk.Button(self.master, text="Select XML File", command=self.browse_input_file)
        self.input_button.pack(pady = 10)

        self.convert_button = tk.Button(self.master, text="Get Health Data", command=self.convert_to_csv)
        self.convert_button.pack()
        
        #metric values
        self.numMetrics = 0 
        self.numEntries = 0
        
    
        
        
        # Instructions
        instruction_label = tk.Label(self.master, text="Instructions", font=("Arial", 16, "bold"))
        instruction_label.pack(pady=10)
        
        instructions = """
        1. Open Apple Health app
        2. Click on profile on top right corner
        3. Scroll down and press "Export All Health Data"
        4. Export the data to a local computer using bluetooth, etc.
        5. Press the "Select XML File button"
        6. Go into the data folder. 
        7. Select "export_fixed.xml" if it exists.
        8. Otherwise, select "export.xml"
        9. Press "Get Health Data". The button will be remain 
        pressed until the data is read.
        10. A CSV file with the stats will be placed in the same
        directory as your data file
        """
        
        instructions_text = tk.Text(self.master, height=14, width=50, font=("Arial", 12))
        instructions_text.insert(tk.END, instructions)
        instructions_text.pack()
        
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
        
        if self.input_file_path:
            input_file_dir, input_file_name = os.path.split(self.input_file_path)
            input_file_base_name, input_file_ext = os.path.splitext(input_file_name)
            output_file_name = input_file_base_name + ".csv"
            output_file_path = os.path.join(input_file_dir, output_file_name)
            try:
                stat_df = m.main(self.input_file_path)
                stat_df.to_csv(output_file_path, index=False)
                self.numMetrics = m.valid_rows(stat_df)
                self.numEntries = m.entries_filled(stat_df)
                
                numMetric_label = tk.Label(self.master, text=f"Percentage of Metrics: {int(self.numMetrics / 13 * 100)} %")
                numMetric_label.pack()
                
                numEntries_label = tk.Label(self.master, text=f"Percentage of Boxes: {int(self.numEntries / 364 * 100)} %")
                numEntries_label.pack()
            


                tk.messagebox.showinfo("Conversion Complete", f"CSV file saved as {output_file_path}")
            except:
                tk.messagebox.showinfo("Bad File", "XML file is not of the proper configuration. Choose an alternative XML file if possible")
        else:
            tk.messagebox.showinfo("Bad File", "XML file is not of the proper configuration. Choose an alternative XML file if possible")
if __name__ == "__main__":
    # Create the Tkinter window
    root = tk.Tk()

    # Create the XML to CSV converter object
    converter = XmlToCsvConverter(root)
    
    #close loading icon
    if getattr(sys, 'frozen', False):
        pyi_splash.close()

    # Start the Tkinter event loop
    root.mainloop()