from django.shortcuts import render
#from django.contrib import messages


def mypage (request):
    ctx = {}
    #ctx['title'] = 'My Page'
    ctx['has_permission'] = True    # enable block usertools
    #messages.info (request, 'All is fine')
    return render (request, 'erp/mypage.html', ctx)


def index (request):
    ctx = {}
    ctx['has_permission'] = True
    return render (request, 'erp/index.html', ctx)
