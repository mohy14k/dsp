from tkinter import * 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import ttk
from task2 import operations_signal_window
from task3 import quantization_window
from task4 import frequency_domain_window
from task6 import task6_window
from task7 import task7_window
#button1

def get_file_path():
    file_read_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    return file_read_path

# read
def read_File(filePath: str):
    myfile = open(filePath, 'r')
    lines = [line.strip() for line in myfile.readlines()]
    myfile.close()
    
    samples = []
    for i in range(3):
        samples.append(int(lines.pop(0)))

    index_x = []
    index_y = []
    for row in lines:
        x = row.split(sep=" ")
        index_x.append(float(x[0]))
        index_y.append(float(x[1]))

    return [samples, index_x, index_y]

# plot
def plot_discrete_and_analog_signals(df: pd.DataFrame):
    # Create a larger figure with two subplots (1 row, 2 columns)
    fig, axes = plt.subplots(1, 2, figsize=(16, 8))  

    # Plot the discrete signal as a stem plot on the first subplot
    axes[0].stem(df[df.columns[0]], df[df.columns[1]], basefmt=" ", use_line_collection=True)
    axes[0].set_title('Discrete Signal', fontsize=18)
    axes[0].set_xlabel(df.columns[0], fontsize=14)  # Set x-label
    axes[0].set_ylabel(df.columns[1], fontsize=14)  # Set y-label
    axes[0].grid(True)
    


    # Plot the analog signal on the second subplot
    sns.lineplot(data=df, x=df.columns[0], y=df.columns[1], marker="o", markersize=7, ax=axes[1])
    axes[1].set_title('Analog Signal', fontsize=18)
    axes[1].set_xlabel(df.columns[0], fontsize=14)  # Set x-label
    axes[1].set_ylabel(df.columns[1], fontsize=14)  # Set y-label
    axes[1].grid(True)
    
   

    # Adjust layout
    plt.tight_layout()
    plt.show()

# read window function
def read_window():
    filePath = get_file_path()

    signalData = read_File(filePath)

    df_read = pd.DataFrame({
        "time": signalData[1],
        'amplitude': signalData[2]
    })
    
    plot_discrete_and_analog_signals(df_read)

#-------------------------------------------------------------------
#button2

def get_save_file_path():
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",  # Default extension is now .txt
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    return file_path


def write_file(filename:str,df:pd.DataFrame,sampligFrequency:float,signalType:int=0,isPeriodic:int=0):
    myFile = open(filename,"w")
    myFile.write(f"{signalType}\n")
    myFile.write(f"{isPeriodic}\n")
    myFile.write(f"{sampligFrequency}\n")
        
        # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        myFile.write(f"{row[0]} {row[1]}\n")
    myFile.close()


def generate_signal (type:str, amplitude:float, phaseShift:float, analogFrequency:float, SamplingFrequency:float):
    #sin(2pi n fa/fs + theta)
    
    digital_frequency = analogFrequency/SamplingFrequency
    indexes = np.arange(0,SamplingFrequency)
    if type == 'cos':
        result = amplitude * np.cos(2 * np.pi * digital_frequency * 
                                    indexes + phaseShift)
    else:
        result = amplitude * np.sin(2 * np.pi * digital_frequency * 
                                    indexes + phaseShift)

    return pd.DataFrame({'index':indexes,'result':result})


def generate_signal_button_action():
    
    signal_type = type_comboBox.get()
    amplitude = float(amplitude_entry.get())
    analog_frequency = float(analogFrequency_entry.get())
    sampling_frequency = float(samplingFrequency_entry.get())
    phase_shift = float(phaseShift_entry.get())

    
    df_generate = generate_signal(
        type=signal_type,
        amplitude=amplitude,
        analogFrequency=analog_frequency,
        SamplingFrequency=sampling_frequency,
        phaseShift=phase_shift
    )
    
    path = get_save_file_path()
    write_file(filename=path,df=df_generate,sampligFrequency=sampling_frequency)

    plot_discrete_and_analog_signals(df_generate)



