from django.forms import ModelForm, TextInput, Select, FileInput

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
