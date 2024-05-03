from django import forms
from babapp.models import register,forgot,password

class regform(forms.ModelForm):
    class Meta:
        model=register
        fields='__all__'
class forgotform(forms.ModelForm):
    class Meta:
        model=forgot
        fields=['Email']
class passform(forms.ModelForm):
    class Meta:
        model= password
        fields='__all__'