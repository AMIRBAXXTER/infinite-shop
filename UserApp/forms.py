from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11:
            raise forms.ValidationError('phone number must be 11 digits')
        return phone


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11:
            raise forms.ValidationError('شماره ی تماس باید 11 رقم باشد.')
        if not phone.startswith('09'):
            raise forms.ValidationError('شماره ی تماس باید با 09 شروع شود.')
        if not phone.isdigit():
            raise forms.ValidationError('شماره ی تماس باید فقط شامل اعداد باشد.')
        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('شماره ی تماس تکراری است.')
        return phone
