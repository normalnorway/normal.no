import init_django
from apps.news.models import Article

#print Article.objects.all()
for o in Article.objects.all():
    print o


#o = Article (title="testing", url=None)
#o.full_clean() # validation
#print o
#o.save()

#Article.objects.filter (title="testing").delete()

#qs = Article.objects.filter (title="TITLE")
#qs.delete()

#print Article.objects.filter (title="testing")
#print Article.objects.filter (url='')
#print Article.objects.filter (url=None)    # url is null
