import os
import tkinter as tk
from tkinter import ttk
from tkinter.messagebox import showinfo
import numpy as np
import time
import nidaqmx
import nidaqmx.system
from nidaqmx.constants import LineGrouping
from nidaqmx.constants import Edge
from nidaqmx.constants import AcquisitionType 
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("TkAgg")
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib.widgets import Slider

class APP(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('Force Ramp Interface')
        self.geometry('700x1000')
        



        """
        Buttons
        """
        self.start_rec_button = tk.Button(self, text='START', bg ='green')
        self.start_rec_button['command'] = self.start_rec
        self.start_rec_button.pack()
        self.start_rec_button.place(x=10, y=10)

        self.stop_rec_button = tk.Button(self, text='STOP', bg ='red')
        self.stop_rec_button['command'] = self.stop_rec
        self.stop_rec_button.pack()
        self.stop_rec_button.place(x=70, y=10)

        self.trial_ID = tk.StringVar()
        self.lbl_trial_ID = ttk.Label(self, text='Trial Num:')
        self.lbl_trial_ID.pack(fill='x', expand=True)
        self.lbl_trial_ID.place(x=10, y=40)
        self.t_trial_ID = tk.Entry(self, textvariable=self.trial_ID)
        self.t_trial_ID.insert(0, "1")
        self.t_trial_ID.pack(fill='x', expand=True)
        self.t_trial_ID.focus()
        self.t_trial_ID.place(x=150, y=40, width = 50)

        self.check_dir_button = tk.Button(self, text='CHECK DIR', bg ='yellow')
        self.check_dir_button['command'] = self.check_dir
        self.check_dir_button.pack()
        self.check_dir_button.place(x=250, y=40)

        self.dump_path = tk.StringVar()
        self.lbl_dump_path = ttk.Label(self, text='Dump Path:')
        self.lbl_dump_path.pack(fill='x', expand=True)
        self.lbl_dump_path.place(x=10, y=70)
        self.t_dump_path = tk.Entry(self, textvariable=self.dump_path)
        self.t_dump_path.insert(0, r"C:\Users\praka\Desktop\TMSi data\N3 stim\P9\20230504\force_data")
        self.t_dump_path.pack(fill='x', expand=True)
        self.t_dump_path.focus()
        self.t_dump_path.place(x=150, y=70, width = 500)

        self.daq_name = tk.StringVar()
        self.lbl_daq_name = ttk.Label(self, text='DAQ ID:')
        self.lbl_daq_name.pack(fill='x', expand=True)
        self.lbl_daq_name.place(x=10, y=100)
        self.t_daq_name = tk.Entry(self, textvariable=self.daq_name)
        self.t_daq_name.insert(0, "Dev3")
        self.t_daq_name.pack(fill='x', expand=True)
        self.t_daq_name.focus()
        self.t_daq_name.place(x=150, y=100, width = 100)

        self.analog_chan = tk.StringVar()
        self.lbl_Ach_name = ttk.Label(self, text='Analog Inp Chans:')
        self.lbl_Ach_name.pack(fill='x', expand=True)
        self.lbl_Ach_name.place(x=10, y=130)
        self.t_Ach_name = tk.Entry(self, textvariable=self.analog_chan)
        self.t_Ach_name.insert(0, "ai1")
        self.t_Ach_name.pack(fill='x', expand=True)
        self.t_Ach_name.focus()
        self.t_Ach_name.place(x=150, y=130, width = 100)

        self.digi_chan = tk.StringVar()
        self.lbl_Dch_name = ttk.Label(self, text='Digital Inp Chans:')
        self.lbl_Dch_name.pack(fill='x', expand=True)
        self.lbl_Dch_name.place(x=10, y=160)
        self.t_Dch_name = tk.Entry(self, textvariable=self.digi_chan)
        self.t_Dch_name.insert(0, "port0/line0")
        self.t_Dch_name.pack(fill='x', expand=True)
        self.t_Dch_name.focus()
        self.t_Dch_name.place(x=150, y=160, width = 100)

        self.start_daq_button = tk.Button(self, text='START DAQ', bg ='yellow')
        self.start_daq_button['command'] = self.start_DAQ
        self.start_daq_button.pack()
        self.start_daq_button.place(x=10, y=190)

        self.stream_daq_button = tk.Button(self, text='STREAM DAQ', bg ='yellow')
        self.stream_daq_button['command'] = self.stream_DAQ
        self.stream_daq_button.pack()
        self.stream_daq_button.place(x=200, y=190)

        self.test_force_read_button = tk.Button(self, text='TEST RIG', bg ='yellow')
        self.test_force_read_button['command'] = self.test_force_read
        self.test_force_read_button.pack()
        self.test_force_read_button.place(x=300, y=190)

        self.conv_factor = tk.StringVar()
        self.lbl_conv_factor = ttk.Label(self, text='Torque Const.:')
        self.lbl_conv_factor.pack(fill='x', expand=True)
        self.lbl_conv_factor.place(x=10, y=220)
        self.t_conv_factor = tk.Entry(self, textvariable=self.conv_factor)
        self.t_conv_factor.insert(0, "0.26959694")
        self.t_conv_factor.pack(fill='x', expand=True)
        self.t_conv_factor.focus()
        self.t_conv_factor.place(x=150, y=220, width = 100)

        self.MVC_duration = tk.StringVar()
        self.lbl_MVC_len = ttk.Label(self, text='Duration of MVC (s):')
        self.lbl_MVC_len.pack(fill='x', expand=True)
        self.lbl_MVC_len.place(x=10, y=250)
        self.t_MVC_len = tk.Entry(self, textvariable=self.MVC_duration)
        self.t_MVC_len.insert(0, "5")
        self.t_MVC_len.pack(fill='x', expand=True)
        self.t_MVC_len.focus()
        self.t_MVC_len.place(x=150, y=250, width = 100)

        self.start_MVC_button = tk.Button(self, text='START MVC', bg ='yellow')
        self.start_MVC_button['command'] = self.get_MVC
        self.start_MVC_button.pack()
        self.start_MVC_button.place(x=10, y=280)

        self.trl_duration = tk.StringVar()
        self.lbl_trl_duration = ttk.Label(self, text='Trial Duration (s):')
        self.lbl_trl_duration.pack(fill='x', expand=True)
        self.lbl_trl_duration.place(x=10, y=330)
        self.t_trl_duration = tk.Entry(self, textvariable=self.trl_duration)
        self.t_trl_duration.insert(0, "60")
        self.t_trl_duration.pack(fill='x', expand=True)
        self.t_trl_duration.focus()
        self.t_trl_duration.place(x=150, y=330, width = 100)

        self.init_wait = tk.StringVar()
        self.lbl_init_wait = ttk.Label(self, text='Ramp Delay (s):')
        self.lbl_init_wait.pack(fill='x', expand=True)
        self.lbl_init_wait.place(x=10, y=360)
        self.t_init_wait = tk.Entry(self, textvariable=self.init_wait)
        self.t_init_wait.insert(0, "5")
        self.t_init_wait.pack(fill='x', expand=True)
        self.t_init_wait.focus()
        self.t_init_wait.place(x=150, y=360, width = 100)

        self.peak_ramp_force = tk.StringVar()
        self.lbl_peak_ramp_force = ttk.Label(self, text='Max Ramp Force (x MVC):')
        self.lbl_peak_ramp_force.pack(fill='x', expand=True)
        self.lbl_peak_ramp_force.place(x=310, y=360)
        self.t_peak_ramp_force = tk.Entry(self, textvariable=self.peak_ramp_force)
        self.t_peak_ramp_force.insert(0, "0.3")
        self.t_peak_ramp_force.pack(fill='x', expand=True)
        self.t_peak_ramp_force.focus()
        self.t_peak_ramp_force.place(x=450, y=360, width = 100)

        self.lbl_max_force = ttk.Label(self, text="Max Force",font=('Helvetica 16 bold'))
        self.lbl_max_force.pack(fill='x', expand=True)
        self.lbl_max_force.place(x=400, y=150)
        self.max_force = tk.StringVar()
        self.max_force.set('0')
        self.lbl_max_force_num = ttk.Label(self, textvariable=self.max_force,font=('Helvetica 30 bold'))
        self.lbl_max_force_num.pack(fill='x', expand=True)
        self.lbl_max_force_num.place(x=400, y=200)

        self.start_vanilla_button = tk.Button(self, text='PUSH VANILLA', bg ='yellow')
        self.start_vanilla_button['command'] = self.do_vanilla
        self.start_vanilla_button.pack()
        self.start_vanilla_button.place(x=10, y=400)
        
        self.start_sombrero_button = tk.Button(self, text='PUSH SOMBRERO', bg ='yellow')
        self.start_sombrero_button['command'] = self.do_sombrero
        self.start_sombrero_button.pack()
        self.start_sombrero_button.place(x=310, y=400)

        self.sombrero_width = tk.StringVar()
        self.lbl_sombrero_width = ttk.Label(self, text='Sombrero hold (s):')
        self.lbl_sombrero_width.pack(fill='x', expand=True)
        self.lbl_sombrero_width.place(x=310, y=430)
        self.t_sombrero_width = tk.Entry(self, textvariable=self.sombrero_width)
        self.t_sombrero_width.insert(0, "10")
        self.t_sombrero_width.pack(fill='x', expand=True)
        self.t_sombrero_width.focus()
        self.t_sombrero_width.place(x=500, y=430, width = 100)

        self.sombrero_ramp = tk.StringVar()
        self.lbl_sombrero_ramp = ttk.Label(self, text='Sombrero ramp (s):')
        self.lbl_sombrero_ramp.pack(fill='x', expand=True)
        self.lbl_sombrero_ramp.place(x=310, y=460)
        self.t_sombrero_ramp = tk.Entry(self, textvariable=self.sombrero_ramp)
        self.t_sombrero_ramp.insert(0, "5")
        self.t_sombrero_ramp.pack(fill='x', expand=True)
        self.t_sombrero_ramp.focus()
        self.t_sombrero_ramp.place(x=500, y=460, width = 100)

        self.sombrero_force = tk.StringVar()
        self.lbl_sombrero_force = ttk.Label(self, text='Sombrero Ramp Force (x MVC):')
        self.lbl_sombrero_force.pack(fill='x', expand=True)
        self.lbl_sombrero_force.place(x=310, y=490)
        self.t_sombrero_force = tk.Entry(self, textvariable=self.sombrero_force)
        self.t_sombrero_force.insert(0, "0.1")
        self.t_sombrero_force.pack(fill='x', expand=True)
        self.t_sombrero_force.focus()
        self.t_sombrero_force.place(x=500, y=490, width = 100)

        fig = Figure(figsize=(7, 4), dpi=100)
        self.disp_target = fig.add_subplot(111)
        
        self.disp_target.set_xlabel("Time (s)", fontsize=14)
        self.disp_target.set_ylabel("Torque (Nm)", fontsize=14)
        
        self.canvas_disp_target = FigureCanvasTkAgg(fig, master=self)  
        self.canvas_disp_target.draw()
        self.canvas_disp_target.get_tk_widget().pack(side=tk.BOTTOM, fill='x', expand=True)
        self.canvas_disp_target.get_tk_widget().place(y=600,)

    def start_rec(self,):
        print('starting')
        self.trial_ID.set(str(int(self.trial_ID.get())+1))
        current_trial = int(self.trial_ID.get())
        self.t_trial_ID.delete(0, 'end')
        self.t_trial_ID.insert(0, str(current_trial))
        self.update()

    def stop_rec(self,):
        print('stopping')
        self.trial_ID.set(str(int(self.trial_ID.get())+1))
        current_trial = int(self.trial_ID.get())
        self.t_trial_ID.delete(0, 'end')
        self.t_trial_ID.insert(0, str(current_trial))
        self.update()

    def test_force_read(self):
        self.test_force_read_button.config(bg = 'red')
        self.test_force_read_button.config(bg = 'yellow')
        print("force trace for acclamatization")

    def check_dir(self):
        dump_name = self.dump_path.get()
        if not os.path.isdir(dump_name):
            print("Dir not found, making it")
            os.mkdir(dump_name)
        self.check_dir_button.config(bg = 'green')

    def start_DAQ(self):
        daq_name = self.daq_name.get()
        di_chan_name = self.digi_chan.get()
        ai_chan_name = self.analog_chan.get()

        self.task_trig = nidaqmx.Task("rec_trig")
        self.task_trig.di_channels.add_di_chan(daq_name+"/" + di_chan_name, line_grouping=LineGrouping.CHAN_PER_LINE)

        self.task_force = nidaqmx.Task("rec_force")
        self.task_force.ai_channels.add_ai_voltage_chan(daq_name+"/"+ai_chan_name)
        self.in_stream_force = self.task_force.in_stream

        self.start_daq_button.config(bg = 'green')

    def stream_DAQ(self):
        self.stream_daq_button.config(bg = 'red')
        t0 = time.time()
        while time.time()-t0 < 5:
            print("trigs", self.task_trig.read(number_of_samples_per_channel=10))
            print("force", abs(np.mean(self.in_stream_force.read(number_of_samples_per_channel=10)))*float(self.conv_factor.get()))
        self.stream_daq_button.config(bg = 'yellow')

    def get_MVC(self):
        trial_len = int(self.MVC_duration.get())
        t0 = time.time()
        max_force = 0
        self.start_MVC_button.config(bg = 'red')

        while time.time()-t0 < trial_len:
            curr_force = abs(np.mean(self.in_stream_force.read(number_of_samples_per_channel=10)))*float(self.conv_factor.get())
            if curr_force > max_force:
                max_force = curr_force
                self.max_force.set(str(max_force))
                self.update()
        self.max_force 
        self.start_MVC_button.config(bg = 'green')

    def do_sombrero(self):
        max_force = float(self.max_force.get())
        peak_ramp_force = float(self.peak_ramp_force.get())
        trl_duration = float(self.trl_duration.get())
        init_wait = float(self.init_wait.get())
        sombrero_width = float(self.sombrero_width.get())
        sombrero_ramp = float(self.sombrero_ramp.get())
        sombrero_force = float(self.sombrero_force.get())

        self.target_profile_x = [0, init_wait, init_wait+sombrero_ramp, init_wait+sombrero_ramp+sombrero_width, trl_duration//2, 
                                 trl_duration-init_wait-sombrero_ramp-sombrero_width, trl_duration-init_wait-sombrero_ramp, trl_duration-init_wait, trl_duration]
        self.target_profile_y = [0, 0, max_force*sombrero_force, max_force*sombrero_force, max_force*peak_ramp_force, max_force*sombrero_force, max_force*sombrero_force, 0, 0]
        assert len(self.target_profile_x) == len(self.target_profile_y)

        self.disp_target.clear()
        
        self.disp_target.set_xlabel("Time (s)", fontsize=14)
        self.disp_target.set_ylabel("Torque (Nm)", fontsize=14)
        self.disp_target.plot(self.target_profile_x, self.target_profile_y, linewidth = 5, color = 'r')
        self.canvas_disp_target.draw()
        self.start_vanilla_button.config(bg = 'yellow')
        self.start_sombrero_button.config(bg = 'green')

    def do_vanilla(self):
        max_force = float(self.max_force.get())
        peak_ramp_force = float(self.peak_ramp_force.get())
        trl_duration = float(self.trl_duration.get())
        init_wait = float(self.init_wait.get())

        self.target_profile_x = [0, init_wait, trl_duration//2, trl_duration-init_wait, trl_duration]
        self.target_profile_y = [0, 0, peak_ramp_force*max_force, 0, 0]
        assert len(self.target_profile_x) == len(self.target_profile_y)

        self.disp_target.clear()
        self.disp_target.set_xlabel("Time (s)", fontsize=14)
        self.disp_target.set_ylabel("Torque (Nm)", fontsize=14)
        self.disp_target.plot(self.target_profile_x, self.target_profile_y, linewidth = 5, color = 'r')
        self.canvas_disp_target.draw()

        self.start_sombrero_button.config(bg = 'yellow')
        self.start_vanilla_button.config(bg = 'green')



def main():
    tk_trial = APP()
    tk_trial.mainloop()
    return None

if __name__ == "__main__":
    main()