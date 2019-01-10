import csv
from pollSite.models import siteUrl
csvFile=open("urls.csv","r")
urlFile=csv.DictReader(csvFile)
for row in urlFile:
	siteUrl.objects.create(urlText=row['urls'])
