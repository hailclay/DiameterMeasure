import imagej, skimage, os, xarray
import matplotlib.pyplot as plt
import csv
import numpy as np
import subprocess


# Initialize ImageJ in head mode
print("Initializing PyImageJ...")
ij = imagej.init('/Applications/Fiji')
#print(f"ImageJ version: {ij.getVersion()}")
def analyze_image(image_path,  pixel_ratio, unit, num_droplets = 200, threshold = "Default"):
    macro_args = f"{num_droplets},{threshold},{pixel_ratio},{unit},{image_path}"
    print(f"what it should be: {macro_args}")
    macro = open('/Users/haile/Desktop/DmterMeasure.ijm').read()
    result = ij.py.run_macro(macro,{"argument": macro_args})
    if os.path.exists('/tmp/visual_output.png'):
        print("visual output saved successfully")
        subprocess.run(['open','/tmp/visual_output.png'])
    else:
        print("NOOOOOO")
    feret_path = '/tmp/feret_values.txt'
    with open(feret_path) as f:
        values = [float(line.strip()) for line in f if line.strip()]
    
    fig, ax, = plt.subplots()
    ax.hist(values, bins = 'auto', edgecolor = 'black')
    ax.set_xlabel(f"Feret Diameter {unit}")
    ax.set_ylabel("Count")
    ax.set_title(f"Droplets Size Distribution(n={len(values)})")
    plt.tight_layout()
    plt.savefig("/tmp/histogram.png",dpi = 150)

    subprocess.run(['open','/tmp/histogram.png'])
    plt.close()


    return{
        "histogram": "/tmp/histogram.png",
        "visual" : "tmp/visual_output.png",
        "values": values,
        "n" : len(values),
        "mean": np.mean(values),
        "std": np.std(values)

    }

numDroplets = int(input("What is a rough estimate of the num of droplets?"))
measurePixel= float(input("For ratio, num of pixels"))
if measurePixel == 0:
    print("number of pixels cannot be 0 in measurement. Input again")
    while(not measurePixel):
        measurePixel= float(input("For ratio, num of pixels"))

measureUnits = float(input("for ratio, for that num of pixels, what is the measurement in ur unit?"))
unit = input("What is your unit?")
path = input("What is the path of your image")[1:-1]
 
print("processing image...")
#analyze_image('/Volumes/DISK_IMG/Droplet Picture/IMG_0010.jpg', 0.1, "ooh",500) #this works great!
#analyze_image('/Volumes/DISK_IMG/Droplet Picture/IMG_0008.jpg', 1, "hello",100) #this is having more trouble...
try:
    analyze_image(path,float(measureUnits/measurePixel),unit, numDroplets)
except FileNotFoundError:
    print("couldn't find the given file. Please try again:")
    path = input("What is the path of your image")
    analyze_image(path,float(measureUnits/measurePixel),unit, numDroplets)


print("done :)")

ij.dispose()
import jpype
jpype.shutdownJVM()