from django import forms
from django.contrib.auth.forms import UserCreationForm
from accounts.models import User
from app.models import Intern, Trainer


class MyUserCreationForm(UserCreationForm):
    is_intern = forms.BooleanField(required=False, initial=False)
    is_trainer = forms.BooleanField(required=False, initial=False)
    
    class Meta(UserCreationForm.Meta):
        model = User

    def clean(self):
        cleaned_data = super(MyUserCreationForm, self).clean()
        is_intern = cleaned_data.get("is_intern")
        is_trainer = cleaned_data.get("is_trainer")
        if is_trainer and is_intern:
            self._errors['is_intern'] = self.error_class([ 
                'Enter only one of trainer or intern']) 
        elif not is_intern and not is_trainer:
            self._errors['is_trainer'] = self.error_class([ 
                'You must enter a trainer or a intern']) 
        return cleaned_data

    def save(self):
        user = super().save(commit=False)
        is_intern = self.cleaned_data.get("is_intern")
        is_trainer = self.cleaned_data.get("is_trainer")
        if is_intern:  
            user.is_intern = True
            user.save()
            intern = Intern.objects.create(user=user)
        if is_trainer:
            user.is_trainer = True
            user.save()
            teacher = Trainer.objects.create(user=user)
        return user
