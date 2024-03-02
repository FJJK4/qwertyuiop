from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from .models import Profile


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Логин', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Логин"}))
    password1= forms.CharField(label='Пароль', required= True , widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder':"Пароль"}))
    password2 = forms.CharField(label='Подтверждение пароля', required= True , widget=forms.PasswordInput(attrs={'class': 'form-control mb-3', 'placeholder':"Подтверждение пароля"}))
    email = forms.EmailField(label='Почта', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Почта"}))
    first_name = forms.CharField(label='Имя', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Имя"}))
    last_name = forms.CharField(label='Логин', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Фамилия"}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'first_name', 'last_name')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
            return user
        

class ProfileForm(forms.ModelForm):
    username = forms.CharField(label='username', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"username"}))
    email = forms.EmailField(label='Почта', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Почта"}))
    first_name = forms.CharField(label='Имя', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Имя"}))
    last_name = forms.CharField(label='Логин', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Фамилия"}))
    text = forms.CharField(label='Описание', required= True , widget=forms.TextInput(attrs={'class': 'form-control mb-3', 'placeholder':"Описание"}))
    avatar = forms.FileField(label='Аватар', required= True , widget=forms.FileInput(attrs={'class': 'form-control mb-3', 'placeholder':"Аватар"}))
    birth_date = forms.DateField(label='День рождения', required= True , widget=forms.DateInput(attrs={'class': 'form-control mb-3', 'placeholder':"День рождения"}))
    phone = forms.IntegerField(label='Номер', required= True , widget=forms.NumberInput(attrs={'class': 'form-control mb-3', 'placeholder':"Номер"}))
    
    class Meta:
        model = Profile
        fields = ['username','first_name', 'last_name', 'email', 'text', 'avatar', 'birth_date', 'phone']
    

    def profile_save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.text = self.cleaned_data['text']
        user.avatar = self.cleaned_data['avatar']
        user.birth_date = self.cleaned_data['birth_date']
        user.phone = self.cleaned_data['Номер']

        if commit:
            user.profile_save()
            return user