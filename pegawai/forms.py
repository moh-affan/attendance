from django import forms

from pegawai.models import Pegawai, Jabatan


class PegawaiForm(forms.ModelForm):
    class Meta:
        model = Pegawai
        fields = '__all__'
        widgets = {
            'nip': forms.TextInput(attrs={'class': 'form-control'}),
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
            'tgl_lahir': forms.DateInput(attrs={'class': 'form-control'}),
            'alamat': forms.TextInput(attrs={'class': 'form-control'}),
            'no_hp': forms.TextInput(attrs={'class': 'form-control'}),
            'jabatan': forms.Select(attrs={'class': 'form-control'}),
            'jenis_kelamin': forms.Select(attrs={'class': 'form-control'})
        }


class JabatanForm(forms.ModelForm):
    class Meta:
        model = Jabatan
        fields = '__all__'
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control'}),
        }
