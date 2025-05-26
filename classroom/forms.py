from django import forms
from .models import Classroom

class ClassroomForm(forms.ModelForm):
    class Meta:
        model = Classroom
        fields = ['name', 'code', 'description', 'day_of_week', 'start_time', 'end_time']
        widgets = {
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'type': 'time'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Make the code field readonly
        self.fields['code'].widget.attrs['readonly'] = True
