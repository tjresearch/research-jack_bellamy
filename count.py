import os
import random
from shutil import copy, copyfile
import sys
#takes dir with subdir of folders that contain images and their annotations, collapses into one folder
def count_stats(top_dir):
  total_deer_count = 0;
  total_hog_count=0;
  total_other_count=0;
	file_sets = list(os.walk(top_dir))
	pic_sets = []
	for i in file_sets:
		if not i[1]:
			pic_sets.append(i)
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
                                                    class_id = int(a[0])
                                                    if temp_d[class_id]=="deer":
                                                        total_deer_count+=1
                                                    if temp_d[class_id]=="hog":
                                                        total_hog_count+=1
                                                    if temp_d[class_id]=="other":
                                                        total_other_count+=1
						except KeyError:
							print(f,a[0],temp_d,base)
							fail_cases.append(f)
							#sys.exit(0)
					a_file.close()
  return (total_deer_count,total_hog_count,total_other_count)
