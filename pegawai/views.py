# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import json

from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404

from pegawai.forms import PegawaiForm, JabatanForm
from pegawai.models import Pegawai, Jabatan


# Create your views here.


def index(request):
    return render(request, 'admin\pegawai.html', {'active': 'pegawai'})


def store_pegawai(request):
    if request.method == 'POST':
        form = PegawaiForm(data=request.POST)
    else:
        form = PegawaiForm()
    if form.is_valid():
        form.save()
        return redirect('pegawai_index')
    context = {'form': form, 'active': 'pegawai'}
    return render(request, 'admin\pegawai_add.html', context)


def api_get_pegawai(request):
    peg = Pegawai.objects.all().exclude(id=0)
    data = []
    for pegawai in peg:
        data.append({
            'id': '',
            'nip': pegawai.nip,
            'nama': pegawai.nama,
            'tgl_lahir': pegawai.tgl_lahir.isoformat(),
            'alamat': pegawai.alamat,
            'jenis_kelamin': pegawai.jenis_kelamin,
            'no_hp': pegawai.no_hp,
            'jabatan': pegawai.jabatan.nama
        })
    return HttpResponse(json.dumps({'data': data}), content_type='application/json')


def api_get_pegawai_dd(request):
    peg = Pegawai.objects.all().exclude(id=0)
    data = []
    for pegawai in peg:
        data.append({
            'value': pegawai.id,
            'name': pegawai.nama,
        })
    return HttpResponse(json.dumps({'data': data}), content_type='application/json')


def view_pegawai(request, nip):
    pegawai = get_object_or_404(Pegawai, nip=nip)
    form = PegawaiForm(instance=pegawai)
    if request.method == 'POST':
        form = PegawaiForm(data=request.POST, instance=pegawai)
        if form.is_valid():
            form.save()
            return redirect('pegawai_index')
    context = {'form': form, 'active': 'pegawai'}
    return render(request, 'admin\pegawai_edit.html', context)


def del_pegawai(request, nip):
    pegawai = get_object_or_404(Pegawai, nip=nip)
    pegawai.delete()
    return redirect('pegawai_index')


def jabatan(request):
    return render(request, 'admin\jabatan.html', {'active': 'jabatan'})


def store_jabatan(request):
    # return HttpResponse("Jabatan Add")
    if request.method == 'POST':
        form = JabatanForm(data=request.POST)
    else:
        form = JabatanForm()
    if form.is_valid():
        form.save()
        return redirect('jabatan_index')
    context = {'form': form, 'active': 'jabatan'}
    return render(request, 'admin\jabatan_add.html', context)


def api_get_jabatan(request):
    peg = Jabatan.objects.all()
    data = []
    for jabatan in peg:
        data.append({
            'idx': '',
            'id': jabatan.id,
            'nama': jabatan.nama,
        })
    return HttpResponse(json.dumps({'data': data}), content_type='application/json')


def view_jabatan(request, id):
    jabatan = get_object_or_404(Jabatan, pk=id)
    form = JabatanForm(instance=jabatan)
    if request.method == 'POST':
        form = JabatanForm(data=request.POST, instance=jabatan)
        if form.is_valid():
            form.save()
            return redirect('jabatan_index')
    context = {'form': form, 'active': 'jabatan', 'id': id}
    return render(request, 'admin\jabatan_edit.html', context)


def del_jabatan(request, id):
    jabatan = get_object_or_404(Jabatan, pk=id)
    jabatan.delete()
    return redirect('jabatan_index')
