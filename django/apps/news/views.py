from django.views.generic import dates
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
#from django.core.exceptions import ValidationError, NON_FIELD_ERRORS
from django.contrib.auth.decorators import permission_required
from django.contrib import messages
from .models import Article
from .forms import AddNewForm
from .newsgrab import get_metadata


# q: login_url='/loginpage/'
# @todo check if url is alive? (if no newsgrap support)
@permission_required ('news.add_article')
def add_new (request):
    if request.method != 'POST':
        return render (request, 'news/add-new.html')
        #form = AddNewForm1()
        #return render (request, 'news/add-new.html', dict(form=form))

    step = int(request.POST.get('step', 1))
    url = request.POST['url'].strip()
    if step == 1:
        # Check if already exists. @todo check canonical url also
        if Article.objects.filter(url=url).exists():
            messages.warning(request, u'Den lenken har vi allerede. Ellers takk :)')
            return redirect (request.path)
        # Try to init form with metadata
        #form = AddNewForm (initial=get_metadata(url))
        data = get_metadata(url)
        if not data: data = dict(url=url)
        form = AddNewForm (initial=data)
        form.fields['url'].widget.attrs['readonly'] = True
    else:
        # Step 2: Save form
        form = AddNewForm (request.POST)
        if form.is_valid():
            # Note: Does not call full_clean(), so will get IntegrityError
            # from db about url column not uniqie.
            #obj = Article.objects.create (**form.cleaned_data)

            # Note: If full_clean() raises error, it's not converted
            # to an validation error.
            try:
                obj = Article (**form.cleaned_data)
                obj.full_clean()
                obj.save()
                messages.success (request, u'Lagt til nyhet: "%s"' % obj.title)
                return redirect (request.path)
            except ValidationError as e:
                form._errors.update (e.message_dict)
                # @todo can raise forms.ValidationError() to propagate error?
                #       note: this is a non-field-error
                # self._errors["subject"] = self.error_class([msg])
                #form._errors = e.update_error_dict (form._errors)
                # form._errors.setdefault (NON_FIELD_ERRORS, self.error_class()).extend(messages)
                # Form.add_error(field, error)  # Django 1.7
                #non_field_errors = e.message_dict[NON_FIELD_ERRORS]

    return render (request, 'news/add-new.html', dict(form=form, step=step, url=url))



def detail (request, news_id):
    return render (request, 'news/detail.html', {
        'item': get_object_or_404 (Article, pk=news_id)
        # @todo use same name as DetailView uses. (object?)
    })



class ArchiveView (dates.ArchiveIndexView):
    model = Article
    date_field = 'date'
    paginate_by = 25
    #context_object_name = 'list'    # object_list
    #date_list_period = 'year'
    #allow_future = False
    # get_dated_queryset(**lookup)
    # get_date_list(queryset, date_type=None, ordering='ASC')
    # @todo get from cache (same query as sub-menu does. cache queryset?)
#    def get_date_list(queryset, date_type=None, ordering='ASC'):
#        return [datetime(2002,1,1), datetime(2004,1,1), datetime(2006,1,1)]
archive = ArchiveView.as_view()


# ArchiveYearView
# @todo show months in revered order?
class YearView (dates.YearArchiveView):
    model = Article
    date_field = 'date'
    make_object_list = True     # False => only generate month list
archive_year = YearView.as_view()


# ArchiveMonthView
class MonthView (dates.MonthArchiveView):
    model = Article
    date_field = 'date'
    month_format = '%m'
    make_object_list = True
archive_month = MonthView.as_view()
