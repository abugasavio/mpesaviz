from django.conf.urls import patterns, url
from . import views

urlpatterns = patterns('',
                       url('^data/$', views.GraphDataView.as_view(), name='data'),
                       )

urlpatterns.extend(views.TransactionCRUDL().as_urlpatterns())



