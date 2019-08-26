# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import base64
import json
import os
import cv2

import numpy as np
from datetime import datetime, date

from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from absensi.models import Log
from attendance.settings import BASE_DIR
from pegawai.models import Pegawai

FOTO_PATH = os.path.join(BASE_DIR, "foto")
YALE_FOTO_PATH = os.path.join(BASE_DIR, "orl")
pcaRecognizer = cv2.face.EigenFaceRecognizer_create(num_components=5)
fisherRecognizer = cv2.face.FisherFaceRecognizer_create()
lbphRecognizer = cv2.face.LBPHFaceRecognizer_create()
TEMP_DIR = os.path.join(BASE_DIR, "temp")


# pcaRecognizer = lbphRecognizer


def index(request):
    simpan = False
    if request.method == 'POST':
        faces = [str(request.POST['face_0']).encode('ascii'),
                 str(request.POST['face_1']).encode('ascii'),
                 str(request.POST['face_2']).encode('ascii'),
                 str(request.POST['face_3']).encode('ascii'),
                 str(request.POST['face_4']).encode('ascii'),
                 str(request.POST['face_5']).encode('ascii'),
                 str(request.POST['face_6']).encode('ascii'),
                 str(request.POST['face_7']).encode('ascii'),
                 str(request.POST['face_8']).encode('ascii'),
                 str(request.POST['face_9']).encode('ascii')]
        id_pegawai = request.POST['id_pegawai']
        save_faces(id_pegawai, faces)
        simpan = True
    return render(request, 'admin\\enrol.html', {'active': 'enrol', 'simpan': simpan})


def absensi(request):
    imgs, lbl = prepare_training_data(FOTO_PATH)
    print(pcaRecognizer.train(imgs, np.array(lbl)))
    # TEST
    data = cv2.imread(os.path.join(TEMP_DIR, 'tmp.png'))
    # data = cv2.imread(os.path.join(FOTO_PATH, '2_faces/1.png'))
    data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    pg, lbl = predict(data)
    print("pg")
    print(pg)
    print("label")
    print(lbl)
    if pg is not None:
        log = Log.objects.filter(pegawai_id=pg.id, waktu_masuk__date=date.today())
        if len(log) > 0:
            lg = Log.objects.get(pk=log[0].id)
            lg.waktu_keluar = datetime.now()
            lg.save(force_update=True)
        else:
            Log(keterangan="Wajah dikenali sebagai {}".format(pg.nama), pegawai=pg, status='H').save()
    else:
        Log(keterangan="Wajah tidak dikenali", status='A', pegawai_id=0, waktu_masuk=datetime.now()).save()
    # END TEST
    if request.method == 'POST':
        # data = np.array(request.POST['face'].split(','), 'uint8')
        face = str(request.POST['face']).encode('ascii')
        clear_dir(TEMP_DIR)
        save_face(TEMP_DIR, 'tmp', face)
        data = cv2.imread(os.path.join(TEMP_DIR, 'tmp.png'))
        data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        pg, lbl = predict(data)
        if pg is not None:
            log = Log.objects.filter(pegawai_id=pg.id, waktu_masuk__date=date.today())
            if len(log) > 0:
                lg = Log.objects.get(pk=log[0].id)
                lg.waktu_keluar = datetime.now()
                lg.save(force_update=True)
            else:
                Log(keterangan="Wajah dikenali sebagai {}".format(pg.nama), pegawai=pg, status='H',
                    waktu_masuk=datetime.now()).save()
        else:
            Log(keterangan="Wajah tidak dikenali", status='A', pegawai_id=0, waktu_masuk=datetime.now()).save()
    logs = Log.objects.filter(waktu_masuk__date=date.today())
    # return render(request, 'admin\\absensi.html', {'active': 'absen', 'logs': logs})
    return HttpResponse(pg)


def predict(test_img):
    face = test_img
    # img = test_img.copy()
    # face = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # print face
    # print len(face[0])
    label = pcaRecognizer.predict(face)
    try:
        pegawai = Pegawai.objects.get(pk=label)
    except:
        pegawai = None
    return pegawai, label


def prepare_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    for dir_name in dirs:
        label = int(dir_name.split('_')[0])
        subject_dir_path = data_folder_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            face = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if face is not None:
                faces.append(face)
                labels.append(label)
    return faces, labels


def save_faces(id_pegawai, faces):
    idx = 0
    dirname = os.path.join(FOTO_PATH, "{}_faces".format(id_pegawai))
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    clear_dir(dirname)

    for face in faces:
        with open(os.path.join(dirname, "{}.png".format(idx)), 'wb') as fh:
            fh.write(base64.decodestring(face))
        idx += 1
    return dirname


def save_face(dirname, name, face):
    if not os.path.exists(dirname):
        os.makedirs(dirname)
    clear_dir(dirname)
    with open(os.path.join(dirname, "{}.png".format(name)), 'wb') as fh:
        fh.write(base64.decodestring(face))


