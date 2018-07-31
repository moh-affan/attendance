from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^get_all/', views.api_get_pegawai, name='api_get_pegawai'),
    url(r'^get_dropdown/', views.api_get_pegawai_dd, name='api_get_pegawai_dd'),
    url(r'^jabatan/get_all/', views.api_get_jabatan, name='api_get_jabatan'),
]
