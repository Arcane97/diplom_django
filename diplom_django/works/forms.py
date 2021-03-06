from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Select, FileInput, PasswordInput, CheckboxInput, Form, ModelChoiceField, \
    NumberInput

from works.models import Work, WorkType, AcademicYear


class WorksFilterForm(Form):
    work_type = ModelChoiceField(label="", queryset=WorkType.objects.all(), empty_label=None, to_field_name="url_slug",
                                 widget=Select(attrs={'class': 'form-control'}))
    academic_year = ModelChoiceField(label="", queryset=AcademicYear.objects.all(), empty_label=None,
                                     to_field_name="url_slug",
                                     widget=Select(attrs={'class': 'form-control'}))


class WorkForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = Work
        fields = ['name', 'file']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название работы'}),
            # 'work_type': Select(attrs={'class': 'form-control'}),
            # 'file': FileInput(attrs={'class': 'form-control-file'}),
        }


class WorkFormCreate(WorkForm):
    # academic_year = ModelChoiceField(label="Учебный год", queryset=AcademicYear.objects.all(), empty_label=None,
    #                                  to_field_name="url_slug",
    #                                  widget=Select(attrs={'class': 'form-control'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['academic_year'].empty_label = None
        self.fields['owner'].empty_label = '--- Выберите студента ---'

    class Meta:
        model = Work
        fields = ['name', 'academic_year', 'file', 'owner', 'grade', 'is_accepted']
        widgets = {
            'name': TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название работы'}),
            'work_type': Select(attrs={'class': 'form-control'}),
            'academic_year': Select(attrs={'class': 'form-control'}),
            'owner': Select(attrs={'class': 'form-control'}),
            'grade': NumberInput(attrs={'class': 'form-control'}),
            'is_accepted': CheckboxInput(attrs={'class': 'form-check-input lg',
                                                'style': 'margin-left:20px; margin-top:8px; transform: scale(1.5); '
                                                         '-webkit-transform: scale(1.5);'}),
            # 'file': FileInput(attrs={'class': 'form-control-file'}),
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


class LoginUserForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'

    # class Meta:
    #     model = User
    #     fields = ['username', 'password1', 'password2']
    #     widgets = {
    #         'username': TextInput(attrs={'class': 'form-control'}),
    #         'password1': PasswordInput(attrs={'class': 'form-control'}),
    #         'password2': PasswordInput(attrs={'class': 'form-control'}),
    #     }
