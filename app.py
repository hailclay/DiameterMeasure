import streamlit as st
import tempfile, os
from connection import segment_droplets, hough_detect,ratiod, plot_values

IMG_PATH_NAME = '/tmp/visual_output.png'

st.title("Droplet Diameter Measure")

file = st.file_uploader("Upload your image")

def run(choice:str,args):
    if args["pixel_num"] == 0:
        scale = 1
    else:
        scale = args["distance_num"]/args["pixel_num"]
    if choice == "Thresholding":
        return segment_droplets(tmp_path,scale,args["unit"],args["threshold"])
    elif choice == "Hough Circle Transform":
        results = hough_detect(tmp_path,args["min_size"],args["max_size"],args["sigma_blur"],args["confidence"])
        processed = ratiod(results,scale)
        return processed
    
    
if file is not None:
    with tempfile.NamedTemporaryFile(delete = False, suffix = os.path.splitext(file.name)[1])as tmp:
        tmp.write(file.getbuffer())
        tmp_path = tmp.name
    st.image(tmp_path)
    choice = st.selectbox("Measurement Method", options = ["Thresholding", "Hough Circle Transform"])
    advanced = st.expander("Advanced")
    args = dict()
    if choice == "Hough Circle Transform":
        args["min_size"] = advanced.slider("Approximate minimum area (in pixels)", 0, 100,80)
        args["max_size"] = advanced.slider("Approximate max area(in pixels)",0,200,140)
        args["sigma_blur"] = advanced.slider("sigma blur", 0, 4,2)
        args["confidence"] = advanced.slider("confidence threshold", 0.0,1.00, 0.15)
    elif choice == "Thresholding":
        args["threshold"] = advanced.selectbox("Threshold type", options=["default", "Huang", "Intermodes", "IsoData", "IJ_IsoData", "Li", "MaxEntropy", "Mean", "MinError", "Minimum", "Moments", "Otsu","Percentile", "RenyiEntropy", "Shanbhag", "Triangle", "Yen"])
    args["pixel_num"] = st.number_input("Distance in Pixels", 0)
    args["distance_num"] = st.number_input("Known Distance", 0)
    args["unit"] = st.text_input("Unit of Length", "pixel")
        #run(choice)
    pressed = st.button("Measure Diameter")
    if(pressed):
        with st.spinner("Analyzing..."):
            result=run(choice,args)

        if(result):
            histogram = plot_values(result, args["unit"])
            col1, col2 = st.columns(2)
            col1.image(IMG_PATH_NAME)
            col2.pyplot(histogram)
        




