from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Client
class UserForm(UserCreationForm):    
        sexe_choice = (("homme","homme"),
                ("femme","femme"))
        email = forms.EmailField()
        fields = ("username","email","gender","password1","password2")
        def clean_gender(self):
            data = self.cleaned_data["gender"]
            return data

        def save(self, commit=True):
            user = super(UserForm, self).save(commit=False)
            user.email = self.cleaned_data["email"]
            if self.is_valid():
                user.save()
            return user
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ("username","lastname","adresse","phone","email")
        widgets={
                   "username":forms.TextInput(attrs={'placeholder':'Prenom','name':'username','class':'form-control'}),
                   "adresse":forms.TextInput(attrs={'placeholder':'Rue xxx 8x0x...','name':'addresse','class':'form-control'}),
                   "email":forms.TextInput(attrs={'placeholder':'xyz@gmail.com','email':'email','class':'form-control'}),
                   "phone":forms.TextInput(attrs={'placeholder':'8 chiffres','phone':'phone','class':'form-control'}),
                   "lastname":forms.TextInput(attrs={'placeholder':'Nom','lastname':'lastname','class':'form-control'}),
                   "gender":forms.Select(attrs={"name": "Gender","class": "form-select"})
                }  
