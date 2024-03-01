from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from .models import User


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
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


class UserLoginForm(forms.Form):
    phone = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='شماره موبایل')
    password = forms.CharField(max_length=250, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='رمز عبور')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        user = User.objects.filter(phone=phone).first()
        if len(phone) != 11:
            raise forms.ValidationError('شماره ی تماس باید 11 رقم باشد.')
        if not phone.startswith('09'):
            raise forms.ValidationError('شماره ی تماس باید با 09 شروع شود.')
        if not phone.isdigit():
            raise forms.ValidationError('شماره ی تماس باید فقط شامل اعداد باشد.')
        if not user:
            raise forms.ValidationError('رمز عبور یا شماره موبایل صحیح نیست.')

        return phone

    def clean_password(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(phone=phone).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError('رمز عبور یا شماره موبایل صحیح نیست.')
        return password


class UserRegisterForm(forms.Form):
    first_name = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 label='نام')
    last_name = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                                label='نام خانوادگی')
    phone = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='شماره موبایل')
    password = forms.CharField(max_length=250, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='رمز عبور')
    password2 = forms.CharField(max_length=250, required=True,
                                widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='تایید رمز عبور')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if len(phone) != 11:
            raise forms.ValidationError('شماره ی تماس باید 11 رقم باشد.')
        if not phone.startswith('09'):
            raise forms.ValidationError('شماره ی تماس باید با 09 شروع شود.')
        if not phone.isdigit():
            raise forms.ValidationError('شماره ی تماس باید فقط شامل اعداد باشد.')
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('شماره ی تماس تکراری است.')

        return phone

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if len(password2) <= 8:
            raise forms.ValidationError('رمز عبور باید باید حداقل 8 رقم باشد.')
        if password1 != password2:
            raise forms.ValidationError('رمز عبور ها متفاوت هستند.')
        return password2
