import datetime

from django import forms
from django.conf import settings



from django import forms

class UploadFileForm(forms.Form):
    ofac_file = forms.FileField(required=False)
    un_file = forms.FileField(required=False)
    eu_file = forms.FileField(required=False)
