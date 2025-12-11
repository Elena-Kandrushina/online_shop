from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class UserRegisterCreationForm(UserCreationForm):
    phone_number = forms.CharField(max_length=15, required=False, help_text='Необязательное поле. Введите ваш номер телефона.')
    country = forms.CharField(max_length=35, required=False, help_text='Введите страну.')
    avatar = forms.ImageField(required=False, help_text='Загрузите фото.')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('email', 'password1', 'password2', 'phone_number', 'country', 'avatar')

    def clean_phone_number(self):
        phone_number = self.cleaned_data.get('phone_number')
        if phone_number and not phone_number.isdigit():
            raise forms.ValidationError('Номер телефона должен состоять из цифр.')
        return phone_number

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in ['email', 'phone_number', 'country']:
            self.fields[field_name].widget.attrs.update({'class': 'form-control'})
        self.fields['avatar'].widget.attrs.update({'class': 'form-control-file'})