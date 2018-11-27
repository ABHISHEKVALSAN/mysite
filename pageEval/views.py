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
def string_to_words(s):
	s=s.replace("\n"," ")
	s=s.replace(string.punctuation,"")
	s=re.sub("[^\w]"," ",  s).split()
	return s
def get_words(d):
	txt=d.execute_script("return document.body.innerText")
	if txt==None:
		txt=""
	words = string_to_words(str(unidecode.unidecode(txt)))
	return words
def get_word_count(d):
	#print "Param1"
	words=get_words(d)
	return float(len(words))
def get_text_body_ratio(soup):

	#print "Param2"

	headers=[]
	for i in range(1,7):
		headers+=soup.findAll("h"+str(i))
	sizeHeaders=[]
	sizeHeaders+=soup.findAll("font",{"size":"3"})
	sizeHeaders+=soup.findAll("font",{"size":"4"})
	sizeHeaders+=soup.findAll("font",{"size":"5"})
	txt=""
	for i in headers:
		txt+=" "+i.text
	for i in sizeHeaders:
		txt+=" "+i.text
	words=[]
	if len(txt)!=0:
		words=string_to_words(str(unidecode.unidecode(txt)))
	#print words
	return float(len(words))
def get_emph_body_text_percentage(d):

	#print "Param3"

	boldText = d.find_elements_by_tag_name("b")
	words=[]
	for i in boldText:
		words+= string_to_words(str(unidecode.unidecode(i.text)))
	boldWordCount=len(words)
	try:
		txt=str(unidecode.unidecode(d.execute_script("return document.body.innerText")))
	except:
		txt=str(unidecode.unidecode(d.execute_script("return document.body.textContent")))
	pattern = re.compile("!+")
	exclWordCount=len(re.findall(pattern,txt))

	words=get_words(d)
	capWordCount=0
	for i in words:
		if i==i.upper():
			capWordCount+=1
	#print boldWordCount, exclWordCount, capWordCount
	return boldWordCount + exclWordCount + capWordCount
def get_text_position_changes(s):

	#print "Param4"

	elem=s.findAll()
	prev=""
	textPositionChanges=0
	for i in elem:
		try:
			string=str(i["style"])
			if "text-align:"in string:
				align=string.split("text-align:")[1]
				position=align.split(";")[0].strip()
				if position!=prev:
					textPositionChanges+=1
					prev=position


		except:
			pass

	return textPositionChanges
def get_text_clusters(d):

	#print "Param5"

	tableText= d.find_elements_by_tag_name("td")+d.find_elements_by_tag_name("table")
	paraText = d.find_elements_by_tag_name("p")
	textClusters=len(tableText)+len(paraText)
	#print tableText,"\n\n",paraText,"\n\n",textClusters
	return textClusters
def get_visible_links(d):

	#print "Param6"

	links=d.find_elements_by_tag_name("a")
	visibleLinkCount=0
	for i in links:
		if i.text != "":
			visibleLinkCount+=1
	return visibleLinkCount
def get_page_size(d):

	#print "Param7"

	scriptToExecute = "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
	networkData = d.execute_script(scriptToExecute)
	pageSize=0
	for i in networkData:
		try:
			pageSize+=int(i[u'transferSize'])
		except:
			pass
	return float(pageSize)/1024.0
def get_graphics_size(d):

	#print "Param8"

	scriptToExecute = "var performance = window.performance || window.mozPerformance || window.msPerformance || window.webkitPerformance || {}; var network = performance.getEntries() || {}; return network;"
	networkData = d.execute_script(scriptToExecute)
	graphicsSize=0.0
	for i in networkData:
		try:
			if i[u'initiatorType']== u'script' or i[u'initiatorType']==u'img' or i['initiatorType']== u'css':
				graphicsSize+=int(i[u'transferSize'])
		except:
			pass
	return float(graphicsSize)/1024.0
def get_graphics_count(d):

	#print "Param9"
	styleSteets=d.find_elements_by_tag_name("style")
	images=d.execute_script("return document.images;")
	graphicsCount=len(styleSteets)+len(images)
	return  graphicsCount
def get_color_count(d):
	d.save_screenshot('/home/abhiavk/git/mysite/pageEval/static/pageEval/images/screenshot.png')
	img 	 = Image.open('/home/abhiavk/git/mysite/pageEval/static/pageEval/images/screenshot.png')

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
def get_font_count(d):

	#print("Param11")

	bold		= d.find_elements_by_tag_name("b")
	italic		= d.find_elements_by_tag_name("i")
	big		= d.find_elements_by_tag_name("big")
	strong		= d.find_elements_by_tag_name("big")

	faces		=d.find_elements_by_tag_name("font")
	fontFaces	=""
	for face in faces:
		fontFaces	+=  (str(face).split("face=\"")[-1]).split("\"")[0]+","
	faceCount 	= len(set(fontFaces.split(",")))-1

	fontCount =len(bold)+len(italic)+len(big)+len(strong)+faceCount
	return fontCount
