from django.conf.urls import patterns, url

urlpatterns = patterns('budget.views',
    url(r'^$', 'index'),
)