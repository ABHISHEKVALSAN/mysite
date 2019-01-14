from pollSite.models import siteUrl
import csv
csvFile		= open('data_Y.csv','w')
writer		= csv.writer(csvFile)
writer.writerow(['rating'])
for obj in siteUrl.objects.all():
	siteId=obj.id
	siteRating=obj.rating
	siteZRating= (siteRating-1.0)/7.0
	print(siteId,siteZRating)
	writer.writerow([siteZRating])
csvFile.close()