def main(url):
	options = Options()
	options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-gpu')
	options.add_argument('--remote-debugging-port=9222')
	driver= webdriver.Chrome(chrome_options=options)
	driver.implicitly_wait(1)
	driver.get(url)
	WebDriverWait(driver, timeout=10).until(lambda x: x.find_elements_by_tag_name('body'))
	page_source=driver.page_source
	soup=BeautifulSoup(page_source,'html.parser')
	wordCount				=	get_word_count(driver)					#Parameter 1
	textBodyRatio			=	get_text_body_ratio(soup)				#Parameter 2
	emphText				=	get_emph_body_text_percentage(driver)	#Parameter 3
	textPositionalChanges	=	get_text_position_changes(soup)			#Parameter 4
	textClusters			=	get_text_clusters(driver)				#Parameter 5
	visibleLinks			=	get_visible_links(driver)				#Parameter 6
	pageSize				=	get_page_size(driver)					#Parameter 7
	graphicsSize			=	get_graphics_size(driver)				#Parameter 8
	graphicsCount			=	get_graphics_count(driver)				#Parameter 9
	colorCount				=	get_color_count(driver)					#Parameter 10
	fontCount				=	get_font_count(driver)					#Parameter 11
	driver.quit()
	if pageSize==0:
		graphicsPercent=0
	else:
		graphicsPercent=graphicsSize*100.0/pageSize
	if wordCount!=0:
		textBodyRatio=textBodyRatio*1.0/wordCount
		emphTextRatio=emphText/wordCount
	else:
		textBodyRatio=0.0
		emphTextRatio=0.0
	return [wordCount, textBodyRatio, emphTextRatio , textPositionalChanges, textClusters, visibleLinks, pageSize ,graphicsPercent, graphicsCount, colorCount, fontCount]
def saveImg(webMetrics):
	b18	=[	597.961325966851, 1.20941463305307, 0.263530270897063, 0.519337016574586, 22.2430939226519, 29.5359116022099,\
			3234.79961045407, 74.9498683548821, 30.8839779005525, 7.97790055248619,	4.19889502762431]
	eb18=[	1093.00357000861, 13.1064831934754, 0.369497128439535, 4.03813923074724, 37.6512729508433, 41.7942723730434,\
			6608.11853235636, 26.6774076382953, 50.2731739563354, 4.13784136034583, 12.6180734088065]
	metricsName=["Word Count","Body Text Ratio","Emphasized Text","Text Positional Changes","Text Clusters","Visible Links","Page Size (kb)","Graphics Percent","Graphics Count","Color Count","Font Count"]
	ewebMetrics=[0 for i in range(11)]
	Country = ['Your Url', 'BEST OF 2018']
	x_pos = np.arange(len(Country))

	for mno in range(11):
		col='red'
		if mno in [1,4,6,9,10]:
			col='blue'
		CTEs	= [webMetrics[mno],b18[mno]]
		error 	= [[min(webMetrics[mno],ewebMetrics[mno]),min(b18[mno],eb18[mno])],[ewebMetrics[mno],eb18[mno]]]
		fig 	= Figure(figsize=(8,8))
		ax 		= fig.add_subplot(111)
		lprop = {'fontsize':20,'weight':'bold'}
		ax.bar(x_pos, CTEs, yerr=error, align='center', color=col,alpha=0.5, ecolor='black', capsize=20)
		ax.set_xticks(x_pos)
		ax.set_title(metricsName[mno],fontdict=lprop)
		ax.set_xticklabels(Country,fontdict=lprop)
		ax.yaxis.set_tick_params(labelsize=20)
		ax.yaxis.grid(True)
		canvas = FigureCanvasAgg(fig)
		canvas.print_figure('/home/abhiavk/git/mysite/static/pageEval/images/'+str(mno)+'.png', dpi=80)
#---UrlTransitions---#
def index(request):
	return render(request, 'pageEval/index.html')
def results(request):
	return render(request, 'pageEval/results.html',{
            'error_message': "You didn't select a choice.",
        })
def metrics(request):
	url			= 	request.POST['urlText']
	webMetrics	=	main(url)
	saveImg(webMetrics)
	arg={'webMetrics':webMetrics}
	#return render(request,'pageEval/error.html',arg)
	return render(request,'pageEval/results.html',arg)
