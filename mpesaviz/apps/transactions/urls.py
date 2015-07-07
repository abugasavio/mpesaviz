from django.conf.urls import patterns
from . import views

urlpatterns = patterns('',)

urlpatterns.extend(views.TransactionCRUDL().as_urlpatterns())



