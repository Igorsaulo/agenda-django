from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from .models import Contact

class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', 'last_name', 'email', 'phone', 'picture', 'description', 'category']
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'email': 'E-mail',
            'phone': 'Telefone',
            'description': 'Descrição',
            'category': 'Categoria',
             'picture': 'Foto',
        }
        
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o primeiro nome'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o sobrenome'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o e-mail'}),
            'phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o telefone'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Digite a descrição'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'picture': forms.FileInput(attrs={'class': 'form-control', 'id': 'img-input'}),
        }
        
        
    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.fields['category'].empty_label = 'Selecione'
        self.fields['description'].required = False
        self.fields['last_name'].required = False
        self.fields['email'].required = False
        self.fields['picture'].required = False
        
    def clean(self):
        cleaned_data = super().clean()
        last_name = cleaned_data.get('last_name')
        first_name = cleaned_data.get('first_name')
        phone = cleaned_data.get('phone')
        
        self.validatorText(last_name, 'last_name')
        self.validatorText(first_name, 'first_name')
        self.validatorPhone(phone)
        
    def validatorText(self, text, field_name):
        if text and text.isalpha() == False:
            self.add_error(field_name, f'O campo {field_name.replace("first_name", "Nome").replace("last_name", "Sobrenome")} deve conter apenas letras')
    
    def validatorPhone(self, phone):
        if phone.isnumeric() == False:
            self.add_error('phone', 'O telefone deve conter apenas números')
    

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email','first_name', 'last_name',]
        labels = {
            'first_name': 'Nome',
            'last_name': 'Sobrenome',
            'username': 'Nome de usuário',
            'email': 'E-mail'
        }
        
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite o nome de usuário'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Digite o e-mail'}),
        }
        
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este e-mail já está em uso')
        return email
    

class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True,
        min_length=3,
    )
    last_name = forms.CharField(
        required=True,
        min_length=3,
    )
    email = forms.EmailField()

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username', 'password1', 'password2',
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')

        if User.objects.filter(email=email).exists():
            self.add_error(
                'email',
                ValidationError('Já existe este e-mail', code='invalid')
            )

        return email


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label="Nome",
        min_length=2,
        max_length=30,
        required=True,
        help_text='Campo obrigatório',
        error_messages={
            'min_length': 'Nome deve ter no mínimo 2 caracteres',
        }
    )
    last_name = forms.CharField(
        label="Sobrenome",
        min_length=2,
        max_length=30,
        required=True,
        help_text='Campo obrigatório',
    )

    password1 = forms.CharField(
        label="Senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False,
    )

    password2 = forms.CharField(
        label="Confirme a senha",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password"}),
        help_text='As senhas devem ser iguais.',
        required=False,
    )

    class Meta:
        model = User
        fields = (
            'first_name', 'last_name', 'email',
            'username',
        )

    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user = super().save(commit=False)
        password = cleaned_data.get('password1')

        if password:
            user.set_password(password)

        if commit:
            user.save()

        return user

    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 or password2:
            if password1 != password2:
                self.add_error(
                    'password2',
                    ValidationError('Senhas não batem')
                )

        return super().clean()

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email

        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error(
                    'email',
                    ValidationError('Já existe este e-mail', code='invalid')
                )

        return email

    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')

        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as errors:
                self.add_error(
                    'password1',
                    ValidationError(errors)
                )

        return password1