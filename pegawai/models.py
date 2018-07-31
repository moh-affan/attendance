# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class Jabatan(models.Model):
    nama = models.CharField(max_length=50)

    def __str__(self):
        return self.nama


class Pegawai(models.Model):
    JENIS_KELAMIN = (
        ('L', 'Laki-Laki'),
        ('P', 'Perempuan')
    )
    nip = models.CharField(max_length=18, unique=True)
    nama = models.CharField(max_length=255)
    tgl_lahir = models.DateField()
    alamat = models.CharField(max_length=255)
    jenis_kelamin = models.CharField(max_length=1, choices=JENIS_KELAMIN)
    no_hp = models.CharField(max_length=15, unique=True)
    jabatan = models.ForeignKey(Jabatan, related_name='pegawai')

    def __str__(self):
        return self.nip


class Akun(models.Model):
    JENIS_AKUN_CHOICES = (
        ('pegawai', 'Pegawai'),
        ('admin', 'Administrator'),
    )
    akun = models.ForeignKey(User)
    pegawai = models.ForeignKey(Pegawai)
    jenis_akun = models.CharField(max_length=20, choices=JENIS_AKUN_CHOICES)

    def __str__(self):
        return self.pegawai.nip
