from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Select, FileInput, PasswordInput

from works.models import Work


class WorkForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['work_type'].empty_label = '---Выберите тип работы---'

    class Meta:
        model = Work
        fields = ['name', 'work_type', 'file']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название работы'}),
            'work_type': Select(attrs={'class': 'form-control'}),
            'file': FileInput(attrs={'class': 'form-control-file'}),
        }


class RegisterUserForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
        widgets = {
            'username': TextInput(attrs={'class': 'form-control'}),
            'password1': PasswordInput(attrs={'class': 'form-control'}),
            'password2': PasswordInput(attrs={'class': 'form-control'}),
        }
