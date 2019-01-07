from pollSite.models import siteUrl
import csv
csvFile		= open('urls.csv','w')
writer		= csv.writer(csvFile)
writer.writerow(['id','urls'])
it=1
for obj in siteUrl.objects.all():
	print(it,obj.urlText)
	writer.writerow([it,obj.urlText])
	it+=1
csvFile.close()
