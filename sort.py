import os
import random
from shutil import copy, copyfile
import sys
train, test = [],[]
#takes dir with subdir of folders that contain images and their annotations, collapses into one folder
def collapse_files(top_dir):
	file_sets = list(os.walk(top_dir))
	pic_sets = []
	for i in file_sets:
		if not i[1]:
			pic_sets.append(i)
	base = {"deer":0,"hog":1,"other":2}
	fail_cases = []
	for i in pic_sets:
		temp_d = {}
		os.chdir(i[0])
		if "classes.txt" in i[2]:
			c_file = open("classes.txt","r")
			l = [x.rstrip() for x in c_file.readlines()]
			for a in range(len(l)):
				temp_d[a]=l[a]
		print(temp_d)
		print(i[0])
		for f in i[2]:
			if not "classes" in f:
				if ".txt" in f:
					print(f)
					a_file = open(f,"r")
					l = [x for x in a_file.readlines()]
					new_l = []
					for a in l:
						try:
							new_l.append(str(base[temp_d[int(a[0])]])+a[1:])
						except KeyError:
							print(f,a[0],temp_d,base)
							fail_cases.append(f)
							#sys.exit(0)
					a_file.close()
					with open(f,"w") as b_file:
						for a in new_l:
							b_file.write(a)
						b_file.close()
					
	os.chdir(top_dir)
	for i in pic_sets:
		os.chdir(i[0])
		for a in i[2]:
			if not "classes" in a and a not in fail_cases:
				copy(a,top_dir)
	os.chdir(top_dir)
	heck = open("classes.txt","w")
	heck.write("deer\n")
	heck.write("hog\n")
	heck.write("other\n")
#splits files into train and test groups; train group has only annotated files
def split_groups(dir_name,split_num):
	files = os.listdir(dir_name)
	img_files = [x for x in files if ".JPG" in x]
	annotated_files = [x for x in img_files if x.split(".JPG")[0]+".txt" in files]
	train = random.sample(annotated_files, int(len(annotated_files)*split_num))
	test = random.sample(img_files, int(len(annotated_files)*(1-split_num)))
	return (train, test)
#creates training and test files in given dir
def create_train_test(source_dir, split_num, work_dir):
	train_group, test_group = split_groups(source_dir, split_num)
	os.chdir(work_dir)
	tr_file = open("train.txt","w")
	t_file = open("test.txt","w")
	for i in train_group:
		tr_file.write(source_dir+i+"\n")
	for i in test_group:
		t_file.write(source_dir+i+"\n")
#creates trainer.data file for given img dir
def create_trainer_instr(source_dir,work_dir):
	files = os.listdir(source_dir)
	os.chdir(source_dir)
	class_num=-1
	if("classes.txt" in files):
		c_f = open("classes.txt","r")
		l = c_f.readlines()
		class_num=len(l)
		c_f.close()
		copyfile("classes.txt",work_dir+"//classes.names")
	else:
		print("Error: no class file found")
		sys.exit(0);
	os.chdir(work_dir)
	f = open("trainer.data","w")
	f.write("classes = "+str(class_num)+"\n")
	f.write("train = train.txt\n")
	f.write("valid = test.txt\n")
	f.write("names = classes.names\n")
	f.write("backup = backup/\n")
	f.close()

create_train_test("/home/jbellamy/darknet/build/darknet/x64/data/images/",.90,"/home/jbellamy/darknet/")
create_trainer_instr("/home/jbellamy/darknet/build/darknet/x64/data/images/","/home/jbellamy/darknet/")
#collapse_files("/home/jbellamy/darknet/build/darknet/x64/data/images/")
