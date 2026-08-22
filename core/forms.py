"""Server-side forms that validate all user-supplied TaskSwap input."""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, UserCreationForm
from django.utils import timezone

from .models import Application, Profile, Task, TaskMessage, User


class StyledFormMixin:
    """Apply the shared, accessible CSS class to every rendered field."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            existing = field.widget.attrs.get("class", "")
            field.widget.attrs["class"] = f"{existing} form-control".strip()


class SignupForm(StyledFormMixin, UserCreationForm):
    """Create a local account while preventing duplicate email addresses."""

    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2")
        widgets = {
            "name": forms.TextInput(attrs={"autocomplete": "name", "placeholder": "Your name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@example.com"}),
        }

    def clean_email(self):
        email = self.cleaned_data["email"].lower()
        if User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account already uses this email address.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data["email"]
        user.name = self.cleaned_data["name"].strip()
        if commit:
            user.save()
            Profile.objects.get_or_create(user=user)
        return user


class EmailAuthenticationForm(StyledFormMixin, AuthenticationForm):
    """Use the default session authentication flow with an email-labelled field."""

    username = forms.EmailField(
        label="Email address",
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@example.com"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"autocomplete": "current-password", "placeholder": "Password"})
    )


class PasswordResetRequestForm(StyledFormMixin, forms.Form):
    """Accept an email without exposing whether a matching account exists."""

    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"autocomplete": "email", "placeholder": "you@example.com"})
    )


class NewPasswordForm(StyledFormMixin, SetPasswordForm):
    """Use Django's strong password validation for an approved reset token."""


class TaskForm(StyledFormMixin, forms.ModelForm):
    """Validate a new task before it can be opened to local applicants."""

    class Meta:
        model = Task
        fields = ("title", "description", "category", "budget", "deadline")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "What needs doing?"}),
            "description": forms.Textarea(attrs={"rows": 7, "placeholder": "Explain what help you need."}),
            "budget": forms.NumberInput(attrs={"min": "0", "step": "0.01", "placeholder": "0.00"}),
            "deadline": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_deadline(self):
        deadline = self.cleaned_data["deadline"]
        if deadline < timezone.localdate():
            raise forms.ValidationError("Choose a deadline that is today or later.")
        return deadline


class ApplicationForm(StyledFormMixin, forms.ModelForm):
    """Capture a concise note from the person offering help."""

    class Meta:
        model = Application
        fields = ("message",)
        widgets = {
            "message": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Introduce yourself and explain how you can help."}
            )
        }


class TaskMessageForm(StyledFormMixin, forms.ModelForm):
    """Validate a private post-acceptance message without exposing sender or task fields."""

    class Meta:
        model = TaskMessage
        fields = ("body",)
        labels = {"body": "New message"}
        widgets = {
            "body": forms.Textarea(
                attrs={"rows": 5, "placeholder": "Share the address, arrival time, or a task update."}
            )
        }


class ProfileForm(StyledFormMixin, forms.ModelForm):
    """Expose only public profile fields; account ownership is enforced in the view."""

    class Meta:
        model = Profile
        fields = ("bio", "skills", "location")
        widgets = {
            "bio": forms.Textarea(attrs={"rows": 5, "placeholder": "A little about how you like to help."}),
            "skills": forms.TextInput(attrs={"placeholder": "e.g., carpentry, tutoring, design"}),
            "location": forms.TextInput(attrs={"placeholder": "Your neighbourhood or city"}),
        }
