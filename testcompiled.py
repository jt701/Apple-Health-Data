import tkinter as tk
from tkinter import filedialog
import os
import main as m

class XmlToCsvConverter:
    def __init__(self, master):
        self.master = master
        self.master.title("XML to CSV Converter")

        # Create widgets
        self.input_label = tk.Label(self.master, text="Select an XML file:")
        self.input_label.pack()

        self.input_button = tk.Button(self.master, text="Browse", command=self.browse_input_file)
        self.input_button.pack()

        self.convert_button = tk.Button(self.master, text="Convert to CSV", command=self.convert_to_csv)
        self.convert_button.pack()

        # Initialize variables
        self.input_file_path = None

    def browse_input_file(self):
        self.input_file_path = filedialog.askopenfilename(
            title="Select an XML file",
            filetypes=[("XML files", "*.xml")]
        )

    def convert_to_csv(self):
        if self.input_file_path:
            input_file_dir, input_file_name = os.path.split(self.input_file_path)
            input_file_base_name, input_file_ext = os.path.splitext(input_file_name)
            output_file_name = input_file_base_name + ".csv"
            output_file_path = os.path.join(input_file_dir, output_file_name)
            os.replace(m.main(self.input_file_path), output_file_path)
            tk.messagebox.showinfo("Conversion Complete", f"CSV file saved as {output_file_path}")

if __name__ == "__main__":
    # Create the Tkinter window
    root = tk.Tk()

    # Create the XML to CSV converter object
    converter = XmlToCsvConverter(root)

    # Start the Tkinter event loop
    root.mainloop()