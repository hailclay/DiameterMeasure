import imagej, skimage, os, xarray

filename = os.path.join(skimage.data_dir, '/Volumes/DISK_IMG/Droplet Picture/IMG_0004.jpg')
droplets = skimage.io.imread(filename)

xdroplets = xarray.DataArray(droplets, name = 'xdroplets', dims=('t', 'row', 'col'))

# Initialize ImageJ in head mode
print("Initializing PyImageJ...")
ij = imagej.init('sc.fiji:fiji')

jdroplets = ij.py.to_java(xdroplets)#converting xarray (labeled numpy array) to java
ij.py.show(jdroplets)


# Print the active version to confirm it works
print(f"ImageJ version: {ij.getVersion()}")

#takes in inputs... should ask for num, measurement conversion, (give me pixel to length ratio preferrably?)
#if num is less than like 120, take in min size and max size estimates... (in pixels). If they don't have, auto should be around 80 - 150
#once input is ready, calls the appropriate macro with all of the parameters.

numDroplets = int(input("What is a rough estimate of the num of droplets?"))
measureRatio = float(input("What is the ratio of pixel to unit?"))
minSize = 80
maxSize = 140

if numDroplets > 120:
    #run Macro from Internet
    print("running macro from internet")
else:
    print("running hough circle macro.. will take a minute")
    #run hough circle macro


