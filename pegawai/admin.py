# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

# Register your models here.
from pegawai.models import Jabatan, Pegawai, Akun

admin.site.register(Jabatan)
admin.site.register(Pegawai)
admin.site.register(Akun)