def clear_dir(dirname):
    image_paths = [os.path.join(dirname, f) for f in os.listdir(dirname)]
    for dir in image_paths:
        os.unlink(dir)


def manual(request):
    pegawai = Pegawai.objects.all().exclude(id=0)
    if request.method == 'POST':
        for pg in pegawai:
            try:
                log_id = request.POST['log_id[{}]'.format(pg.id)]
                status = request.POST['status[{}]'.format(pg.id)]
                keterangan = request.POST['keterangan[{}]'.format(pg.id)]
                if log_id != '':
                    log = Log.objects.get(pk=log_id)
                    log.pegawai_id = pg.id
                    log.keterangan = keterangan
                    log.status = status
                    log.waktu_masuk = datetime.now()
                else:
                    # insert log
                    log = Log(pegawai_id=pg.id, status=status, keterangan=keterangan, waktu_masuk=datetime.now())
                    log.save()
            except:
                print("POST tidak ditemukan")
    data = []
    for peg in pegawai:
        log = Log.objects.filter(pegawai_id=peg.id, waktu_masuk__date=date.today()).order_by('-waktu_masuk').exclude(
            id=0)
        if len(log) > 0:
            absen = {'id': peg.id, 'nip': peg.nip, 'nama': peg.nama, 'status': log[0].status,
                     'keterangan': log[0].keterangan, 'waktu': log[0].waktu_masuk, 'log_id': log[0].id}
        else:
            absen = {'id': peg.id, 'nip': peg.nip, 'nama': peg.nama, 'status': '',
                     'keterangan': '', 'waktu': '', 'log_id': ''}
        data.append(absen)
    return render(request, 'admin\manual.html', {'active': 'manual', 'data': data})


def api_get_log(request):
    logs = Log.objects.filter(waktu_masuk__date=date.today())
    data = ""
    for log in logs:
        data += '<li>{} - {}</li>'.format(log.waktu_masuk.strftime('%d/%m/%Y %H:%M: %S'), log.pegawai.nama)
    return HttpResponse(data)


def api_get_absensi(request):
    pegawai = Pegawai.objects.all().exclude(id=0)
    data = ""
    for peg in pegawai:
        log = Log.objects.filter(pegawai_id=peg.id, waktu_masuk__date=date.today()).exclude(pegawai_id=0)
        len(log)
        if len(log) > 0:
            mark = '<span class="glyphicon glyphicon-check text-success pull-right"></span>'
        else:
            mark = '<span class="glyphicon glyphicon-remove text-danger pull-right"></span>'
        data += '<li>{} - {} {}</li>'.format(peg.nip, peg.nama, mark)
    return HttpResponse(data)


def laporan(request):
    if request.method == 'POST':
        tanggal = request.POST['tanggal']
        tgl = "{}".format(tanggal).split('-')
        y = int(tgl[0])
        m = int(tgl[1])
        d = int(tgl[2])
        dt = datetime(year=y, month=m, day=d)
        logs = Log.objects.filter(waktu_masuk__date=dt).order_by('waktu_masuk').exclude(pegawai_id=0)
    else:
        logs = Log.objects.filter(waktu_masuk__date=date.today()).order_by('waktu_masuk').exclude(pegawai_id=0)
    return render(request, 'admin\laporan.html', {'active': 'laporan', 'data': logs})


def get_absen_graph(request):
    data = []
    pegs = Pegawai.objects.all().exclude(id=0)
    for peg in pegs:
        hcount = peg.log.filter(status='H').count()
        dt = {'y': "{}aKehadiran {}".format(peg.nama, hcount), 'item1': int(hcount)}
        data.append(dt)
    return HttpResponse(json.dumps(data), content_type='application/json')


def prepare_orl_training_data(data_folder_path):
    dirs = os.listdir(data_folder_path)
    faces = []
    labels = []
    for dir_name in dirs:
        label = int(dir_name.replace("s", ""))
        subject_dir_path = data_folder_path + "/" + dir_name
        subject_images_names = os.listdir(subject_dir_path)
        for image_name in subject_images_names:
            if image_name.startswith("."):
                continue
            image_path = subject_dir_path + "/" + image_name
            image = cv2.imread(image_path)
            face = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
            if face is not None:
                faces.append(face)
                labels.append(label)
    return faces, labels


def yale_test(request):
    imgs, lbl = prepare_orl_training_data(YALE_FOTO_PATH)
    pcaRecognizer.train(imgs, np.array(lbl))
    data = cv2.imread(os.path.join(YALE_FOTO_PATH, 's17/1.pgm'))
    data = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
    pg, lbl = predict(data)
    return HttpResponse("<h1>foto dikenali dengan subject {}</h1>".format(lbl))
