import tkinter as tk
from tkinter import filedialog, ttk, END

import asyncio
import os
import ctypes

from srtmergecommon import do_merge

company = 'Nibiru'
product = 'SRT Merger'
subproduct = 'Merger'
year = 2024
version = '0.2'

srt_position_modes = [
['Top left', '{\\an7}'],
['Top center', '{\\an8}'],
['Top right', '{\\an9}'],

['Center left', '{\\an4}'],
['Center center', '{\\an5}'],
['Center right', '{\\an6}'],

['Bottom left', '{\\an1}'],
['Bottom center', '{\\an2}'],
['Bottom right', '{\\an3}']
]

srt_color_modes = [
['White', '#FFFFFF'],
['Red', '#FF0000'],
['Green', '#00FF00'],
['Blue', '#0000FF'],
['Yellow', '#FFFF00'],
['Cyan', '#00FFFF'],
['Magenta', '#FF00FF']
]

srt_position_labels = [x[0] for x in srt_position_modes]
srt_color_labels = [x[0] for x in srt_color_modes]

myappid = f'{company}.{product}.{subproduct}.{version}'

ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(myappid)

class App:
    async def exec(self):
        self.window = Window()
        await self.window.show();

class Window(tk.Tk):

    def __init__(self):

        self.root = tk.Tk()
        self.root.geometry("1300x280")
        self.root.iconbitmap("srt.ico")

        self.root.title(f'{product} v{version} by {company} ©{year}')

        self.srt_primary_color=ttk.Combobox(values=srt_color_labels, width=7)
        self.srt_secondary_color=ttk.Combobox(values=srt_color_labels, width=7)

        self.srt_primary_position=ttk.Combobox(values=srt_position_labels, width=11)
        self.srt_secondary_position=ttk.Combobox(values=srt_position_labels, width=11)

        self.srt_primary_color.set(srt_color_labels[4])
        self.srt_secondary_color.set(srt_color_labels[0])

        self.srt_primary_position.set(srt_position_labels[6])
        self.srt_secondary_position.set(srt_position_labels[8])

        self.input_file_primary_path=tk.StringVar()
        self.input_file_secondary_path=tk.StringVar()
        self.output_file_path=tk.StringVar()
        self.progress = tk.IntVar()

        self.input_file_primary_label = tk.Label(text='Primary SRT')
        self.input_file_primary_path_entry = tk.Entry(borderwidth=1, textvariable = self.input_file_primary_path)
        self.select_input_file_primary_button = tk.Button(text='Select', width=10, command=self.set_input_file_primary_path)

        self.input_file_secondary_label = tk.Label(text='Secondary SRT')
        self.input_file_secondary_path_entry = tk.Entry(borderwidth=1, textvariable = self.input_file_secondary_path)
        self.select_input_file_secondary_button = tk.Button(text='Select', width=10, command=self.set_input_file_secondary_path)

        self.output_file_label = tk.Label(text='Target SRT file')
        self.output_file_path_entry = tk.Entry(borderwidth=1, textvariable = self.output_file_path)
        self.select_output_file_button = tk.Button(text='Select', width=10, command=self.set_output_file_path)

        self.progressbar = ttk.Progressbar(variable=self.progress) #mode="determinate"
        self.start_process_button = tk.Button(text='Start process', width=10, command=lambda: asyncio.create_task(self.start_process()))

        self.log_text = tk.Text(height=5, width=40)

        self.scrollbar = ttk.Scrollbar(orient="vertical", command = self.log_text.yview)

        #pack
        self.srt_primary_color.grid(row=0, column=0, sticky = "e", pady=3, padx=3)
        self.srt_primary_position.grid(row=0, column=1, sticky = "e", pady=3, padx=3)
        self.input_file_primary_label.grid(row=0, column=2, sticky = "e", pady=3, padx=3)
        self.input_file_primary_path_entry.grid(row=0, column=3, sticky = "ew", pady=3, padx=3)
        self.select_input_file_primary_button.grid(row=0, column=4, columnspan=2, sticky = "e", pady=3, padx=3)

        self.srt_secondary_color.grid(row=1, column=0, sticky = "e", pady=3, padx=3)
        self.srt_secondary_position.grid(row=1, column=1, sticky = "e", pady=3, padx=3)
        self.input_file_secondary_label.grid(row=1, column=2, sticky = "e", pady=3, padx=3)
        self.input_file_secondary_path_entry.grid(row=1, column=3, sticky = "ew", pady=3, padx=3)
        self.select_input_file_secondary_button.grid(row=1, column=4, columnspan=2, sticky = "e", pady=3, padx=3)

        self.output_file_label.grid(row=2, column=2, sticky = "w", pady=3, padx=3)
        self.output_file_path_entry.grid(row=2, column=3, sticky = "ew", pady=3, padx=3)
        self.select_output_file_button.grid(row=2, column=4, columnspan=2, sticky = "e", pady=3, padx=3)

        self.progressbar.grid(row=3, column=0, columnspan=4, sticky = "ew", pady=3, padx=3)
        self.start_process_button.grid(row=3, column=4, columnspan=2, sticky = "e", pady=3, padx=3)

        self.log_text.grid(row=4,column=0, columnspan=5, pady=3, padx=3, sticky = "ew")

        self.scrollbar.grid(row=4, column=5, sticky = "nsw")

        self.log_text.tag_config('comment', foreground="blue")
        self.log_text.tag_config('error', foreground="red")
        self.log_text["yscrollcommand"]=self.scrollbar.set

        self.root.columnconfigure(0, weight=0)
        self.root.columnconfigure(1, weight=0)
        self.root.columnconfigure(2, weight=0)
        self.root.columnconfigure(3, weight=5)
        self.root.columnconfigure(4, weight=0)

        self.root.protocol("WM_DELETE_WINDOW", self.exit_app)

    def set_input_file_primary_path(self):
        file_path = filedialog.askopenfilename(defaultextension=".srt", filetypes=[("SRT Files", "*.srt")])
        self.input_file_primary_path.set(file_path)

        merged_path = file_path.replace('.srt', '.merged.srt')
        
        self.output_file_path.set(merged_path)

    def set_input_file_secondary_path(self):
        file_path = filedialog.askopenfilename(defaultextension=".srt", filetypes=[("SRT Files", "*.srt")])
        self.input_file_secondary_path.set(file_path)

    def set_output_file_path(self):

        current_state = self.output_file_path.get()
        if not current_state:
            current_state = 'merged.srt'

        file_path = filedialog.asksaveasfilename(initialfile=current_state, filetypes=[("SRT Files", "*.csv")])
        self.output_file_path.set(file_path)
        #self.progress.set(0)

    def clean_log (self):
        self.log_text.delete("1.0", END)

    def add_to_log (self, text, tag = None):
        self.log_text.insert(END, f'{text}\n', tag)

    def get_value_by_label (self, label, data):
        value = None

        for item in data:
            if item[0] == label:
                value = item[1]
                break
        return value
    
    async def start_process(self):

        self.clean_log ()
        self.progress.set(0)

        input_file_primary_path = self.input_file_primary_path.get()
        input_file_secondary_path = self.input_file_secondary_path.get()
        output_file_path = self.output_file_path.get()

        if not input_file_primary_path:
            self.add_to_log ('Primary path is empty!', 'error')
        elif not input_file_secondary_path:
            self.add_to_log ('Secondary path is empty!', 'error')   
        elif not output_file_path:
            self.add_to_log ('Output path is empty!', 'error') 

        elif (input_file_primary_path == output_file_path):
            self.add_to_log ('Primary and output path is equal!', 'error')
        elif (input_file_secondary_path == output_file_path):
            self.add_to_log ('Primary and output path is equal!', 'error')
        
        else:    
            #can process now
            self.start_process_button["state"] = "disabled" #для предотвращения двойного запуска
            self.add_to_log ('Start processing')

            primary_preamble_label = self.srt_primary_position.get()
            secondary_preamble_label = self.srt_secondary_position.get()
            primary_color_label = self.srt_primary_color.get()
            secondary_color_label = self.srt_secondary_color.get() 


            # Write merged to file

            do_merge(input_file_primary_path,
                     self.get_value_by_label(primary_preamble_label, srt_position_modes),
                     self.get_value_by_label(primary_color_label, srt_color_modes),
                     input_file_secondary_path,
                     self.get_value_by_label(secondary_preamble_label, srt_position_modes),
                     self.get_value_by_label(secondary_color_label, srt_color_modes),
                     output_file_path)
        
            self.progress.set(100)
  
            self.add_to_log ('Done!')
            self.start_process_button["state"] = "normal"

    async def show(self):
        while True:
            self.root.update()
            await asyncio.sleep(0.01)

    def exit_app(self):
        os._exit(0)

asyncio.run(App().exec())