from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from .models import UserProfile, Question, Choice
from django.forms import inlineformset_factory



class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['title', 'short_description', 'question_text', 'image', 'pub_date', 'end_date']



class ChoiceForm(forms.ModelForm):
    class Meta:
        model = Choice
        fields = ['choice_text']
ChoiceFormSet = inlineformset_factory(
            Question, Choice, form=ChoiceForm, extra=3, can_delete=True
)

class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()

        # Сохраняем профиль и аватар
        profile, created = UserProfile.objects.get_or_create(user=user)
        if 'avatar' in self.cleaned_data:
            avatar = self.cleaned_data['avatar']
            profile.avatar = avatar
            print(f"Avatar saved: {avatar}")
        profile.save()

        return user

class UserProfileForm(forms.ModelForm):
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(required=False, widget=forms.Textarea)

    class Meta:
        model = UserProfile  # Привяжите форму к модели UserProfile
        fields = ['avatar', 'bio']

class ProfileEditForm(UserChangeForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'email')

    avatar = forms.ImageField(required=False)
    bio = forms.CharField(widget=forms.Textarea, required=False)

    def save(self, commit=True):
        user = super().save(commit=False)

        if commit:
            user.save()

        user_profile = UserProfile.objects.get(user=user)
        if 'avatar' in self.cleaned_data:
            user_profile.avatar = self.cleaned_data['avatar']
        if 'bio' in self.cleaned_data:
            user_profile.bio = self.cleaned_data['bio']

        if commit:
            user_profile.save()

        return user