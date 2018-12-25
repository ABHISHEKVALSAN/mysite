
import subprocess
import sys
import numpy as np
import webcolors
import re
import string
import sys
import unidecode
from bs4 import BeautifulSoup
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.urls import reverse
from django.views import generic
from itertools import groupby
from matplotlib.backends.backend_agg import FigureCanvasAgg
from matplotlib.figure import Figure
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait
def closest_colour(requested_colour):
    min_colours = {}
    for key, name in webcolors.css3_hex_to_names.items():
        r_c, g_c, b_c = webcolors.hex_to_rgb(key)
        rd = (r_c - requested_colour[0]) ** 2
        gd = (g_c - requested_colour[1]) ** 2
        bd = (b_c - requested_colour[2]) ** 2
        min_colours[(rd + gd + bd)] = name
    return min_colours[min(min_colours.keys())]
def colour_name(requested_colour):
    try:
        closest_name = webcolors.rgb_to_name(requested_colour)
    except ValueError:
        closest_name = closest_colour(requested_colour)
    return closest_name
def get_color_count():
	img 	 = Image.open('/home/abhiavk/git/mysite/static/pageEval/images/screenshot.png')
	p=img.getdata()
	total_pix=len(p)
	p_list=[i[:-1] for i in p]
	p_list.sort()
	temp = [[len(list(group)),key] for key,group in groupby(p_list)]
	temp.sort()

	#Keeping a threshold on the colors
	p_freq=[]
	for i in temp[::-1]:
		if i[0]>1:
			p_freq.append(i)
		else:
			break

	p_color = [[colour_name(p_freq[i][1]),p_freq[i][0]] for i in range(len(p_freq))]
	p_color.sort()
	p_color_uni=[p_color[0]]
	for i in p_color[1:]:
		if p_color_uni[-1][0]==i[0]:
			p_color_uni[-1][1]+=i[1]
		else:
			p_color_uni.append(i)
	total_color_pix=0
	for i in p_color_uni:
		total_color_pix+=i[1]

	c_count=0
	for i in range(len(p_color_uni)):
		if float(p_color_uni[i][1])/total_color_pix>0.01:
			#print p_color_uni[i]
			c_count+=1

	return c_count
print(get_color_count())
