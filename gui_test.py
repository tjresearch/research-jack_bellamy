from tkinter import *
from tkinter.filedialog import askdirectory, askopenfilename
from PIL import Image, ImageTk
import os
from day_nightv2 import main
dirname =""
filename="/home/jbellamy/darknet/build/darknet/x64/data/images/April 2019/04280001.JPG"
w, h = 400,400
#sets working directory, separate from button and only use as helper
def find_dir():
    global dirname
    dirname = askdirectory()
    if dirname is None or type(dirname) is tuple or not dirname:
        print("No folder selected")
        return
    os.chdir(dirname)
#draws and labels bounding boxes around detected objects, may integrate into another method in future
def find_bounding_boxes(file_str,can,label_obj,rec):
    try:
        fi = open(file_str,"r")
    except FileNotFoundError:
        print("Error: no annotation file found")
        return
    try:
        class_names = open("classes.txt","r").readlines()
    except FileNotFoundError:
        print("Error: no class file found")
        return
    label_obj.set("Label: ")
    objs = [x.rstrip() for x in fi.readlines()]
    obj_counter = 1
    for f in objs:
        params = f.split(" ")
        obj, x, y, wid, hei = int(params[0]), float(params[1]), float(params[2]), float(params[3]), float(params[4])
        x1,y1,x2,y2= int(x*w)-(int(wid*w)/2), int(y*h)-(int(hei*h)/2), int(x*w)+(int(wid*w)/2), int(y*h)+(int(hei*h)/2)
        can.create_rectangle(x1,y1,x2,y2)
        can.create_text(x1,y1,text=str(obj_counter))
        label_obj.set(label_obj.get()+class_names[obj]+"("+str(obj_counter)+") ")
        obj_counter+=1
#opens and displays image file
def find_file(i_c):
    global filename
    filename = askopenfilename()
    if filename is None or not filename:
        print("No file selected")
        return
    i_c.delete("all")
    i = Image.open(filename)
    i = i.resize((w, h), Image.ANTIALIAS)
    root.p =ImageTk.PhotoImage(i)
    curr_img=i_c.create_image(w/2,h/2,image=root.p)
#runs darknet train command, switch for classify program in the future
def run_darknet():
    os.chdir("/home/jbellamy/darknet")
    os.system("./darknet detector train trainer.data yolov3-tiny.cfg yolov3-tiny.weights")

root = Tk()
img = Image.open(filename)
img = img.resize((w, h), Image.ANTIALIAS)
root.photo = ImageTk.PhotoImage(img)
c=Canvas(root, width=w,height=h)
i=c.create_image(w/2,h/2,image=root.photo)
c.pack()
f = Frame(root)

find_dir_b=Button(f,text="Find Directory",command=find_dir)
find_dir_b.grid(row=0,column=0)
class_b=Button(f,text="Split",command= lambda : main(dirname))
class_b.grid(row=0,column=1)
open_img=Button(f,text="Open Image",command= lambda: find_file(c))
open_img.grid(row=0,column=2)
st = StringVar()
img_class = Label(f, textvariable=st)
st.set("Label: ")
img_class.grid(row=1,column=0)
draw_box=Button(f,text="Draw Box",command= lambda : find_bounding_boxes(filename.split(".JPG")[0]+".txt",c,st,i))
draw_box.grid(row=0,column=3)
classify_b=Button(f,text="Classify",command= lambda : run_darknet())
classify_b.grid(row=0,column=4)


f.pack()
mainloop()
