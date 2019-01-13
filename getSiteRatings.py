from pollSite.models import siteUrl
import csv
csvFile		= open('siteRatings.csv','w')
writer		= csv.writer(csvFile)
writer.writerow(['id','rateCount','rating'])
for obj in siteUrl.objects.all():
	siteId=obj.id
	rating=0.0
	rating+=obj.rate7*7
	rating+=obj.rate6*6
	rating+=obj.rate5*5
	rating+=obj.rate4*4
	rating+=obj.rate3*3
	rating+=obj.rate2*2
	rating+=obj.rate1*1
	rateCount=obj.rate7+obj.rate6+obj.rate5+obj.rate4+obj.rate3+obj.rate2+obj.rate1
	try:
		rating/=rateCount
	except:
		rating=0.0
	print(siteId,rateCount,round(rating,2))
	writer.writerow([siteId,rateCount,rating])
csvFile.close()
