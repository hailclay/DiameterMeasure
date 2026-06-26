import streamlit as st
import tempfile, os
from connection import segment_droplets, hough_detect,ratiod

IMG_PATH_NAME = '/tmp/visual_output.png'

st.title("Droplet Diameter Measure")

file = st.file_uploader("Upload your image")

def run(choice:str,args):
    if args["pixel_num"] == 0:
        scale = 1
    else:
        scale = args["pixel_num"]/float(args["distance_num"])
    if choice == "Thresholding":
        return segment_droplets(tmp_path,scale,args["unit"])
    elif choice == "Hough Circle Transform":
        return ratiod(hough_detect(tmp_path,args["min_size"],args["max_size"],args["sigma_blur"],args["confidence"]),scale)
    
    
if file is not None:
    with tempfile.NamedTemporaryFile(delete = False, suffix = os.path.splitext(file.name)[1])as tmp:
        tmp.write(file.getbuffer())
        tmp_path = tmp.name
    st.image(tmp_path)
    choice = st.selectbox("Measurement Method", options = ["Thresholding", "Hough Circle Transform"])
    args = dict()
    if choice == "Hough Circle Transform":
        args["min_size"] = st.slider("Approximate minimum area (in pixels)", 0, 100,80)
        args["max_size"] = st.slider("Approximate max area(in pixels)",0,200,140)
        args["sigma_blur"] = st.slider("sigma blur", 0, 4,2)
        args["confidence"] = st.slider("confidence threshold", 0.0,1.00, 0.15)
    args["pixel_num"] = st.number_input("Distance in Pixels", 0)
    args["distance_num"] = st.number_input("Known Distance", 0)
    args["unit"] = st.text_input("Unit of Length", "pixel")
        #run(choice)
    pressed = st.button("Measure Diameter")
    if(pressed):
        result=run(choice,args)
        if(result):
            st.image(IMG_PATH_NAME)
        




