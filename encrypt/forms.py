from django.forms import ModelForm
from .models import Uploads


class UploadsForm(ModelForm):
    class meta:
        model = Uploads
        fields = ('description', 'text_file')
