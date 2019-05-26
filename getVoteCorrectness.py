from pollSite.models import siteUrl,Entries,Person

l=[]
for objPerson in Person.objects.all():
	temp=0.0
	n=0
	for objSiteUrl in siteUrl.objects.all():
		for objEntries in Entries.objects.filter(personId=objPerson.id,urlId=objSiteUrl.id):
			if objPerson.name== 'radha':
				print(objSiteUrl.id,float(objEntries.rating),float(objSiteUrl.rating))
			temp+=abs(float(objEntries.rating)-float(objSiteUrl.rating))
			n+=1
	try:
		l.append([temp/n,objPerson.name,objPerson.id,n])
	except:
		l.append([1111,objPerson.name,objPerson.id,n])
l.sort()
for i in l:
	print(i)
