import imagej,skimage, os
import matplotlib.pyplot as plt
import csv
import numpy as np
import subprocess

SIGMA_BLUR = 2
CONFIDENCE_THRESHOLD = 0.15
MIN_RADIUS = 80
MAX_RADIUS = 140

# Initialize ImageJ in head mode
print("Initializing PyImageJ...")
ij = imagej.init('/Applications/Fiji')
def hough_detect(image_path, min_r = MIN_RADIUS, max_r = MAX_RADIUS):
    img = skimage.io.imread(image_path)
    gray_img = skimage.color.rgb2gray(img)

    edges = skimage.feature.canny(gray_img,sigma = SIGMA_BLUR)
    radii = np.arange(min_r,max_r,2)
    hough_res = skimage.transform.hough_circle(edges,radii)

    accums,cx,cy,radii_found = skimage.transform.hough_circle_peaks(
        hough_res, radii,
        min_xdistance=min_r,
        min_ydistance=min_r, threshold = CONFIDENCE_THRESHOLD
    )
    img_copy = img.copy()
    for center_y, center_x, radius in zip(cy,cx, radii_found):
        circy, circx = skimage.draw.circle_perimeter(center_y, center_x, radius, shape = img_copy.shape[:2])
        img_copy[circy,circx] = (220,20,20)
    #print(f"Found {len(radii_found)} circles")
    #print(f"Confidence scores: min={accums.min():.2f} max={accums.max():.2f} mean={accums.mean():.2f}")
    skimage.io.imsave('/tmp/visual_output.png',img_copy)
    #ax.imshow(img_copy, cmap=plt.cm.gray)
    #plt.show()
    
    feret_values = (2*radii_found).tolist()
    plot_values(feret_values,'pixels')

def plot_values(feret: list[float],unit):
    fig, ax, = plt.subplots()
    ax.hist(feret, bins = 'auto', edgecolor = 'black')
    ax.set_xlabel(f"Feret Diameter {unit}")
    ax.set_ylabel("Count")
    ax.set_title(f"Droplets Size Distribution(n={len(feret)})")
    plt.tight_layout()
    plt.savefig("/tmp/histogram.png",dpi = 150)

    subprocess.run(['open','/tmp/histogram.png'])
    plt.close()

#print(f"ImageJ version: {ij.getVersion()}")
def segment_droplets(image_path,  pixel_ratio, unit, num_droplets = 200, threshold = "Default"):
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
    
    plot_values(values,unit)


    return{
        "histogram": "/tmp/histogram.png",
        "visual" : "tmp/visual_output.png",
        "values": values,
        "n" : len(values),
        "mean": np.mean(values),
        "std": np.std(values)

    }

hough_detect('/Volumes/DISK_IMG/Droplet Picture/IMG_0013.jpg')#works pretty well!
#hough_detect('/Volumes/DISK_IMG/Droplet Picture/IMG_0010.jpg',40,110)#this works ok, but tends to undershoot and it really 
#depends on the values you put in for blur and confidence
#segment_droplets('/Volumes/DISK_IMG/Droplet Picture/IMG_0010.jpg', 1, "pixels",500) #this works great!
'''
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
    segment_droplets(path,float(measureUnits/measurePixel),unit, numDroplets)
except FileNotFoundError:
    print("couldn't find the given file. Please try again:")
    path = input("What is the path of your image")
    segment_droplets(path,float(measureUnits/measurePixel),unit, numDroplets)

'''
print("done :)")

ij.dispose()
import jpype
jpype.shutdownJVM()