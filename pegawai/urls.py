from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='pegawai_index'),
    url(r'^(?P<nip>[0-9]+)/$', views.view_pegawai, name='pegawai_view'),
    url(r'^(?P<nip>[0-9]+)/delete/$', views.del_pegawai, name='pegawai_delete'),
    url(r'^add/$', views.store_pegawai, name='pegawai_add'),
    url(r'^jabatan/$', views.jabatan, name='jabatan_index'),
    url(r'^jabatan/(?P<id>[0-9]+)/$', views.view_jabatan, name='jabatan_view'),
    url(r'^jabatan/(?P<id>[0-9]+)/delete/$', views.del_jabatan, name='jabatan_delete'),
    url(r'^jabatan/add/$', views.store_jabatan, name='jabatan_add'),
]
