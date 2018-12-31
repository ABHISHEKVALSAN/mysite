from pollSite.models import Entries
import csv
csvFile		= open('entries.csv','w')
writer		= csv.writer(csvFile)
writer.writerow(['entryId','personId','siteId','rating'])
for obj in Entries.objects.all():
	a=obj.id
	b=obj.personId.id
	c=obj.urlId.id
	d=obj.rating
	print(a,b,c,d)
	writer.writerow([a,b,c,d])
csvFile.close()
