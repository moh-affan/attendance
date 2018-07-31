# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.contrib.auth import authenticate, logout, login
from django.contrib import messages
from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404

# Create your views here.
from absensi.models import Log
from beranda import auth
from pegawai.models import Akun, Pegawai


def index(request):
    is_searcing = False
    nama = ""
    tanggal = ""
    logs = []
    if request.method == 'POST':
        is_searcing = True
        nama = request.POST['nama']
        tanggal = request.POST['tgl']
        tgl = "{}".format(tanggal).split('-')
        y = int(tgl[0])
        m = int(tgl[1])
        d = int(tgl[2])
        dt = datetime.datetime(year=y, month=m, day=d)
        logs = Log.objects.filter(waktu_masuk__date=dt, pegawai__nama__icontains=nama).order_by('-waktu_masuk')

    return render(request, 'beranda.html',
                  {'nama': nama, 'tanggal': tanggal, 'logs': logs, 'is_searching': is_searcing})


def login_view(request):
    if request.POST:
        user = authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is not None:
            if user.is_active:
                try:
                    akun = Akun.objects.get(akun=user.id)
                    login(request, user)
                    request.session['pegawai_id'] = akun.pegawai.id
                    request.session['jenis_akun'] = akun.jenis_akun
                    request.session['username'] = request.POST['username']
                    return redirect('/admin')
                except:
                    messages.add_message(request, messages.INFO,
                                         'Akun ini belum terhubung dengan data pegawai, silahkan hubungi administrator')
            else:
                messages.add_message(request, messages.INFO, 'User belum terverifikasi')
        else:
            messages.add_message(request, messages.INFO, 'Username atau password Anda salah')
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    request.session.flush()
    return redirect('/login/')


def dashboard(request):
    if not auth.isloggedin(request):
        return redirect('/login/')
    c_hadir = Log.objects.filter(waktu_masuk__year=datetime.datetime.today().strftime('%Y'),
                                 waktu_masuk__month=datetime.datetime.today().strftime('%m'), status='H').exclude(pegawai_id=0).count()
    c_alpa = Log.objects.filter(waktu_masuk__year=datetime.datetime.today().strftime('%Y'),
                                waktu_masuk__month=datetime.datetime.today().strftime('%m'), status='A').exclude(pegawai_id=0).count()
    c_sakit = Log.objects.filter(waktu_masuk__year=datetime.datetime.today().strftime('%Y'),
                                 waktu_masuk__month=datetime.datetime.today().strftime('%m'), status='S').exclude(pegawai_id=0).count()
    c_ijin = Log.objects.filter(waktu_masuk__year=datetime.datetime.today().strftime('%Y'),
                                waktu_masuk__month=datetime.datetime.today().strftime('%m'), status='I').exclude(pegawai_id=0).count()
    c_absen = [c_hadir, c_ijin, c_sakit, c_alpa]
    return render(request, 'admin\dashboard.html', {'c_absen': c_absen})
