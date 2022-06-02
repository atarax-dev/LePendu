from django import forms
from django.core.validators import RegexValidator


class LetterForm(forms.Form):
    letter_try = forms.CharField(
        label='Votre réponse',
        widget=forms.TextInput(attrs={'placeholder': 'Entrez une lettre'}),
        validators=[RegexValidator(regex='^[a-zA-Z]{1}$',
                                   message="N'entrez qu'une seule lettre")])
