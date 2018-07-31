# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
from pegawai.models import Pegawai


class Log(models.Model):
    CHOICES = (('H', 'Hadir'), ('A', 'Tanpa Keterangan'), ('I', 'Ijin'), ('S','Sakit'))
    pegawai = models.ForeignKey(Pegawai, related_name='log', blank=True)
    keterangan = models.CharField(max_length=200)
    status = models.CharField(max_length=1, choices=CHOICES, default='H')
    waktu_masuk = models.DateTimeField(auto_now=False)
    waktu_keluar = models.DateTimeField(auto_now=False, blank=True)

    def __str__(self):
        return "{}/{}/{} {}:{} - {} {}".format(self.waktu_masuk.day, self.waktu_masuk.month, self.waktu_masuk.year, self.waktu_masuk.hour,
                                               self.waktu_masuk.minute, self.pegawai.nip,
                                               self.pegawai.nama)


# class Absensi(models.Model):
#     CHOICES = ['H','A','I','S']
#     pegawai = models.ForeignKey(Pegawai, related_name='absensi', blank=False)
#     status_kedatangan = models.CharField(max_length=200)
#     keterangan = models.CharField(max_length=200)
#     def __str__(self):
#         return ""
