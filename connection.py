import imagej, skimage, os, xarray
import matplotlib.pyplot as plt
import csv
import numpy as np


# Initialize ImageJ in head mode
print("Initializing PyImageJ...")
ij = imagej.init('/Applications/Fiji')
#print(f"ImageJ version: {ij.getVersion()}")
def analyze_image(image_path,  pixel_ratio, unit, num_droplets = 200, threshold = "Default"):
    macro_args = f"{num_droplets},{threshold},{pixel_ratio},{unit},{image_path}"
    print(f"what it should be: {macro_args}")
    macro = open('/Users/haile/Desktop/DmterMeasure.ijm').read()
    result = ij.py.run_macro(macro,{"argument": macro_args})
    '''
    import os
    print("feret file exists:", os.path.exists('/tmp/feret_values.txt'))
    print("feret file size:", os.path.getsize('/tmp/feret_values.txt') if os.path.exists('/tmp/feret_values.txt') else "N/A")
    print("results csv exists:", os.path.exists('/tmp/results.csv'))
    print('what I got:')
    print_thing = result.get('printed_args')
    print(print_thing)'''
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
    plt.close()

    return{
        "histogram": "/tmp/histogram.png",
        "visual" : "tmp/visual_output.png",
        "values": values,
        "n" : len(values),
        "mean": np.mean(values),
        "std": np.std(values)

    }


 
print("processing image...")
analyze_image('/Volumes/DISK_IMG/Droplet Picture/IMG_0003.jpg', 1, "mm",100)
print("done :)")

ij.dispose()
import jpype
jpype.shutdownJVM()