def generate_signal_window():
    window = Tk()
    window.geometry("1000x650")

    global type_comboBox, amplitude_entry, analogFrequency_entry, samplingFrequency_entry, phaseShift_entry

    # Type label and comboBox
    type_label = Label(window, text="type", fg="black", font=("Arial", 12))
    type_label.place(x=10, y=10)
    type_comboBox = ttk.Combobox(window, values=["sin", "cos"])
    type_comboBox.place(x=50, y=15)

    # Amplitude label and entry
    amplitude_label = Label(window, text="amplitude", fg="black", font=("Arial", 12))
    amplitude_label.place(x=10, y=50)
    amplitude_entry = Entry(window, justify='center')
    amplitude_entry.place(x=90, y=56)

    # Analog frequency label and entry
    analogFrequency_label = Label(window, text="AnalogFrequency", fg="black", font=("Arial", 12))
    analogFrequency_label.place(x=10, y=90)
    analogFrequency_entry = Entry(window, justify='center')
    analogFrequency_entry.place(x=140, y=95)

    # Sampling frequency label and entry
    samplingFrequency_label = Label(window, text="SamplingFrequency", fg="black", font=("Arial", 12))
    samplingFrequency_label.place(x=10, y=130)
    samplingFrequency_entry = Entry(window, justify='center')
    samplingFrequency_entry.place(x=160, y=135)

    # Phase shift label and entry
    phaseShift_label = Label(window, text="PhaseShift", fg="black", font=("Arial", 12))
    phaseShift_label.place(x=10, y=170)
    phaseShift_entry = Entry(window, justify='center')
    phaseShift_entry.place(x=100, y=175)

    # Generate button
    generate_button = Button(window, text="Generate Signal", command=generate_signal_button_action)
    generate_button.place(x=10, y=210)

#----------------------------------------------------------------------------------------
#task 2  --------------------------------------------------------------------------------



# Main application window
root = Tk()
root.title("DSP Framework")
root.geometry("1000x650+100+100")

Main_label = Label(
    master=root, 
    text="DSP Framework",
    fg="black",
    font=("Arial", 16)
)
Main_label.place(x=0, y=10)

# Button to read signals
read_signals_button = Button(
    master=root,
    text="Read Signal",
    fg="black",
    bg="gray",
    font=("Arial", 12),
    width=15,
    activebackground="lightblue",
    command=read_window  # No parn ientheses here, passing the functiotself
)
read_signals_button.place(x=0, y=50)



generate_signal_button =  Button(
    master=root,
    text="generate signal",
    fg="black",
    bg="gray",
    font=("Arial",12),
    width=15,
    activebackground="lightblue",
    command= generate_signal_window
    )
generate_signal_button.place(x=0,y=90)

#task2
operations_signal_button =  Button(
    master=root,
    text="signal operations",
    fg="black",
    bg="gray",
    font=("Arial",12),
    width=15,
    activebackground="lightblue",
    command= operations_signal_window
    )
operations_signal_button.place(x=0,y=130)

#task 3
quantization_button =  Button(
    master=root,
    text="quantization",
    fg="black",
    bg="gray",
    font=("Arial",12),
    width=15,
    activebackground="lightblue",
    command= quantization_window
    )
quantization_button.place(x=0,y=170)

frequency_domain_button =  Button(
    master=root,
    text="frequency domain",
    fg="black",
    bg="gray",
    font=("Arial",12),
    width=15,
    activebackground="lightblue",
    command= frequency_domain_window
    )
frequency_domain_button.place(x=0,y=220)

task6_button =  Button(
    master=root,
    text="task 6",
    fg="black",
    bg="gray",
    font=("Arial",12),
    width=15,
    activebackground="lightblue",
    command= task6_window
    )
task6_button.place(x=0,y=270)

task7_button =  Button(
    master=root,
    text="fir filters",
    fg="black",
    bg="gray",
    font=("Arial",12),
    width=15,
    activebackground="lightblue",
    command= task7_window
    )
task7_button.place(x=0,y=270)

root.mainloop()