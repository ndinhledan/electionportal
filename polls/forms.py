from django import forms
from django.core.validators import EmailValidator

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class SignupForm(UserCreationForm):
    email = forms.EmailField(max_length=200, help_text='Required')

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def clean_email(self):
        email_form = self.cleaned_data['email']
        print('here5')
        print(email_form)
        if not (email_form.endswith('e.ntu.edu.sg') or email_form.endswith('ntu.edu.sg')):
            print('here6')
            raise forms.ValidationError('Please enter NTU email!')
        try:
        	match = User.objects.get(email=email_form)
        except User.DoesNotExist:
        	return email_form
        raise forms.ValidationError('This email is already registered!')
    