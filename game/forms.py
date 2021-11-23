from django import forms
from django.core import validators
from django.contrib.auth.models import User

def validate_location(value):
    columns = ['a','b','c','d','e','f','g','h']
    char1 = [ele for ele in columns if(value[0] in ele)]
    char2 = [ele for ele in columns if(value[2] in ele)]
    if ((not char1) or  (not char2) or (not value[1].isdigit()) or (not value[3].isdigit())):
        raise forms.ValidationError("Use row and column format, e.g. a2a4.")
    if ((int(value[1]) < 1 or int(value[1]) > 8) or (int(value[3]) < 1 or int(value[3]) > 8)):
        raise forms.ValidationError("Enter an integer from 1 to 8.")




class ChessForm(forms.Form):
    location=forms.CharField(min_length=4, max_length=4, strip=True,
        widget=forms.TextInput(attrs={'placeholder':'a1c1','style':'font-size:small'}),
        validators=[validators.MinLengthValidator(4),
        validators.MaxLengthValidator(4),
        validate_location])
