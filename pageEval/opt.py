
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
def saveImg(webMetrics):
	b18	=[	597.961325966851, 1.20941463305307, 0.263530270897063, 0.519337016574586, 22.2430939226519, 29.5359116022099,\
			3234.79961045407, 74.9498683548821, 30.8839779005525, 7.97790055248619,	4.19889502762431]
	eb18=[	1093.00357000861, 13.1064831934754, 0.369497128439535, 4.03813923074724, 37.6512729508433, 41.7942723730434,\
			6608.11853235636, 26.6774076382953, 50.2731739563354, 4.13784136034583, 12.6180734088065]
	metricsName=["Word Count","Body Text Ratio","Emphasized Text","Text Positional Changes","Text Clusters","Visible Links","Page Size (kb)","Graphics Percent","Graphics Count","Color Count","Font Count"]
	ewebMetrics=[0 for i in range(11)]
	xlabels = ['Your Url', 'BEST OF 2018']
	x_pos = np.arange(len(xlabels))

	for mno in range(11):
		col='red'
		if mno in set([1,4,6,9,10]):
			col='blue'
		CTEs	= [webMetrics[mno],b18[mno]]
		error 	= [[0,0],[ewebMetrics[mno],eb18[mno]]]
		fig 	= Figure(figsize=(8,8))
		ax 		= fig.add_subplot(111)
		lprop = {'fontsize':20,'weight':'bold'}
		ax.bar(x_pos, CTEs, yerr=error, align='center', color=col,alpha=0.5, ecolor='black', capsize=20)
		ax.set_xticks(x_pos)
		ax.set_title(metricsName[mno],fontdict=lprop)
		ax.set_xticklabels(xlabels,fontdict=lprop)
		ax.yaxis.set_tick_params(labelsize=20)
		ax.yaxis.grid(True)
		canvas = FigureCanvasAgg(fig)
		canvas.print_figure('/home/abhiavk/git/mysite/static/pageEval/images/'+str(mno)+'.png', dpi=80)

import views
webMetrics=[i for i in range(11)]
saveImg(webMetrics)
