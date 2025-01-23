from tkinter import * 
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
from tkinter import filedialog
from tkinter import ttk

#backend task1-----------------------------------------------------------------
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

def Shift_Fold_Signal(file_name,Your_indices,Your_samples):      
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
            print("Shift_Fold_Signal Test case failed, your signal have different values from the expected one") 
            return
    print("Shift_Fold_Signal Test case passed successfully")

def DerivativeSignal_test():
    InputSignal =  [float(i) for i in range(1, 101)]
    expectedOutput_first = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    expectedOutput_second = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

    FirstDrev= []
    for n in range(1,len(InputSignal)):
        FirstDrev.append(InputSignal[n] - InputSignal[n-1])
    #print(FirstDrev)
    
    SecondDrev= []
    for n in range(1,len(InputSignal)-1):
        SecondDrev.append(InputSignal[n+1] - 2*InputSignal[n]+ InputSignal[n-1])
    #print(SecondDrev)
    
    if( (len(FirstDrev)!=len(expectedOutput_first)) or (len(SecondDrev)!=len(expectedOutput_second))):
        print("mismatch in length") 
        return
    first=second=True
    for i in range(len(expectedOutput_first)):
        if abs(FirstDrev[i] - expectedOutput_first[i]) < 0.01:
            continue
        else:
            first=False
            print("1st derivative wrong")
            return
    for i in range(len(expectedOutput_second)):
        if abs(SecondDrev[i] - expectedOutput_second[i]) < 0.01:
            continue
        else:
            second=False
            print("2nd derivative wrong") 
            return
    if(first and second):
        print("Derivative Test case passed successfully")
    else:
        print("Derivative Test case failed")
    return

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


#backend------------------------------

def re_index(df1,df2):
    

    df1.set_index(df1.columns[0], inplace=True)
    df2.set_index(df2.columns[0], inplace=True)


    common_start = int(min(df1.index.min(), df2.index.min()))
    common_end = int(max(df1.index.max(), df2.index.max()))


    full_index = pd.Index(range(common_start, common_end + 1))


    df1_reindexed = df1.reindex(full_index, fill_value=0)
    df2_reindexed = df2.reindex(full_index, fill_value=0)

    df1_reindexed.reset_index(inplace=True)
    df2_reindexed.reset_index(inplace=True)

    return df1_reindexed,df2_reindexed

#add two signals
def add_two_signals(df1: pd.DataFrame, df2: pd.DataFrame):
    df1=df1.copy()
    df2 = df2.copy()
    df1,df2 = re_index(df1,df2)

    result_df = pd.DataFrame()

    
    result_df['Index'] = df1.iloc[:, 0]  
    result_df['amplitude'] = df1.iloc[:, 1] + df2.iloc[:, 1]  

    return result_df

#subtract two signal
def subtract_two_signals(df1: pd.DataFrame, df2: pd.DataFrame):    
    # Create a new DataFrame to store the results
    df1=df1.copy()
    df2 = df2.copy()
    df1,df2 = re_index(df1,df2)

    result_df = pd.DataFrame()

    result_df['Index'] = df1.iloc[:, 0]  
    result_df['amplitude'] = (df1.iloc[:, 1] - df2.iloc[:, 1]).abs()

    return result_df

#Accumulation of input signal    
def accumulate_signal(data_signal:pd.DataFrame):
    
    data_signal = data_signal.copy()
    data_signal[data_signal.columns[1]] = data_signal[data_signal.columns[1]].cumsum()
    return data_signal

# Normalization: normalize the signal from -1 to 1 or 0 to 1 depending on user choice.
def normalize_signal(data_signal:pd.DataFrame,lower_range = 0,upper_range = 1):
    data_signal = data_signal.copy()  # no change in pramater

    if lower_range == 0:
        data_signal[data_signal.columns[1]] = (data_signal[data_signal.columns[1]] - 
                                               data_signal[data_signal.columns[1]].min()) / (
                                               data_signal[data_signal.columns[1]].max() -
                                               data_signal[data_signal.columns[1]].min())
    elif lower_range == -1:
        data_signal[data_signal.columns[1]] = 2 * (data_signal[data_signal.columns[1]] - 
                                                   data_signal[data_signal.columns[1]].min()) / (
                                                    data_signal[data_signal.columns[1]].max() - 
                                                    data_signal[data_signal.columns[1]].min()) - 1                                        
    return data_signal

