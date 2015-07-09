# -*- coding: utf-8 -*-
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class RegistrationForm(forms.Form):
    email = forms.EmailField(label='Email', required=True)
    full_name = forms.CharField(label='Full Name', required=True)
    password1 = forms.CharField(label='Password', required=True, widget=forms.PasswordInput)
    password2 = forms.CharField(
        label='Password confirmation', required=True, widget=forms.PasswordInput
    )

    def clean_email(self):
        cleaned_email = self.cleaned_data.get('email')

        existing_users = User.objects.filter(email=cleaned_email)
        if existing_users:
                raise forms.ValidationError(
                    'User with this email address already exists.'
                )

        return cleaned_email

    def clean_full_name(self):
        cleaned_full_name = self.cleaned_data.get('full_name')
        if len(cleaned_full_name.split()) <= 1:
            raise forms.ValidationError('Enter your name AND last name.')

        return cleaned_full_name

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match.")
        return password2

    def save(self):
        data = self.cleaned_data
        user = User(
            email=data['email'],
            first_name=data['full_name'].split()[0],
            last_name=' '.join(data['full_name'].split()[1:]),
            is_active=False,
        )

        user.set_password(data['password1'])
        user.save()

        return user
