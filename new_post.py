#!/usr/bin/python

import os

posts_dir = "_posts"
file_list = os.listdir(posts_dir)
file_list.sort()
last_file_name = file_list[-1]
last_file_path = posts_dir + "/" + last_file_name

file_obj = open(last_file_path)

print(file_obj.read())