#Squaring: squaring a signal and displaying the resulting signal.
def square_signal(data_signal:pd.DataFrame):
    data_signal = data_signal.copy()  # no change in pramater
    
    data_signal[data_signal.columns[1]] = data_signal[data_signal.columns[1]] ** 2
    return data_signal

#multiply a signal by a constant value to amplify or reduce the signal amplitude
def signalMultiplication(data_signal:pd.DataFrame,factor:int):
    data_signal = data_signal.copy()  # no change in pramater
    
    if factor == None:
        factor = 1

    data_signal[data_signal.columns[1]] = data_signal[data_signal.columns[1]] * factor
    return data_signal

#Sharpening: Compute and display y(n) which represents First Derivative of input signal or Second derivative of input signal 
def DerivativeSignal(values:list,type_drev:str):
    drev_results = []
    if type_drev == 'first':
        for n in range(1,len(values)):
            drev_results.append(values[n] - values[n-1])
    else:
        for n in range(1,len(values)-1):
            drev_results.append(values[n+1] - 2*values[n]+ values[n-1])

    return drev_results
        
def shift_right(k:int,index:list):
    new_index=[]
    for i in range(len(index)):
        new_index.append(index[i] - k)
    return new_index       

def shift_left(k:int,index:list):
    new_index=[]
    for i in range(len(index)):
        new_index.append(index[i] + k)
    return new_index

def fold_signel(signalValues:list):
    folded_signel_value = signalValues[::-1]
    return folded_signel_value

