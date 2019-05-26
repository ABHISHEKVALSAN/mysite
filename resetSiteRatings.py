from pollSite.models import Entries,siteUrl
for siteObj in siteUrl.objects.all():
	siteObj.rate7=0
	siteObj.rate6=0
	siteObj.rate5=0
	siteObj.rate4=0
	siteObj.rate3=0
	siteObj.rate2=0
	siteObj.rate1=0
	siteObj.save()
for obj in Entries.objects.all():
	siteObj=siteUrl.objects.filter(id=obj.urlId.id)[0]
	if obj.rating==7:
		siteObj.rate7+=1
	if obj.rating==6:
		siteObj.rate6+=1
	if obj.rating==5:
		siteObj.rate5+=1
	if obj.rating==4:
		siteObj.rate4+=1
	if obj.rating==3:
		siteObj.rate3+=1
	if obj.rating==2:
		siteObj.rate2+=1
	if obj.rating==1:
		siteObj.rate1+=1
	rating=0.0
	rating+=siteObj.rate6*6
	rating+=siteObj.rate5*5
	rating+=siteObj.rate4*4
	rating+=siteObj.rate3*3
	rating+=siteObj.rate2*2
	rating+=siteObj.rate1*1
	rateCount=siteObj.rate7+siteObj.rate6+siteObj.rate5+siteObj.rate4+siteObj.rate3+siteObj.rate2+siteObj.rate1
	try:
		rating/=rateCount
	except:
		rating=0.0
	siteObj.rateCount	= rateCount
	siteObj.rating		= rating
	siteObj.save()
