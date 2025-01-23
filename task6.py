import math
import numpy as np
import pandas as pd
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from task4 import get_file_path,read_File,get_save_file_path,write_file
#---- tests
def Compare_Signals(file_name,Your_indices,Your_samples):      
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
    print("Current Output Test file is: ")
    print(file_name)
    print("\n")
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Shift_Fold_Signal Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Shift_Fold_Signal Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Correlation Test case failed, your signal have different values from the expected one") 
            return
    print("Correlation Test case passed successfully")

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

def ConvTest(Your_indices,Your_samples): 
    """
    Test inputs
    InputIndicesSignal1 =[-2, -1, 0, 1]
    InputSamplesSignal1 = [1, 2, 1, 1 ]
    
    InputIndicesSignal2=[0, 1, 2, 3, 4, 5 ]
    InputSamplesSignal2 = [ 1, -1, 0, 0, 1, 1 ]
    """
    
    expected_indices=[-2, -1, 0, 1, 2, 3, 4, 5, 6]
    expected_samples = [1, 1, -1, 0, 0, 3, 3, 2, 1 ]

    
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Conv Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Conv Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Conv Test case failed, your signal have different values from the expected one") 
            return
    print("Conv Test case passed successfully")

#backend--------------------------------------

# smoothing
def moving_avg(signal:list,window_size:int):
    num_it = len(signal[2]) - window_size + 1    
    results = []
    for i in range(num_it):
        avg = 0.0
        for j in range(window_size):
            avg += signal[2][i+j]
        results.append(avg / window_size )
    index = signal[1][:len(signal[1]) - window_size +1]
    return index,results

#dc remove
def remove_dc_time_domain(signal_values:list):
    new_signal__values =[]
    sum_list=sum(signal_values)
    
    dc = float(sum_list / len(signal_values))

    for i in signal_values:
        new_signal__values.append(round(i - dc,3))
    
    return new_signal__values


def remove_dc_Frequency_domain(signal_values:list):
    fft_signal = np.fft.fft(signal_values)
    
    fft_signal[0] = 0 #1st ele is dc to remove it make it 0

    no_dc_signal = np.round(np.fft.ifft(fft_signal).real, 3)
    return no_dc_signal

#convolve_signals
def convolve_signals(indices1, samples1, indices2, samples2):

    indices1 = [int(idx) for idx in indices1]
    indices2 = [int(idx) for idx in indices2]

    output_indices = list(range(indices1[0] + indices2[0], indices1[-1] + indices2[-1] + 1))
    
    # Initialize the output samples with zero values
    output_samples = [0] * len(output_indices)
    
    # Perform the convolution
    for i, index in enumerate(output_indices):
        for j, idx1 in enumerate(indices1):
            for k, idx2 in enumerate(indices2):
                if idx1 + idx2 == index:
                    output_samples[i] += samples1[j] * samples2[k]
    
    return output_indices, output_samples

#corrlation
def auto_correlation(x1:list,x2:list,j:int):
    N = len(x1)
    
    sum_product =0
    for n in range(N): 
            
        sum_product += x1[n] * x2[(n + j) % N]
    
   
    return sum_product/N

def cross_correlation(x1:list,x2:list,j:int):
    r  = auto_correlation(x1,x2,j)
    sum_x1 = 0 
    sum_x2 = 0
    for i in range(len(x1)):
        sum_x1 += x1[i] ** 2
        sum_x2 += x2[i] ** 2
    root_sum = math.sqrt(sum_x1 * sum_x2)
    #return  round(  r/(root_sum / len(x1)) , 5)
    return r/(root_sum / len(x1))

def cross_correlation_list(x1:list,x2:list):
    results = []
    for i in range(len(x1)):
        results.append(cross_correlation(x1,x2,i))
    return results

#------------- gui func
def smooting_signal_func():
    readed_lst = read_File(get_file_path())
    index,sample_values = moving_avg(readed_lst,int(window_size_entry.get()))
    
    Compare_Signals(r"C:\Users\HP\Desktop\dsp\task6\Moving Average\OutMovAvgTest1.txt",index,sample_values)
    Compare_Signals(r"C:\Users\HP\Desktop\dsp\task6\Moving Average\OutMovAvgTest2.txt",index,sample_values)

    df_signal1 =pd.DataFrame({"index":index,"amplitude":sample_values})

    write_file(get_save_file_path(),df_signal1,len(df_signal1))

def remove_dc_func():
    readed_lst = read_File(get_file_path())
    values_without_dc = []
    
    if type_domin_comboBox.get() == "time":
        values_without_dc = remove_dc_time_domain(readed_lst[2])
    else:
        values_without_dc = remove_dc_Frequency_domain(readed_lst[2])
    SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task6\Remove DC component\DC_component_output.txt",readed_lst[1],values_without_dc)
    
    df_signal1 =pd.DataFrame({"index":readed_lst[1],"amplitude":values_without_dc})

    write_file(get_save_file_path(),df_signal1,len(df_signal1))

def conv_button_func():
    
    readed_lst1 = read_File(get_file_path())
    readed_lst2 = read_File(get_file_path())

    result_convelution = convolve_signals(readed_lst1[1], readed_lst1[2], readed_lst2[1], readed_lst2[2])
    ConvTest(result_convelution[0], result_convelution[1])

    df_signal1 =pd.DataFrame({"index":result_convelution[0],"amplitude":result_convelution[1]})

    write_file(get_save_file_path(),df_signal1,len(df_signal1))

def corr_button_func():
    readed_lst1 = read_File(get_file_path())
    readed_lst2 = read_File(get_file_path())

    corr_results = cross_correlation_list(readed_lst1[2],readed_lst2[2])
    Compare_Signals(r"C:\Users\HP\Desktop\dsp\task6\Point1 Correlation\CorrOutput.txt",readed_lst2[1],corr_results)

    df_signal1 =pd.DataFrame({"index":readed_lst2[1],"amplitude":corr_results})

    write_file(get_save_file_path(),df_signal1,len(df_signal1))



#---------window
def task6_window():
    window = Tk()
    window.geometry("750x650")

    global window_size_entry,type_domin_comboBox

    label1 = Label(window, text="enter the window size then click on smooth signal", fg="black")
    label1.place(x=10, y=10)
    
    window_size_entry = Entry(window, justify='center')
    window_size_entry.place(x = 300, y = 10)


    smoothing_button =  Button(window, text="smooth signal",fg="black",bg="gray",activebackground="lightblue", command=smooting_signal_func)
    smoothing_button.place(x=10, y=50)
    #----- dc
    
    label2 = Label(window, text="enter the signal domian type then click on remove dc button", fg="black")
    label2.place(x=10, y=80)
    
    type_domin_comboBox = ttk.Combobox(window, values=["time", "frequency"])
    type_domin_comboBox.place(x = 340, y = 80)
    

    dc_button =  Button(window, text="remove dc",fg="black",bg="gray",activebackground="lightblue", command=remove_dc_func)
    dc_button.place(x=10, y=120)

    #---- convolution
    label3 = Label(window, text="click on convolution button the select 2 signals", fg="black")
    label3.place(x=10, y=150)

    conv_button =  Button(window, text="convolution",fg="black",bg="gray",activebackground="lightblue", command=conv_button_func)
    conv_button.place(x=10, y=190)

    #--- corr
    label4 = Label(window, text="click on correlation button the select 2 signals", fg="black")
    label4.place(x=10, y=220)

    corr_button =  Button(window, text="correlation",fg="black",bg="gray",activebackground="lightblue", command=corr_button_func)
    corr_button.place(x=10, y=260)



