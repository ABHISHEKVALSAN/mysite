from pollSite.models import Entries
import csv
csvFile		= open('entries.csv','w')
writer		= csv.writer(csvFile)
writer.writerow(['id','personId','siteId','rating'])
num=1
for obj in Entries.objects.all():
	a=obj.id
	b=obj.personId.id
	c=obj.urlId.id
	d=obj.rating
	print(a,b,c,d,num)
	num+=1
	writer.writerow([a,b,c,d])
csvFile.close()
