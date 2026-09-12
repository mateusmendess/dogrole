from django import forms


class SignupForm(forms.Form):
    username = forms.CharField(max_length=150)
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    city = forms.CharField(max_length=100)
    phone = forms.CharField(max_length=20, required=False)