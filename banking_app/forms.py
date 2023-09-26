from django import forms

class regform(forms.Form):
    firstname=forms.CharField(max_length=50)
    lastname=forms.CharField(max_length=50)
    username = forms.CharField(max_length=50)
    phone = forms.IntegerField()
    email=forms.EmailField()
    image=forms.FileField()
    pin=forms.CharField(max_length=20)
    confirmpin=forms.CharField(max_length=20)

class logform(forms.Form):
    username=forms.CharField(max_length=20)
    pin=forms.CharField(max_length=20)

class newsform(forms.Form):
    topic=forms.CharField(max_length=300)
    content=forms.CharField(max_length=5000)

class adminform(forms.Form):
    username=forms.CharField(max_length=20)
    password=forms.CharField()

