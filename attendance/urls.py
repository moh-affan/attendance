"""attendance URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from beranda import views as vberanda
from pegawai import urls as upegawai
from pegawai import api_urls as api_pegawai
from absensi import urls as uabsensi, views as v_absensi

urlpatterns = [
    url(r'^$', vberanda.index, name='index'),
    url(r'^login/', vberanda.login_view, name='login'),
    url(r'^api_get_logs/$', v_absensi.api_get_log, name='api_logs'),
    url(r'^api_get_absensi/$', v_absensi.api_get_absensi, name='api_absensi'),
    url(r'^get_absen_graph/$', v_absensi.get_absen_graph, name='api_graph'),
    url(r'^logout/', vberanda.logout_view, name='logout'),
    url(r'^adm/', admin.site.urls),
    url(r'^admin/pegawai/', include(upegawai)),
    url(r'^api/pegawai/', include(api_pegawai)),
    url(r'^admin/absen/', include(uabsensi)),
    url(r'^admin/$', vberanda.dashboard, name='dashboard'),
    url(r'^yale_test/$', v_absensi.yale_test, name='yale_test'),
]
