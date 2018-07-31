from beranda import auth


def isloggedin(request):
    return {'isloggedin': auth.isloggedin(request)}


def pegawai(request):
    return {'pegawai': auth.get_pegawai(request)}
