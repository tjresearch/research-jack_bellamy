import PIL.Image
import PIL.ExifTags
import os
import sys
from shutil import copyfile
from datetime import datetime
#os.chdir("C:\\Users\\jackc\\Desktop\\Senior Lab Work\\April 2019")
def pull_date(img_str):
    try:
        img = PIL.Image.open(img_str)
        exif = {
            PIL.ExifTags.TAGS[k]: v
            for k, v in img._getexif().items()
            if k in PIL.ExifTags.TAGS
            }
        return exif["DateTimeOriginal"]
    except FileNotFoundError:
        print("Error: file not found")
        sys.exit(0)
def main(work_dir):
    if(work_dir==""):
        print("error, no directory specified")
        return
    os.chdir(work_dir)
    files = os.listdir(work_dir)
    imgs = []
    labels = []
    for i in files:
        if(i.endswith(".JPG")):
            imgs.append(i)
        if(i.endswith(".txt")):
            labels.append(i)
        #if(i.endswith(".txt")and i is not "classes.txt"):
    img_date_dict = {}
    try:
        os.mkdir("Day_test")
        os.mkdir("Night_test")
        os.chdir(work_dir+"//Day_test")
        os.mkdir("images")
        os.mkdir("labels")
        os.chdir(work_dir+"//Night_test")
        os.mkdir("images")
        os.mkdir("labels")
        os.chdir(work_dir)
    except FileExistsError:
        print("Error: directories already exist")
        sys.exit(0)
    for i in imgs:
        dt =datetime.strptime(pull_date(i),"%Y:%m:%d %H:%M:%S")
        img_date_dict[i]=(dt.hour+(dt.minute/60))
    for i,time in img_date_dict.items():
        if(time<7 or time>19.75):
            copyfile(i,work_dir+"\\Night_test\\images\\"+i)
            if(i.split(".JPG")[0]+".txt" in labels):
                copyfile(i.split(".JPG")[0]+".txt",work_dir+"\\Night_test\\labels\\"+i.split(".JPG")[0]+".txt")
        else:
            copyfile(i,work_dir+"\\Day_test\\images\\"+i)
            if(i.split(".JPG")[0]+".txt" in labels):
                copyfile(i.split(".JPG")[0]+".txt",work_dir+"\\Day_test\\labels\\"+i.split(".JPG")[0]+".txt")
#main("C:\\Users\\jackc\\Desktop\\Senior Lab Work\\April 2019")
