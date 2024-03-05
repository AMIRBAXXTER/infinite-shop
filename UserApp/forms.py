from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from langdetect import detect

from .models import *


def check_phone(phone, self=None):
    if len(phone) != 11:
        raise forms.ValidationError('شماره ی تماس باید 11 رقم باشد.')
    if not phone.startswith('09'):
        raise forms.ValidationError('شماره ی تماس باید با 09 شروع شود.')
    if not phone.isdigit():
        raise forms.ValidationError('شماره ی تماس باید فقط شامل اعداد باشد.')
    if self is not None:
        if User.objects.filter(phone=phone).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('شماره ی تماس تکراری است.')
    else:
        if User.objects.filter(phone=phone).exists():
            raise forms.ValidationError('شماره ی تماس تکراری است.')
    return phone


def check_first_name(first_name):
    lang = detect(first_name)
    if lang != 'fa' and lang != 'ar' and lang != 'ur':
        raise forms.ValidationError('نام باید به زبان فارسی باشد.')
    return first_name


def check_last_name(last_name):
    lang = detect(last_name)
    if lang != 'fa' and lang != 'ar' and lang != 'ur':
        raise forms.ValidationError('نام خانوادگی باید به زبان فارسی باشد.')
    return last_name


class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return check_phone(phone, self)

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return check_first_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return check_last_name(last_name)


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User
        fields = ('phone', 'first_name', 'last_name', 'is_active', 'is_staff', 'is_superuser')

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return check_phone(phone, self)

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return check_first_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return check_last_name(last_name)


class UserLoginForm(forms.Form):
    phone = forms.CharField(max_length=250, required=True, widget=forms.TextInput(attrs={'class': 'form-control'}),
                            label='شماره موبایل')
    password = forms.CharField(max_length=250, required=True,
                               widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='رمز عبور')



    def clean_password(self):
        phone = self.cleaned_data.get('phone')
        password = self.cleaned_data.get('password')
        user = User.objects.filter(phone=phone).first()
        if  not user or not user.check_password(password):
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
        return check_phone(phone)

    def clean_password2(self):
        password1 = self.cleaned_data.get('password')
        password2 = self.cleaned_data.get('password2')
        if len(password2) <= 8:
            raise forms.ValidationError('رمز عبور باید باید حداقل 8 رقم باشد.')
        if password1 != password2:
            raise forms.ValidationError('رمز عبور ها متفاوت هستند.')
        return password2

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return check_first_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return check_last_name(last_name)


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'national_code', 'email', 'date_of_birth', 'card_number')
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'phone': forms.TextInput(attrs={'class': 'form-control'}),
            'national_code': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(
                attrs={'type': 'date', 'placeholder': 'dd-mm-yyyy (DOB)', 'class': 'form-control'}
            ),
            'card_number': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        return check_phone(phone, self)

    def clean_national_code(self):
        national_code = self.cleaned_data.get('national_code')
        if len(national_code) != 10:
            raise forms.ValidationError('کد ملی باید 10 رقم باشد.')
        if not national_code.isdigit():
            raise forms.ValidationError('کد ملی باید فقط شامل اعداد باشد.')
        if User.objects.filter(national_code=national_code).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('کد ملی قبلا ثبت شده است.')
        return national_code

    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        return check_first_name(first_name)

    def clean_last_name(self):
        last_name = self.cleaned_data.get('last_name')
        return check_last_name(last_name)

    def clean_card_number(self):
        card_number = self.cleaned_data.get('card_number')
        if len(card_number) != 16:
            raise forms.ValidationError('شماره کارت باید 16 رقم باشد.')
        if not card_number.isdigit():
            raise forms.ValidationError('شماره کارت باید فقط شامل اعداد باشد.')
        return card_number


class PasswordChangeForm(forms.Form):
    old_password = forms.CharField(max_length=250, required=True,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='رمز عبور قبل')
    new_password = forms.CharField(max_length=250, required=True,
                                   widget=forms.PasswordInput(attrs={'class': 'form-control'}), label='رمز عبور جدید')
    new_password2 = forms.CharField(max_length=250, required=True,
                                    widget=forms.PasswordInput(attrs={'class': 'form-control'}),
                                    label='تایید رمز عبور جدید')

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password')
        password2 = self.cleaned_data.get('new_password2')
        if len(password2) <= 8:
            raise forms.ValidationError('رمز عبور باید باید حداقل 8 رقم باشد.')
        if password1 != password2:
            raise forms.ValidationError('رمز عبور ها متفاوت هستند.')
        return password2


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ('province', 'city', 'address', 'postal_code', 'receiver_name')
        widgets = {
            'province': forms.Select(attrs={'class': 'form-control'}),
            'city': forms.Select(attrs={'class': 'form-control'}),
            'address': forms.TextInput(attrs={'class': 'form-control'}),
            'postal_code': forms.TextInput(attrs={'class': 'form-control'}),
            'receiver_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_postal_code(self):
        if self.cleaned_data['postal_code'] == '':
            raise forms.ValidationError('postal code is required')
        if len(self.cleaned_data['postal_code']) != 10:
            raise forms.ValidationError('کد پستی باید 10 رقمی باشد.')
        return self.cleaned_data['postal_code']

    def clean_address(self):
        if self.cleaned_data['address'] == '':
            raise forms.ValidationError('address is required')
        return self.cleaned_data['address']
