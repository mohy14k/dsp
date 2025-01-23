import pandas as pd
import math
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from task4 import get_file_path,read_File,get_save_file_path,write_file
from task6 import convolve_signals

#test function 
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
#    print(len(expected_samples),(len(expected_indices)))
    if (len(expected_samples)!=len(Your_samples)) and (len(expected_indices)!=len(Your_indices)):
        print("Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_indices)):
        if(Your_indices[i]!=expected_indices[i]):
            print("Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(expected_samples)):
        if abs(Your_samples[i] - expected_samples[i]) < 0.01:
            continue
        else:
            print("Test case failed, your signal have different values from the expected one") 
            return
    print("Test case passed successfully")


# backend functions

def get_window_method(StopBandAttenuation):
    #1 -> rectangular, 2-> hanning, 3-> hamming, 4-> blackman
    if StopBandAttenuation >= 0 and StopBandAttenuation <= 21 :
        return 1
    if StopBandAttenuation >= 22 and StopBandAttenuation <= 44 :
        return 2
    if StopBandAttenuation >= 45 and StopBandAttenuation <= 53 :
        return 3
    if StopBandAttenuation >= 54 and StopBandAttenuation <= 74 :
        return 4

def get_N(fs,delta_f,window_method_num):
    normal_delta_f = float(delta_f/fs)
    N = 0
    
    if window_method_num == 1:#rectangular
        N = 0.9/normal_delta_f
    elif window_method_num == 2:#hanning
        N = 3.1/normal_delta_f
    elif window_method_num == 3:#hamming
        N = 3.3/normal_delta_f
    elif window_method_num == 4:#blackman
        N = 5.5/normal_delta_f
    
    if(int(N) % 2 == 0):
        N=int(N) + 1
    else:
        N=int(N)
    
    return N

def get_window_value(N,n,window_method_num):
    
    result = 0.0

    if window_method_num == 1:#rectangular
        result = 1.0    
    elif window_method_num == 2:#hanning
        rad = math.radians(float((2*180*n)/N))
        result = 0.5 + (0.5 * math.cos(rad))
    elif window_method_num == 3:#hamming
        rad = math.radians(float(2 * 180 * n/N))
        result = 0.54 + (0.46 * math.cos(rad))
    elif window_method_num == 4:#blackman
        rad1 = math.radians(float(2 * 180 * n / (N-1)))
        rad2 = math.radians(4 * 180 * n / (N-1))
        result = 0.42 + (0.5 * math.cos(rad1)) + (0.08 * math.cos(rad2))
                    
    return result    

def semetric_list(lst:list):
    l = lst[:0:-1]
    #print(l)
    l.extend(lst)
    #print(l)
    return l

#FIR Filters
def lowPass_filter(fs, fp, delta_f,StopBandAttenuation):
    impulse_values = []
    #find window method
    method_num = get_window_method(StopBandAttenuation)
    #print(method_num)
    
    #find N
    N = get_N(fs ,delta_f,method_num)
    max_iteration = int(N/2)

    #find norm_fc
    fc1 = fp + (delta_f/2)
    norm_fc = float(fc1/fs)
    
    #print(N,max_iteration)
    
    Hd_value = 2 * norm_fc
    Wn_value = get_window_value(N,0,method_num)
    impulse_values.append(Hd_value * Wn_value)
    #print(Hd_value * Wn_value)
    
    for n in range(1,max_iteration+1):
        rad = math.radians(n*2*180*norm_fc) 
        Hd_value = 2 * norm_fc * math.sin(rad) /(n * 2*math.pi*norm_fc)
        Wn_value = get_window_value(N,n,method_num)
        #print(Hd_value,Wn_value)
        impulse_values.append(Hd_value*Wn_value)
        #print(n)
        #print(Hd_value * Wn_value)
    impulse_values=semetric_list(impulse_values)
    
    index = [i for i in range(-max_iteration,max_iteration+1) ]
    #print (index)
    
    return impulse_values, index

def highPass_filter(fs, fp, delta_f,StopBandAttenuation):
    impulse_values = []
    #find window method
    method_num = get_window_method(StopBandAttenuation)
    #print(method_num)
    
    #find N
    N = get_N(fs ,delta_f,method_num)
    max_iteration = int(N/2)

    #find norm_fc
    fc1 = fp - (delta_f/2)
    norm_fc = float(fc1/fs)
    
    #print(N,max_iteration)
    
    Hd_value = 1 - 2 * norm_fc
    Wn_value = get_window_value(N,0,method_num)
    impulse_values.append(Hd_value * Wn_value)
    #print(Hd_value * Wn_value)
    
    for n in range(1,max_iteration+1):
        rad = math.radians(n*2*180*norm_fc) 
        Hd_value = -2 * norm_fc * math.sin(rad) /(n * 2*math.pi*norm_fc)
        Wn_value = get_window_value(N,n,method_num)
        impulse_values.append(Hd_value*Wn_value)
        
    impulse_values=semetric_list(impulse_values)
    
    index = [i for i in range(-max_iteration,max_iteration+1) ]
    
    
    return impulse_values, index

def bandPass_filter(fs, fp1,fp2, delta_f,StopBandAttenuation):
    impulse_values = []
    #find window method
    method_num = get_window_method(StopBandAttenuation)
    #print(method_num)
    
    #find N
    N = get_N(fs ,delta_f,method_num)
    max_iteration = int(N/2)

    #find norm_fc
    fc1 = fp1 - (delta_f/2)
    norm_fc1 = float(fc1/fs)
    
    fc2 = fp2 + (delta_f/2)
    norm_fc2 = float(fc2/fs)
    
    #print(N,max_iteration)
    
    Hd_value =  2 * (norm_fc2-norm_fc1)
    Wn_value = get_window_value(N,0,method_num)
    impulse_values.append(Hd_value * Wn_value)
    #print(Hd_value * Wn_value)
    
    for n in range(1,max_iteration+1):
        rad1 = math.radians(n*2*180*norm_fc1)
        rad2 = math.radians(n*2*180*norm_fc2)

        Hd_value = (2*norm_fc2* math.sin(rad2)/(n * 2*math.pi*norm_fc2)) - (2*norm_fc1* math.sin(rad1)/(n * 2*math.pi*norm_fc1))
        Wn_value = get_window_value(N,n,method_num)
        impulse_values.append(Hd_value*Wn_value)
        
    impulse_values=semetric_list(impulse_values)
    
    index = [i for i in range(-max_iteration,max_iteration+1) ]
    
    
    return impulse_values, index

def bandStop_filter(fs, fp1,fp2, delta_f,StopBandAttenuation):
    impulse_values = []
    #find window method
    method_num = get_window_method(StopBandAttenuation)
    #print(method_num)
    
    #find N
    N = get_N(fs ,delta_f,method_num)
    max_iteration = int(N/2)

    #find norm_fc
    fc1 = fp1 + (delta_f/2)
    norm_fc1 = float(fc1/fs)
    
    fc2 = fp2 - (delta_f/2)
    norm_fc2 = float(fc2/fs)
    
    #print(N,max_iteration)
    
    Hd_value = 1- 2 * (norm_fc2-norm_fc1)
    Wn_value = get_window_value(N,0,method_num)
    impulse_values.append(Hd_value * Wn_value)
    #print(Hd_value * Wn_value)
    
    for n in range(1,max_iteration+1):
        rad1 = math.radians(n*2*180*norm_fc1)
        rad2 = math.radians(n*2*180*norm_fc2)

        Hd_value = (2*norm_fc1* math.sin(rad1)/(n * 2*math.pi*norm_fc1)) - (2*norm_fc2* math.sin(rad2)/(n * 2*math.pi*norm_fc2))
        Wn_value = get_window_value(N,n,method_num)
        impulse_values.append(Hd_value*Wn_value)
        
    impulse_values=semetric_list(impulse_values)
    
    index = [i for i in range(-max_iteration,max_iteration+1) ]
    
    
    return impulse_values, index

#resampling
def resampling_down(input_index:list , input_samples_values:list,m:int,fs, fp, delta_f,StopBandAttenuation):
    resampled_sample_values = []
    resampled_indices =[]
    #apply filter
    h,lpf_index = lowPass_filter(fs,fp,delta_f,StopBandAttenuation)
    
    indices , sample_values = convolve_signals(input_index, input_samples_values,lpf_index,h)
    
    #down sample by M factor
    resampled_sample_values = sample_values[::m]

    resampled_indices = [i+indices[0] for i in range(len(resampled_sample_values))]
    
    return resampled_indices , resampled_sample_values

def resampling_up(input_index:list , input_samples_values:list,l:int,fs, fp, delta_f,StopBandAttenuation):
    resampled_sample_values = []
    resampled_indices =[]

    #apply up sample by L factor
    for i in input_samples_values:
        resampled_sample_values.append(i)
        
        for j in range(l-1):
            resampled_sample_values.append(0)
    
    resampled_sample_values = resampled_sample_values[:len(resampled_sample_values)-l+1]
    resampled_indices = [i for i in range(len(resampled_sample_values))]

    #print(resampled_indices)
    #print(resampled_sample_values)

    #apply filter
    h,lpf_index = lowPass_filter(fs,fp,delta_f,StopBandAttenuation)
    
    resampled_indices , resampled_sample_values = convolve_signals(resampled_indices, resampled_sample_values,lpf_index,h)

    #print(resampled_indices)
    #print(resampled_sample_values)

    #print(len(resampled_indices))
    #print(len(resampled_sample_values))
    #resampled_sample_values = resampled_sample_values[:len(resampled_sample_values)-l+1]
    #resampled_indices = resampled_indices[:len(resampled_indices)-l+1]
    return resampled_indices,resampled_sample_values

def resampling_upAndDown(input_index:list , input_samples_values:list,l:int,m:int,fs, fp, delta_f,StopBandAttenuation):
    resampled_up_indices , resampled_up_samples = resampling_up(input_index, input_samples_values, l, fs, fp, delta_f, StopBandAttenuation)
    
    #print(resampled_up_indices)
    #print(resampled_up_samples)
    #print(len(resampled_up_indices))
    #print(len(resampled_up_samples))
    
    #down sampling
    s = resampled_up_samples[::m]
    isd = [i+resampled_up_indices[0] for i in range(len(s))]
    
    #print(isd)
    #print(s)
    #print(len(isd))
    #print(len(s))
    
    return  isd, s

#gui functions
def get_impulse_values(fs,fp,fp2,delta_f,StopBandAttenuation):
    impulse_values = []
    impulse_indices = []
    
    if filter_comboBox.get() == "low pass":
        impulse_values, impulse_indices = lowPass_filter(fs,fp,delta_f,StopBandAttenuation)
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\FIR test cases\Testcase 1\LPFCoefficients.txt", impulse_indices, impulse_values)
    elif filter_comboBox.get() == "high pass":
        impulse_values, impulse_indices = highPass_filter(fs,fp,delta_f,StopBandAttenuation)
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\FIR test cases\Testcase 3\HPFCoefficients.txt", impulse_indices, impulse_values)
    elif filter_comboBox.get() == "band pass":
        impulse_values, impulse_indices = bandPass_filter(fs,fp,fp2,delta_f,StopBandAttenuation)
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\FIR test cases\Testcase 5\BPFCoefficients.txt", impulse_indices, impulse_values)
    elif filter_comboBox.get() == "band stop":
        impulse_values, impulse_indices = bandStop_filter(fs,fp,fp2,delta_f,StopBandAttenuation)
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\FIR test cases\Testcase 7\BSFCoefficients.txt", impulse_indices, impulse_values)

    return impulse_indices,impulse_values

def impulse_button_func(): 
    fs = float(fs_entry.get())
    StopBandAttenuation = float(StopBandAttenuation_entry.get())
    fp = float(fp_entry.get())
    if fp2_entry.get() == '' or fp2_entry.get() == None:
        fp2 = 0
    else:
        fp2= float(fp2_entry.get())
    delta_f = float(delta_f_entry.get())
    
    impulse_values = []
    impulse_indices = []

    impulse_indices, impulse_values = get_impulse_values(fs,fp,fp2,delta_f,StopBandAttenuation)
    
    data = pd.DataFrame({
        "indices":impulse_indices,
        "samples":impulse_values
    })
    write_file(get_save_file_path(),data,len(data))

def filtering_button_func():
    readed_signal = read_File(get_file_path())

    fs = float(fs_entry.get())
    StopBandAttenuation = float(StopBandAttenuation_entry.get())
    fp = float(fp_entry.get())
    fp2 = float(fp2_entry.get())
    delta_f = float(delta_f_entry.get())
    

    impulse_indices, impulse_values = get_impulse_values(fs,fp,fp2,delta_f,StopBandAttenuation)
    
    filtered_indices, filtered_values = convolve_signals(readed_signal[1],readed_signal[2],impulse_indices,impulse_values)
    
    if filter_comboBox.get() == "low pass":
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\FIR test cases\Testcase 2\ecg_low_pass_filtered.txt",filtered_indices,filtered_values)
    elif filter_comboBox.get() == "high pass":
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\FIR test cases\Testcase 4\ecg_high_pass_filtered.txt",filtered_indices,filtered_values)
    elif filter_comboBox.get() == "band pass":
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\FIR test cases\Testcase 6\ecg_band_pass_filtered.txt",filtered_indices,filtered_values)
    elif filter_comboBox.get() == "band stop":
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\FIR test cases\Testcase 8\ecg_band_stop_filtered.txt",filtered_indices,filtered_values)

    data = pd.DataFrame({
        "indices":filtered_indices,
        "samples":filtered_values
    })
    write_file(get_save_file_path(),data,len(data))

def resampling_button_func():
    readed_signal = read_File(get_file_path())
    
    fs = float(fs_entry.get())
    StopBandAttenuation = float(StopBandAttenuation_entry.get())
    fp = float(fp_entry.get())
    delta_f = float(delta_f_entry.get())
    m = int(M_entry.get())
    l = int(L_entry.get())

    resampled_indices = []
    resampled_values = []

    if l == 0 and m != 0:#upSampling
        resampled_indices,resampled_values = resampling_up(readed_signal[1], readed_signal[2], l, fs, fp, delta_f, StopBandAttenuation)
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\sampling test cases\Testcase 2\Sampling_Up.txt",resampled_indices,resampled_values)
    elif l != 0 and m == 0:#downSampling
        resampled_indices,resampled_values = resampling_down(readed_signal[1], readed_signal[2], m, fs, fp, delta_f, StopBandAttenuation)
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\sampling test cases\Testcase 1\Sampling_Down.txt",resampled_indices,resampled_values)
    elif l != 0 and m != 0:#up and down Sampling
        resampled_indices,resampled_values = resampling_upAndDown(readed_signal[1], readed_signal[2],l, m, fs, fp, delta_f, StopBandAttenuation)
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\sampling test cases\Testcase 3\Sampling_Up_Down.txt",resampled_indices,resampled_values)
        Compare_Signals(r"C:\Users\HP\Desktop\dsp\task7\sampling test cases\Testcase 3\Sampling_Up_Down1.txt",resampled_indices,resampled_values)
    else:
        print("error")
    
    data = pd.DataFrame({
        "indices":resampled_indices,
        "samples":resampled_values
    })
    write_file(get_save_file_path(),data,len(data))







#window function
def task7_window():
    window = Tk()
    window.geometry("750x650")

    global filter_comboBox, fs_entry, StopBandAttenuation_entry, fp_entry,fp2_entry, delta_f_entry,M_entry,L_entry

    label1 = Label(window, text="choose filter and its specifications first.", fg="black")
    label1.place(x=10, y=10)
    
    filter_comboBox = ttk.Combobox(window, values=["low pass", "high pass","band pass","band stop"])
    filter_comboBox.place(x = 130, y = 40)
    
    label2 = Label(window, text="choose the filter.", fg="black")
    label2.place(x = 10, y = 40)

    label3 = Label(window, text="enter FS.", fg="black")
    label3.place(x = 10, y = 70)

    fs_entry = Entry(window, justify='center')
    fs_entry.place(x = 130, y = 70)

    label4 = Label(window, text="enter StopBandAttenuation.", fg="black")
    label4.place(x = 10, y = 100)

    StopBandAttenuation_entry = Entry(window, justify='center')
    StopBandAttenuation_entry.place(x = 180, y = 100)

    label5 = Label(window, text="enter FC1.", fg="black")
    label5.place(x = 10, y = 130)

    fp_entry = Entry(window, justify='center')
    fp_entry.place(x = 130, y = 130)


    label5 = Label(window, text="enter FC2.", fg="black")
    label5.place(x = 10, y = 160)

    fp2_entry = Entry(window, justify='center')
    fp2_entry.place(x = 130, y = 160)

    #TransitionBand
    label6 = Label(window, text="enter TransitionBand.", fg="black")
    label6.place(x = 10, y = 190)

    delta_f_entry = Entry(window, justify='center')
    delta_f_entry.place(x = 130, y = 190)
    
    label6 = Label(window, text="to get impulse response of the filter click on imuplse response button. ", fg="black")
    label6.place(x = 10, y = 220)
    
    impulse_button =  Button(window, text="impulse response",fg="black",bg="gray",activebackground="lightblue", command=impulse_button_func)
    impulse_button.place(x=10, y=250)
    
    label6 = Label(window, text="to get samples after filtering  click on filtering button. ", fg="black")
    label6.place(x = 10, y = 280)
    
    filtering_button =  Button(window, text="filtering",fg="black",bg="gray",activebackground="lightblue", command=filtering_button_func)
    filtering_button.place(x=10, y=310)
    
    label6 = Label(window, text="------------------------------------------------------------------------------------------------------------------------------------------", fg="black")
    label6.place(x = 10, y = 340)

#resample part
    label7 = Label(window, text="resampling: pls enter the filter specifications and the filter is low pass by default \nthen enter M and L values then click on resampling", fg="black")
    label7.place(x = 10, y = 370)

    label7 = Label(window, text="enter M factor.", fg="black")
    label7.place(x = 10, y = 420)

    M_entry = Entry(window, justify='center')
    M_entry.place(x = 130, y = 420)
    
    label7 = Label(window, text="enter L factor.", fg="black")
    label7.place(x = 10, y = 450)

    L_entry = Entry(window, justify='center')
    L_entry.place(x = 130, y = 450)

    resampling_button =  Button(window, text="resampling",fg="black",bg="gray",activebackground="lightblue", command=resampling_button_func)
    resampling_button.place(x=10, y=480)
        

    

    


    

    