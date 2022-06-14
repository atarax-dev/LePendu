from django import forms
from django.core.validators import RegexValidator


class LetterForm(forms.Form):
    letter_try = forms.CharField(
        label='Choisissez une lettre :',
        widget=forms.TextInput(attrs={'placeholder': '  Lettre'}),
        validators=[RegexValidator(regex='^[a-zA-Z]{1}$',
                                   message="N'entrez qu'une seule lettre")])