#gui-------------------------------------------------------------------------------------------------------------
def add_button_func():
    #take 2 signals
    path_signal1 = get_file_path()
    path_signal2 = get_file_path()
    
    #read content of 2 files
    lst_data1 = read_File(path_signal1)
    lst_data2 = read_File(path_signal2)

    df_signal1 =pd.DataFrame({"index":lst_data1[1],"amplitude":lst_data1[2]})
    df_signal2 =pd.DataFrame({"index":lst_data2[1],"amplitude":lst_data2[2]})

    result = add_two_signals(df1=df_signal1,df2=df_signal2)

    print(f"sig1 +sig2: " , SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task2\Output files\Signal1+signal2.txt",result[result.columns[0]],result[result.columns[1]]))
    print("sig1 +sig3: ", SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task2\Output files\signal1+signal3.txt",result[result.columns[0]],result[result.columns[1]]))
    
    path_save = get_save_file_path()
    write_file(filename=path_save,df=result,sampligFrequency=len(result))
    
def subtract_button_func():
    #take 2 signals
    path_signal1 = get_file_path()
    path_signal2 = get_file_path()
    
    #read content of 2 files
    lst_data1 = read_File(path_signal1)
    lst_data2 = read_File(path_signal2)

    df_signal1 =pd.DataFrame({"index":lst_data1[1],"amplitude":lst_data1[2]})
    df_signal2 =pd.DataFrame({"index":lst_data2[1],"amplitude":lst_data2[2]})

    result = subtract_two_signals(df1=df_signal1,df2=df_signal2)

    print("sig1 -sig2: ",SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task2\Output files\signal1-signal2.txt",result[result.columns[0]],result[result.columns[1]]))
    print("sig1 -sig3: ",SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task2\Output files\signal1-signal3.txt",result[result.columns[0]],result[result.columns[1]]))
    
    path_save = get_save_file_path()
    write_file(filename=path_save,df=result,sampligFrequency=len(result))

def mult_button_func():
    
    
    #take 2 signals
    path_signal1 = get_file_path()
    
    #read content of 2 files
    lst_data1 = read_File(path_signal1)
    
    df_signal1 =pd.DataFrame({"index":lst_data1[1],"amplitude":lst_data1[2]})
    
    result =signalMultiplication(df_signal1,factor=int(factor_entry.get()))
    
    print("sig1 x 5: ",SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task2\Output files\MultiplySignalByConstant-Signal1 - by 5.txt",result[result.columns[0]],result[result.columns[1]]))
    print("sig2 x 10: ",SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task2\Output files\MultiplySignalByConstant-signal2 - by 10.txt",result[result.columns[0]],result[result.columns[1]]))
    

    path_save = get_save_file_path()
    write_file(filename=path_save,df=result,sampligFrequency=len(result))

def accumulate_button_func():
    #take 1 signals
    path_signal1 = get_file_path()
    
    #read content of 1 files
    lst_data1 = read_File(path_signal1)

    df_signal1 =pd.DataFrame({"index":lst_data1[1],"amplitude":lst_data1[2]})

    result = accumulate_signal(df_signal1)

    print("sig1 accumulation: ",SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task2\Output files\output accumulation for signal1.txt",result[result.columns[0]],result[result.columns[1]]))

    path_save = get_save_file_path()
    write_file(filename=path_save,df=result,sampligFrequency=len(result))

def squaring_button_func():
    #take 1 signals
    path_signal1 = get_file_path()
    
    #read content of 1 files
    lst_data1 = read_File(path_signal1)

    df_signal1 =pd.DataFrame({"index":lst_data1[1],"amplitude":lst_data1[2]})

    result = square_signal(df_signal1)

    print("sig1 sqr: ",SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task2\Output files\Output squaring signal 1.txt",result[result.columns[0]],result[result.columns[1]]))

    path_save = get_save_file_path()
    write_file(filename=path_save,df=result,sampligFrequency=len(result))

def normalize_button_func():
    #take 1 signals
    path_signal1 = get_file_path()
    
    #read content of 1 files
    lst_data1 = read_File(path_signal1)

    df_signal1 =pd.DataFrame({"index":lst_data1[1],"amplitude":lst_data1[2]})

    result = normalize_signal(df_signal1,int(range_scale.get()))

    print("sig1 normal(-1 to 1): ",SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task2\Output files\normalize of signal 1 (from -1 to 1)-- output.txt",result[result.columns[0]],result[result.columns[1]]))
    print("sig2 normal(0 to 1): ",SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task2\Output files\normlize signal 2 (from 0 to 1 )-- output.txt",result[result.columns[0]],result[result.columns[1]]))
    
    
    path_save = get_save_file_path()
    write_file(filename=path_save,df=result,sampligFrequency=len(result))

def drev_button_func():
    DerivativeSignal_test()

    readed_list = read_File(get_file_path())
    drev_values = DerivativeSignal(readed_list[2],type_derv_comboBox.get())
    
    index_values = readed_list[1][:len(drev_values)]

    df_drev_values = pd.DataFrame({"index":index_values,"samples":drev_values})
    
    write_file(get_save_file_path(),df_drev_values,readed_list[0][2])

def shift_button_func():
    readed_list = read_File(get_file_path())
    shifted_indexes = []
    
    if type_shift_comboBox.get() == "right":
        shifted_indexes = shift_right(int(magnitude_shift_entery.get()),readed_list[1])
        SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task 5\shift\output shifting by minus 500.txt",shifted_indexes,readed_list[2])
    else:
        shifted_indexes = shift_left(int(magnitude_shift_entery.get()),readed_list[1])
        SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task 5\shift\output shifting by add 500.txt",shifted_indexes,readed_list[2])
    
    df_shifted = pd.DataFrame({"index":shifted_indexes,"samples":readed_list[2]})
    write_file(get_save_file_path(),df=df_shifted, sampligFrequency=len(df_shifted))

def fold_button_func():
    readed_list = read_File(get_file_path())
    fold_values = []
    
    fold_values = fold_signel(readed_list[2])
    SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task 5\Shifting and Folding\Output_fold.txt",readed_list[1],fold_values)
    
    df_folded = pd.DataFrame({"index":readed_list[1],"samples":fold_values})
    write_file(get_save_file_path(),df=df_folded, sampligFrequency=len(df_folded))

def shift_fold_button_func():
    readed_list = read_File(get_file_path())
    shifted_indexes = []
    fold_values = []
    
    fold_values = fold_signel(readed_list[2])
    SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task 5\Shifting and Folding\Output_fold.txt",readed_list[1],fold_values)

    if type_shiftFold_comboBox.get() == "right":
        shifted_indexes = shift_right(int(magnitude_shiftFold_entery.get()),readed_list[1])
        SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task 5\shift\output shifting by minus 500.txt",shifted_indexes,readed_list[2])
        Shift_Fold_Signal(r"C:\Users\HP\Desktop\dsp\task 5\Shifting and Folding\Output_ShiftFoldedby-500.txt",shifted_indexes,fold_values)
    else:
        shifted_indexes = shift_left(int(magnitude_shiftFold_entery.get()),readed_list[1])
        SignalSamplesAreEqual(r"C:\Users\HP\Desktop\dsp\task 5\shift\output shifting by add 500.txt",shifted_indexes,readed_list[2])
        Shift_Fold_Signal(r"C:\Users\HP\Desktop\dsp\task 5\Shifting and Folding\Output_ShifFoldedby500.txt",shifted_indexes,fold_values)
    
    df_shifted_folded = pd.DataFrame({"index":shifted_indexes,"samples":fold_values})
    write_file(get_save_file_path(),df=df_shifted_folded, sampligFrequency=len(df_shifted_folded))


def operations_signal_window():
    window = Tk()
    window.geometry("750x750")

    global factor_entry,range_scale,type_derv_comboBox,type_shift_comboBox,magnitude_shift_entery,type_shiftFold_comboBox,magnitude_shiftFold_entery

    add_button = Button(window, text="adding 2 signals",fg="black",bg="gray",activebackground="lightblue", command=add_button_func)
    add_button.place(x=10, y=10)
    #----------------
    subtract_button = Button(window, text="subtract 2 signals",fg="black",bg="gray",activebackground="lightblue", command=subtract_button_func)
    subtract_button.place(x=10, y=50)

    #mult--------------------
    factor_label = Label(window, text="enter the factor then click on multiplication button", fg="black")
    factor_label.place(x=10, y=90)
    factor_entry = Entry(window, justify='center')
    factor_entry.place(x=10, y=120)

    multiplication_button = Button(window, text="mutiplication signal",fg="black",bg="gray",activebackground="lightblue", command=mult_button_func)
    multiplication_button.place(x=150, y=120)
    #-----------------
    accumulate_button = Button(window, text="accumulate signal",fg="black",bg="gray",activebackground="lightblue", command=accumulate_button_func)
    accumulate_button.place(x=10, y=150)
    #----------------
    squaring_button = Button(window, text="squaring signal",fg="black",bg="gray",activebackground="lightblue", command=squaring_button_func)
    squaring_button.place(x=10, y=190)
    #----------------
    range_label = Label(window, text="select the lower range only and the upper range is 1 by default then click on normalize signal button", fg="black")
    range_label.place(x=10, y=230)
    range_scale = Scale(window, from_= -1, to=0,orient=HORIZONTAL)
    range_scale.place(x=10, y=250)

    normalize_button = Button(window, text="normalize signal",fg="black",bg="gray",activebackground="lightblue", command=normalize_button_func)
    normalize_button.place(x=10, y=300)
    #----------------

    derv_label = Label(window, text="select type of derivative then click on derivative signal button", fg="black")
    derv_label.place(x=10, y=330)

    type_derv_comboBox = ttk.Combobox(window, values=["first", "second"])
    type_derv_comboBox.place(x = 10, y = 360)

    derv_button = Button(window, text="derivative signal",fg="black",bg="gray",activebackground="lightblue", command=drev_button_func)
    derv_button.place(x=10, y=390)

    #----------------
    shift_label = Label(window, text="select type of shift and enter the magnitude then click on shift signal button", fg="black")
    shift_label.place(x=10, y=430)

    type_shift_comboBox = ttk.Combobox(window, values=["left", "right"])
    type_shift_comboBox.place(x = 10, y = 460)

    magnitude_shift_entery = Entry(window, justify='center')
    magnitude_shift_entery.place(x = 180, y = 460)

    shift_button = Button(window, text="shift signal",fg="black",bg="gray",activebackground="lightblue", command=shift_button_func)
    shift_button.place(x=10, y=490)
    #----------------

    fold_label = Label(window, text=" click on fold signal button", fg="black")
    fold_label.place(x=10, y=530)
    
    fold_button = Button(window, text="fold signal",fg="black",bg="gray",activebackground="lightblue", command=fold_button_func)
    fold_button.place(x=170, y=530)
    #-----------------

    shift_fold_label = Label(window, text="select type of shift and enter the magnitude then click on shift fold signal button", fg="black")
    shift_fold_label.place(x=10, y=560)

    type_shiftFold_comboBox = ttk.Combobox(window, values=["left", "right"])
    type_shiftFold_comboBox.place(x = 10, y = 590)

    magnitude_shiftFold_entery = Entry(window, justify='center')
    magnitude_shiftFold_entery.place(x = 180, y = 590)

    shift_Fold_button = Button(window, text="shift fold signal",fg="black",bg="gray",activebackground="lightblue", command=shift_fold_button_func)
    shift_Fold_button.place(x=10, y=630)
