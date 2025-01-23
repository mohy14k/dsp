from tkinter import * 
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from tkinter import filedialog
from tkinter import ttk



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


def write_file(filename:str,df:pd.DataFrame,sampligFrequency:float,signalType:int=0,isPeriodic:int=0):
    myFile = open(filename,"w")
    myFile.write(f"{signalType}\n")
    myFile.write(f"{isPeriodic}\n")
    myFile.write(f"{sampligFrequency}\n")
        
        # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        myFile.write(f"{row[0]} {row[1]}\n")
    myFile.close()

def get_save_file_path():
    
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",  # Default extension is now .txt
        filetypes=[("Text files", "*.txt"), ("All files", "*.*")]
    )
    return file_path



def generate_signal(type: str, amplitude: float, phaseShift: float, analogFrequency: float, SamplingFrequency: float):
    # sin(2pi n fa/fs + theta)
    digital_frequency = analogFrequency / SamplingFrequency
    indexes = np.arange(0, SamplingFrequency)
    if type == 'cos':
        result = amplitude * np.cos(2 * np.pi * digital_frequency *
                                    indexes + phaseShift)
    else:
        result = amplitude * np.sin(2 * np.pi * digital_frequency *
                                    indexes + phaseShift)
    return pd.DataFrame({'index': indexes, 'result': result})

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

    window.mainloop()

# Call the window function to show the GUI
generate_signal_window()
