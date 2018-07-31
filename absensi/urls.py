from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^laporan/$', views.laporan, name='laporan_index'),
    url(r'^manual/$', views.manual, name='manual_index'),
    url(r'^enrol/$', views.index, name='enrol_index'),
    url(r'^$', views.absensi, name='absen_index'),
]
