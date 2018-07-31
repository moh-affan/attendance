from pegawai.models import Pegawai


def isloggedin(request):
    islog = 'pegawai_id' in request.session and 'jenis_akun' in request.session and 'username' in request.session
    return islog


def get_pegawai(request):
    if isloggedin(request):
        pegawai = Pegawai.objects.get(id=request.session['pegawai_id'])
        return pegawai
    return None
