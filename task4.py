from tkinter import * 
import pandas as pd
from tkinter import filedialog
from tkinter import ttk
import math

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

#write
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
    #for index, row in df.iterrows():
    #    myFile.write(f"{row[0]} {row[1]}\n")
    #myFile.close()
    for index, row in df.iterrows():
        row_values = " ".join(str(value) for value in row)
        myFile.write(f"{row_values}\n")

def SignalSamplesAreEqual(file_name,indices,samples):
    expected_indices=[]
    expected_samples=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==2:
                L=line.split(' ')
                V1=int(L[0])
                V2=float(L[1])
                expected_indices.append(V1)
                expected_samples.append(V2)
                line = f.readline()
            else:
                break
                
    if len(expected_samples)!=len(samples):
        print("Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(expected_samples)):
        if abs(samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Test case failed, your signal have different values from the expected one") 
            return
    print("Test case passed successfully")

def compute_dct(input_data, m):
    N = len(input_data)
    dct_result = []

    for k in range(N):  # Iterate over k from 1 to N
        dct_sum = 0
        for n in range(N):  # Iterate over n from 1 to N
            angle = (180 / (4 * N)) * (2 * n - 1) * (2 * k - 1)
            dct_sum += input_data[n] * math.cos(math.radians(angle))
        y_k = float(math.sqrt(2 / N) * dct_sum)  # Use N (total input length) for normalization
        dct_result.append(y_k)   
    index_list =[0 for i in range(m)]

    return pd.DataFrame({"index":index_list, "samples":dct_result[:m]})   # Return only the first m coefficients

def dct_button_func():
    #read_file_path = get_file_path()
    readed_list = read_File(get_file_path())

    m = int(number_enter.get())
    df_dct_values = compute_dct(readed_list[2],m = m)
    
    SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task 5\DCT\DCT_output.txt",df_dct_values[df_dct_values.columns[0]],df_dct_values[df_dct_values.columns[1]])
    write_file(get_save_file_path(),df=df_dct_values,sampligFrequency = m,signalType=0,isPeriodic=1)


def frequency_domain_window():
    window = Tk()
    window.geometry("750x650")

    global number_enter

    label1 = Label(window, text="choose the first m coefficients to be saved in txt file.", fg="black")
    label1.place(x=10, y=10)
    
    number_enter = Entry(window, justify='center')
    number_enter.place(x = 300, y = 10)


    excute_button =  Button(window, text="compute_dct",fg="black",bg="gray",activebackground="lightblue", command=dct_button_func)
    excute_button.place(x=10, y=160)