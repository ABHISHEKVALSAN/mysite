from bs4 import BeautifulSoup
from itertools import groupby
from PIL import Image
from selenium import webdriver
from selenium.webdriver.chrome.options import Options  
from selenium.webdriver import FirefoxOptions
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from selenium.webdriver.support.ui import WebDriverWait

import webcolors
import re
import string
import sys
import unidecode

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


#--------------------------------------------#
#----------- 1.  Word Count -----------------#
#--------------------------------------------#


def get_word_count(d):
	#print "Param1"	
	words=get_words(d)
	return float(len(words))


#--------------------------------------------#
#--------- 2. Text Body Ratio ---------------#
#--------------------------------------------#


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
	
#--------------------------------------------#
#------ 3. Emphasized Body Percentage -------#
#--------------------------------------------#

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
	

#--------------------------------------------#
#----- 4. Text Positional Changes -----------#   //open to improvement
#--------------------------------------------#


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


#--------------------------------------------#
#----------- 5. Text Clusters ---------------#     //open to improvement 
#--------------------------------------------#


def get_text_clusters(d):
	
	#print "Param5"
	
	tableText= d.find_elements_by_tag_name("td")+d.find_elements_by_tag_name("table")
	paraText = d.find_elements_by_tag_name("p")
	textClusters=len(tableText)+len(paraText)
	#print tableText,"\n\n",paraText,"\n\n",textClusters
	return textClusters


#--------------------------------------------#
#---------- 6. Visible Links ----------------#
#--------------------------------------------#
def get_visible_links(d):

	#print "Param6"

	links=d.find_elements_by_tag_name("a")
	visibleLinkCount=0
	for i in links:
		if i.text != "":
			visibleLinkCount+=1
	return visibleLinkCount


#--------------------------------------------#
#------------- 7. Page Size -----------------#
#--------------------------------------------#

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
	

#--------------------------------------------#
#--------- 8. Graphics Percentage -----------#
#--------------------------------------------#


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
#--------------------------------------------#
#----------- 9. Graphics Count --------------#
#--------------------------------------------#

def get_graphics_count(d):

	#print "Param9"
	styleSteets=d.find_elements_by_tag_name("style")
	images=d.execute_script("return document.images;")
	graphicsCount=len(styleSteets)+len(images)  
	return  graphicsCount


#--------------------------------------------#
#----------- 10. Color Count ----------------#
#--------------------------------------------#


def get_color_count(d):
	#print "Param10"
	d.save_screenshot('screenshot.png') 
	img 	 = Image.open('screenshot.png')
	
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


#--------------------------------------------#
#----------- 11. Font Count -----------------#
#--------------------------------------------#


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
	

def main(filename):
	#binary = FirefoxBinary("/usr/bin/firefox")
	#driver=webdriver.Firefox(firefox_binary=binary)
	#opts = FirefoxOptions()
	#opts.add_argument("--headless")
	#driver = webdriver.Firefox(firefox_options=opts)
	options = Options()
	options.add_argument("--headless")
	options.add_argument('--no-sandbox')
	options.add_argument('--disable-gpu')
	options.add_argument('--remote-debugging-port=9222')
	#options.binary_location = "/app/.apt/usr/bin/google-chrome"
	chrome_driver_binary="/home/abhi/git/mysite/venv/bin/chromedriver"
	driver= webdriver.Chrome(chrome_options=options)
	driver.implicitly_wait(3)
	driver.get(url)
	WebDriverWait(driver, timeout=10).until(lambda x: x.find_elements_by_tag_name('body'))
	page_source=driver.page_source
	soup=BeautifulSoup(page_source,'html.parser')
	#---------------------------------------------------#
	#--------- Web Metric Calculation ------------------#
	#---------------------------------------------------#
	wordCount					= get_word_count(driver)				#Parameter 1
	textBodyRatio				= get_text_body_ratio(soup)				#Parameter 2
	emphText					= get_emph_body_text_percentage(driver)			#Parameter 3
	textPositionalChanges		= get_text_position_changes(soup)			#Parameter 4
	textClusters				= get_text_clusters(driver)				#Parameter 5
	visibleLinks				= get_visible_links(driver)				#Parameter 6
	pageSize					= get_page_size(driver)					#Parameter 7
	graphicsSize				= get_graphics_size(driver)				#Parameter 8
	graphicsCount 				= get_graphics_count(driver)				#Parameter 9  
	colorCount					= 10#get_color_count(driver)				#Parameter 10
	fontCount					= get_font_count(driver)				#Parameter 11
	
	driver.quit()
			
	if pageSize==0:
		graphicsPercent=0
	else:
		graphicsPercent=graphicsSize*100.0/pageSize
			
	if wordCount:
		print(wordCount,"\n", textBodyRatio/wordCount,"\n", emphText ,"\n", textPositionalChanges,"\n" , textClusters,"\n" , visibleLinks ,"\n", pageSize ,"\n",graphicsPercent,"\n", graphicsCount,"\n", colorCount,"\n", fontCount)
	else:
		print(wordCount,"\n 0.0 \n", emphText ,"\n", textPositionalChanges,"\n" , textClusters,"\n" , visibleLinks ,"\n", pageSize ,"\n",graphicsPercent,"\n", graphicsCount,"\n", colorCount,"\n", fontCount)
			
if __name__=="__main__":
	url=sys.argv[-1]
	main(url)	
