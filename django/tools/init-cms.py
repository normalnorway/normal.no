"""
Import old data into apps.cms
flatpages -> Page
"""
import initdjango
from datetime import datetime
from django.db import transaction
from django.contrib.flatpages.models import FlatPage
from apps.cms.models import Page

# TransactionManagementError: Your database backend doesn't behave
# properly when autocommit is off. Turn it on before using 'atomic'.
#transaction.set_autocommit (False) # note: the deprecated way?
# ...
#transaction.commit()

#Page.objects.all().delete()

# strip /sider/ prefix
def transform (obj):
    if obj['url'].startswith ('/sider/'):
        obj['url'] = obj['url'][7:]
    #return obj # must/shoud return None when called with filter()

with transaction.atomic(): # note needed, since bulk_create
    datalist = FlatPage.objects.values('pk', 'title', 'url', 'content')
    #for obj in datalist: transform (obj);
    filter (transform, datalist)
    Page.objects.bulk_create (Page(**item) for item in datalist)
