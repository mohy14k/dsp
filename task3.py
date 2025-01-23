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


def QuantizationTest1(file_name,Your_EncodedValues,Your_QuantizedValues):
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
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
                V2=str(L[0])
                V3=float(L[1])
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                line = f.readline()
            else:
                break
    if( (len(Your_EncodedValues)!=len(expectedEncodedValues)) or (len(Your_QuantizedValues)!=len(expectedQuantizedValues))):
        print("QuantizationTest1 Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_EncodedValues)):
        if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
            print("QuantizationTest1 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
            return
    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
            continue
        else:
            print("QuantizationTest1 Test case failed, your QuantizedValues have different values from the expected one") 
            return
    print("QuantizationTest1 Test case passed successfully")

def QuantizationTest2(file_name,Your_IntervalIndices,Your_EncodedValues,Your_QuantizedValues,Your_SampledError):
    expectedIntervalIndices=[]
    expectedEncodedValues=[]
    expectedQuantizedValues=[]
    expectedSampledError=[]
    with open(file_name, 'r') as f:
        line = f.readline()
        line = f.readline()
        line = f.readline()
        line = f.readline()
        while line:
            # process line
            L=line.strip()
            if len(L.split(' '))==4:
                L=line.split(' ')
                V1=int(L[0])
                V2=str(L[1])
                V3=float(L[2])
                V4=float(L[3])
                expectedIntervalIndices.append(V1)
                expectedEncodedValues.append(V2)
                expectedQuantizedValues.append(V3)
                expectedSampledError.append(V4)
                line = f.readline()
            else:
                break
    if(len(Your_IntervalIndices)!=len(expectedIntervalIndices)
     or len(Your_EncodedValues)!=len(expectedEncodedValues)
      or len(Your_QuantizedValues)!=len(expectedQuantizedValues)
      or len(Your_SampledError)!=len(expectedSampledError)):
        print("QuantizationTest2 Test case failed, your signal have different length from the expected one")
        return
    for i in range(len(Your_IntervalIndices)):
        if(Your_IntervalIndices[i]!=expectedIntervalIndices[i]):
            print("QuantizationTest2 Test case failed, your signal have different indicies from the expected one") 
            return
    for i in range(len(Your_EncodedValues)):
        if(Your_EncodedValues[i]!=expectedEncodedValues[i]):
            print("QuantizationTest2 Test case failed, your EncodedValues have different EncodedValues from the expected one") 
            return
        
    for i in range(len(expectedQuantizedValues)):
        if abs(Your_QuantizedValues[i] - expectedQuantizedValues[i]) < 0.01:
            continue
        else:
            print("QuantizationTest2 Test case failed, your QuantizedValues have different values from the expected one") 
            return
    for i in range(len(expectedSampledError)):
        if abs(Your_SampledError[i] - expectedSampledError[i]) < 0.01:
            continue
        else:
            print("QuantizationTest2 Test case failed, your SampledError have different values from the expected one") 
            return
    print("QuantizationTest2 Test case passed successfully")
#-----------------backend
def get_number_levels(number_of_bits:int):
    return 2**number_of_bits

def get_number_bits(number_of_levels:int):
    return math.log2(number_of_levels)

def get_ranges(amplitude_value:list,number_of_levels:int): 
    #list of tubles ranges
    list_ranges = []

    max_amplitude = max(amplitude_value)
    min_amplitude = min(amplitude_value)

    dilta = round((max_amplitude - min_amplitude)/float(number_of_levels),3)
        
    start = min_amplitude
    for i in range(number_of_levels):
    
        end = round(start + dilta,3)
        list_ranges.append((round(start,3), end))
        start = end
    

    return list_ranges

def get_binarys(number_of_levels:int):
    list_encodes=[]
    max_length = len(bin(number_of_levels - 1)[2:]) #get length of the longest binary number


    for i in range(number_of_levels):
        
        binary_representation  = bin(i)[2:].zfill(max_length) # Pad with leading zeros
        #strip '0b'
        list_encodes.append(binary_representation)
    
    return list_encodes 

def get_midPoint_ranges(list_ranges:list):
    list_midPoints=[]
    list_encode=[]
    
    for r in list_ranges:
        midpoint = (r[0] + r[1])/2.0
        list_midPoints.append(round(midpoint,3))

    return list_midPoints 

def quantiz_and_encode( amplitude_value:list,list_ranges :list,
                        list_midPoint:list,list_encode:list):
    
    quantiz_values=[]
    encode_quantiz_values = []
    min_point = min(amplitude_value)
    

    for point in amplitude_value:
        
        for i in range(len(list_ranges)):
       
            if point == min_point:
                quantiz_values.append(list_midPoint[0])
                encode_quantiz_values.append(list_encode[0])
                break

            elif point > list_ranges[i][0] and point <= list_ranges[i][1]:
                quantiz_values.append(list_midPoint[i])
                encode_quantiz_values.append(list_encode[i])
                break
    
    df_quantiz = pd.DataFrame({"encode": encode_quantiz_values,
                                "quantization": quantiz_values})
    
    return df_quantiz

def quantiz_encode_rangeIndex_error( amplitude_value:list,list_ranges :list,
                        list_midPoint:list,list_encode:list):
    
    quantiz_values=[]
    encode_quantiz_values = []
    rangeIndex_values = []
    error_values = []
    min_point = min(amplitude_value)
    

    for point in amplitude_value:
        
        for i in range(len(list_ranges)):
       
            if point == min_point:
                quantiz_values.append(list_midPoint[0])
                encode_quantiz_values.append(list_encode[0])
                rangeIndex_values.append(0+1)
                error_values.append(list_midPoint[0] - point)
                break

            elif point > list_ranges[i][0] and point <= list_ranges[i][1]:
                quantiz_values.append(list_midPoint[i])
                encode_quantiz_values.append(list_encode[i])
                rangeIndex_values.append(i+1)
                error_values.append(list_midPoint[i] - point)
                break

    df_quantiz = pd.DataFrame({"rangeIndex":rangeIndex_values,
                                "encode": encode_quantiz_values,
                                "quantization": quantiz_values,
                                "error":error_values})
    
    
    return df_quantiz

def quantize_button_func():
    
    #read_File
    path_file = get_file_path()
    lst_data = read_File(path_file)

    #logic
    num_levels = 0
    len_bit = 0
    
    if type_comboBox.get() == "bits":
        len_bit = int(number_enter.get())
        num_levels = get_number_levels(len_bit)
    else:
        num_levels =  int(number_enter.get())
        len_bit = int(get_number_bits(num_levels))

    ranges_list = get_ranges(lst_data[2],num_levels)
    encode_list = get_binarys(num_levels)
    midpoints_list = get_midPoint_ranges(ranges_list)


    if output_comboBox.get() == "encoded and quantized" :
        quantiz_df = quantiz_and_encode(amplitude_value=lst_data[2],
                                        list_ranges=ranges_list,
                                        list_midPoint=midpoints_list,
                                        list_encode= encode_list)
        
        print(QuantizationTest1(r"C:\Users\HP\Desktop\dsp\Task3 Files\Quan1_Out.txt",quantiz_df[quantiz_df.columns[0]],quantiz_df[quantiz_df.columns[1]]))
        
        path_save = get_save_file_path()
        write_file(path_save, quantiz_df, sampligFrequency=lst_data[0][-1])
    
    elif output_comboBox.get() == "interval index, encoded, quantized and error":
        quantiz_df = quantiz_encode_rangeIndex_error(amplitude_value=lst_data[2],
                                        list_ranges=ranges_list,
                                        list_midPoint=midpoints_list,
                                        list_encode= encode_list)
        
        print(quantiz_df)
        print(QuantizationTest2(r"C:\Users\HP\Desktop\dsp\Task3 Files\Quan2_Out.txt", quantiz_df[quantiz_df.columns[0]], 
                                quantiz_df[quantiz_df.columns[1]],
                                quantiz_df[quantiz_df.columns[2]],
                                quantiz_df[quantiz_df.columns[3]]))
       
        path_save = get_save_file_path()
        write_file(path_save, quantiz_df, sampligFrequency=lst_data[0][-1])

        
    


def quantization_window():
    window = Tk()
    window.geometry("750x650")

    global type_comboBox,number_enter,output_comboBox

    label1 = Label(window, text="select Number of bits or Number of levels then enter the number.", fg="black")
    label1.place(x=10, y=10)
    
    type_comboBox = ttk.Combobox(window, values=["bits", "levels"])
    type_comboBox.place(x=10, y=50)
    
    number_enter = Entry(window, justify='center')
    number_enter.place(x = 300, y = 50)

    

    label2 = Label(window, text="choose the show ouput.", fg="black")
    label2.place(x = 10, y = 90)

   

    output_comboBox = ttk.Combobox(window, values=["encoded and quantized", "interval index, encoded, quantized and error"])
    output_comboBox.place(x = 10, y = 110)
    
   

    excute_button =  Button(window, text="quantize_signal",fg="black",bg="gray",activebackground="lightblue", command=quantize_button_func)
    excute_button.place(x=10, y=160)