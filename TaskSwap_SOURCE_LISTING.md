# TaskSwap — Complete Source Listing

This document contains the standalone Django project folder structure followed by the complete contents of every runnable source file.

## Folder structure

- `manage.py`
- `requirements.txt`
- `TASKSWAP_README.md`
- `tasksite/__init__.py`
- `tasksite/asgi.py`
- `tasksite/settings.py`
- `tasksite/urls.py`
- `tasksite/wsgi.py`
- `core/__init__.py`
- `core/admin.py`
- `core/apps.py`
- `core/forms.py`
- `core/migrations/0001_initial.py`
- `core/migrations/__init__.py`
- `core/models.py`
- `core/static/core/css/styles.css`
- `core/static/core/js/app.js`
- `core/templates/core/admin_base.html`
- `core/templates/core/admin_dashboard.html`
- `core/templates/core/admin_tasks.html`
- `core/templates/core/admin_users.html`
- `core/templates/core/base.html`
- `core/templates/core/dashboard.html`
- `core/templates/core/home.html`
- `core/templates/core/login.html`
- `core/templates/core/partials/form_fields.html`
- `core/templates/core/password_forgot.html`
- `core/templates/core/password_reset_confirm.html`
- `core/templates/core/password_reset_invalid.html`
- `core/templates/core/profile.html`
- `core/templates/core/profile_edit.html`
- `core/templates/core/public_profile.html`
- `core/templates/core/signup.html`
- `core/templates/core/task_detail.html`
- `core/templates/core/task_form.html`
- `core/tests.py`
- `core/urls.py`
- `core/views.py`

---

## `manage.py`

```python
#!/usr/bin/env python
"""Django's command-line utility for TaskSwap."""
import os
import sys


def main():
    """Run administrative commands against the local TaskSwap project."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasksite.settings")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError("Django is required. Install dependencies from requirements.txt.") from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()

```

## `requirements.txt`

```text
Django>=5.1,<5.2

```

## `TASKSWAP_README.md`

```text
# TaskSwap Django Application

TaskSwap is a local skill-exchange platform implemented with **Django 5.1**, Django’s built-in session authentication and admin, SQLite, server-rendered templates, plain CSS, and lightweight vanilla JavaScript.

## Run locally

From the project root, install the single dependency, apply the included initial migration, and start Django’s development server:

```bash
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

The public application is then available at `http://127.0.0.1:8000/`. The password-reset flow prints reset URLs to the same terminal that runs `runserver`, intentionally avoiding email configuration for local development.

## Create a moderation administrator

Run the following command and supply a name, email, and password when prompted:

```bash
python manage.py createsuperuser
```

The custom superuser setup sets both Django’s `is_superuser` flag and TaskSwap’s `is_admin` flag. This permits access to the protected TaskSwap moderation area at `/admin/` and the standard Django admin at `/django-admin/`.

## Verification

The project includes six end-to-end Django integration tests. Execute them with:

```bash
python manage.py test core -v 2
```

All required source files, including the generated initial database migration, are listed in `TaskSwap_SOURCE_LISTING.md` in the delivery archive.

```

## `tasksite/__init__.py`

```python
"""TaskSwap project package."""

```

## `tasksite/asgi.py`

```python
"""ASGI config for TaskSwap."""
import os

from django.core.asgi import get_asgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasksite.settings")

application = get_asgi_application()

```

## `tasksite/settings.py`

```python
"""Development settings for the TaskSwap SQLite application."""
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# Replace this key with a private value before any public deployment.
SECRET_KEY = "django-insecure-change-this-taskswap-development-key"
DEBUG = True
# Accept local development and the sandbox preview subdomains used for browser checks.
ALLOWED_HOSTS = ["localhost", "127.0.0.1", ".manus.computer"]

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "core",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "tasksite.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "core" / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "tasksite.wsgi.application"
ASGI_APPLICATION = "tasksite.asgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATIC_ROOT = BASE_DIR / "staticfiles"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# This project deliberately uses a custom email-address login model from its first migration.
AUTH_USER_MODEL = "core.User"
LOGIN_URL = "login"
LOGIN_REDIRECT_URL = "dashboard"
LOGOUT_REDIRECT_URL = "home"

```

## `tasksite/urls.py`

```python
"""Top-level URL configuration for TaskSwap."""
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Built-in Django administration remains available for superusers.
    path("django-admin/", admin.site.urls),
    # The product's separately protected moderation dashboard lives under /admin/.
    path("", include("core.urls")),
]

```

## `tasksite/wsgi.py`

```python
"""WSGI config for TaskSwap."""
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasksite.settings")

application = get_wsgi_application()

```

## `core/__init__.py`

```python
"""TaskSwap core application package."""

```

## `core/admin.py`

```python
"""Django's built-in administration views for the TaskSwap data model."""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import Application, PasswordResetToken, Profile, Task, User


@admin.register(User)
class TaskSwapUserAdmin(UserAdmin):
    """Make the custom email user model manageable through Django admin."""

    ordering = ("email",)
    list_display = ("email", "name", "is_admin", "is_active", "created_at")
    list_filter = ("is_admin", "is_active", "is_staff")
    search_fields = ("email", "name")
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal information", {"fields": ("name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser", "is_admin", "groups", "user_permissions")}),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("email", "name", "password1", "password2", "is_admin", "is_staff", "is_superuser"),
        }),
    )


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    """Filter and review tasks in Django's standard administration interface."""

    list_display = ("title", "category", "budget", "deadline", "status", "posted_by", "created_at")
    list_filter = ("status", "category")
    search_fields = ("title", "description", "posted_by__email", "posted_by__name")


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("task", "applicant", "status", "created_at")
    list_filter = ("status",)
    search_fields = ("task__title", "applicant__email", "applicant__name")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "location", "skills")
    search_fields = ("user__email", "user__name", "location")


@admin.register(PasswordResetToken)
class PasswordResetTokenAdmin(admin.ModelAdmin):
    list_display = ("user", "expires_at", "used")
    search_fields = ("user__email",)
    list_filter = ("used",)

```

## `core/apps.py`

```python
from django.apps import AppConfig


class CoreConfig(AppConfig):
    """Register the core application and its model signals."""

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"

```

## `core/forms.py`

```python
"""Server-side forms that validate all user-supplied TaskSwap input."""
from django import forms
from django.contrib.auth.forms import AuthenticationForm, SetPasswordForm, UserCreationForm
from django.utils import timezone

from .models import Application, Profile, Task, User


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

```

## `core/migrations/0001_initial.py`

```python
# Generated by Django 5.1.15 on 2026-08-22 04:37

import core.models
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('name', models.CharField(max_length=150)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('is_admin', models.BooleanField(default=False)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'ordering': ['-created_at'],
            },
            managers=[
                ('objects', core.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bio', models.TextField(blank=True, max_length=500)),
                ('skills', models.CharField(blank=True, max_length=300)),
                ('location', models.CharField(blank=True, max_length=120)),
                ('avatar_url', models.URLField(blank=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=150)),
                ('description', models.TextField(max_length=2500)),
                ('category', models.CharField(choices=[('home', 'Home & garden'), ('tech', 'Technology'), ('learning', 'Learning'), ('creative', 'Creative'), ('events', 'Events'), ('other', 'Other')], max_length=20)),
                ('budget', models.DecimalField(decimal_places=2, max_digits=9)),
                ('deadline', models.DateField()),
                ('status', models.CharField(choices=[('open', 'Open'), ('in_progress', 'In progress'), ('completed', 'Completed'), ('cancelled', 'Cancelled'), ('removed', 'Removed')], default='open', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('posted_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tasks', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='Application',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.TextField(max_length=1000)),
                ('status', models.CharField(choices=[('pending', 'Pending'), ('accepted', 'Accepted'), ('rejected', 'Rejected')], default='pending', max_length=20)),
                ('created_at', models.DateTimeField(default=django.utils.timezone.now, editable=False)),
                ('applicant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to=settings.AUTH_USER_MODEL)),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='applications', to='core.task')),
            ],
            options={
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='PasswordResetToken',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('token', models.CharField(max_length=255, unique=True)),
                ('expires_at', models.DateTimeField()),
                ('used', models.BooleanField(default=False)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='reset_tokens', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'indexes': [models.Index(fields=['token', 'used', 'expires_at'], name='core_passwo_token_81159d_idx')],
            },
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['status', 'category'], name='core_task_status_ec6042_idx'),
        ),
        migrations.AddIndex(
            model_name='task',
            index=models.Index(fields=['deadline'], name='core_task_deadlin_aa9504_idx'),
        ),
        migrations.AddConstraint(
            model_name='application',
            constraint=models.UniqueConstraint(fields=('task', 'applicant'), name='one_application_per_user_task'),
        ),
    ]

```

## `core/migrations/__init__.py`

```python

```

## `core/models.py`

```python
"""Database entities for user accounts, tasks, applications, and profiles."""
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    """Create users with email as the login identifier instead of a username."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("An email address is required.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        # set_password hashes the value into Django's built-in password column.
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)
        extra_fields.setdefault("is_admin", True)
        if extra_fields.get("is_staff") is not True or extra_fields.get("is_superuser") is not True:
            raise ValueError("A superuser must have is_staff=True and is_superuser=True.")
        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Email-authenticated user; Django's `password` field stores the password hash."""

    username = None
    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    objects = UserManager()

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name or self.email


class Profile(models.Model):
    """Public, optional profile fields kept separate from private account data."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    bio = models.TextField(blank=True, max_length=500)
    skills = models.CharField(blank=True, max_length=300)
    location = models.CharField(blank=True, max_length=120)
    avatar_url = models.URLField(blank=True)

    def __str__(self):
        return f"Profile for {self.user}"


class Task(models.Model):
    """A locally posted task with a controlled lifecycle."""

    class Category(models.TextChoices):
        HOME = "home", "Home & garden"
        TECH = "tech", "Technology"
        LEARNING = "learning", "Learning"
        CREATIVE = "creative", "Creative"
        EVENTS = "events", "Events"
        OTHER = "other", "Other"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        REMOVED = "removed", "Removed"

    title = models.CharField(max_length=150)
    description = models.TextField(max_length=2500)
    category = models.CharField(max_length=20, choices=Category.choices)
    budget = models.DecimalField(max_digits=9, decimal_places=2)
    deadline = models.DateField()
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["status", "category"]),
            models.Index(fields=["deadline"]),
        ]

    def __str__(self):
        return self.title


class Application(models.Model):
    """A single applicant's offer to help with a particular task."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="applications")
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    message = models.TextField(max_length=1000)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=["task", "applicant"], name="one_application_per_user_task")
        ]

    def __str__(self):
        return f"{self.applicant} → {self.task}"


class PasswordResetToken(models.Model):
    """A random, single-use, time-limited password-reset credential."""

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reset_tokens")
    token = models.CharField(max_length=255, unique=True)
    expires_at = models.DateTimeField()
    used = models.BooleanField(default=False)

    class Meta:
        indexes = [models.Index(fields=["token", "used", "expires_at"])]

    def is_valid(self):
        """Return true only while the credential remains unused and unexpired."""
        return not self.used and self.expires_at > timezone.now()

```

## `core/static/core/css/styles.css`

```css
/* Quiet Utility design reminder: Apple-inspired porcelain/ink/TaskSwap Blue; typography, whitespace, and precise pills over decoration. */
:root { --paper:#fbfbfd; --ink:#1d1d1f; --muted:#6e6e73; --line:#d2d2d7; --soft:#f5f5f7; --blue:#0071e3; --blue-dark:#0066cc; --error:#b42318; --success:#157a3a; --display:-apple-system,BlinkMacSystemFont,"SF Pro Display","Helvetica Neue",Arial,sans-serif; --ease:cubic-bezier(.22,1,.36,1); --shadow:0 18px 45px rgba(0,0,0,.05); }
*{box-sizing:border-box}html{scroll-behavior:smooth}body{margin:0;background:var(--paper);color:var(--ink);font-family:var(--display);-webkit-font-smoothing:antialiased}a{color:inherit;text-decoration-thickness:1px;text-underline-offset:.18em}a:hover{color:var(--blue)}button,input,select,textarea{font:inherit}button{cursor:pointer}h1,h2,h3,p{margin-top:0}h1,h2,h3{letter-spacing:-.045em}.sr-only{position:absolute;width:1px;height:1px;overflow:hidden;clip:rect(0,0,0,0);white-space:nowrap}.skip-link{position:fixed;z-index:100;top:-4rem;left:1rem;padding:.75rem 1rem;color:#fff;background:var(--ink);border-radius:999px;transition:top 160ms var(--ease)}.skip-link:focus{top:1rem}
.site-header{position:sticky;top:0;z-index:20;background:rgba(251,251,253,.9);border-bottom:1px solid transparent;backdrop-filter:saturate(180%) blur(18px);transition:border-color 180ms var(--ease)}.site-header.is-scrolled{border-color:var(--line)}.nav-shell{display:flex;align-items:center;justify-content:space-between;min-height:52px;max-width:1240px;margin:0 auto;padding:0 28px}.brand{display:inline-flex;align-items:center;gap:9px;color:var(--ink);text-decoration:none;font-size:.95rem;font-weight:700;letter-spacing:-.035em}.brand:hover{color:var(--ink)}.brand-mark{display:inline-grid;width:28px;height:28px;place-items:center;border-radius:8px;background:var(--ink);color:#fff;font-size:.63rem;letter-spacing:-.08em}.brand-wordmark{line-height:1}.primary-nav{display:flex;align-items:center;gap:21px;font-size:.78rem;font-weight:500}.primary-nav a,.nav-link-button{text-decoration:none;color:var(--ink)}.primary-nav a:hover,.nav-link-button:hover{color:var(--blue)}.nav-cta{color:#fff!important;background:var(--blue);padding:7px 12px;border-radius:999px}.nav-cta:hover{background:var(--blue-dark);color:#fff!important}.nav-account{max-width:9rem;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.inline-form{margin:0}.nav-link-button{padding:0;border:0;background:transparent;font-size:inherit}.menu-toggle{display:none;border:0;background:transparent;padding:8px 0 8px 10px}.menu-toggle span:not(.sr-only){display:block;width:18px;height:1px;margin:4px 0;background:var(--ink)}
.message-stack{position:fixed;z-index:40;right:18px;top:68px;width:min(390px,calc(100vw - 36px))}.message{padding:14px 18px;margin-bottom:10px;background:var(--ink);color:#fff;border-radius:14px;font-size:.9rem;box-shadow:var(--shadow)}.message--error{background:var(--error)}.message--success{background:var(--success)}.eyebrow{margin-bottom:15px;color:var(--muted);font-size:.72rem;font-weight:700;letter-spacing:.11em;text-transform:uppercase}
.hero{position:relative;display:grid;min-height:calc(100svh - 52px);place-items:center;padding:9rem 28px 7rem;text-align:center}.hero-copy{max-width:1000px}.hero h1{margin-bottom:16px;font-size:clamp(4.4rem,13vw,9.4rem);font-weight:800;line-height:.91}.hero-subtitle{max-width:450px;margin:0 auto 31px;color:var(--muted);font-size:clamp(1.1rem,2vw,1.35rem);line-height:1.4;letter-spacing:-.025em}.hero-actions{display:flex;justify-content:center}.scroll-cue{position:absolute;bottom:28px;color:var(--muted);font-size:.78rem;text-decoration:none}.scroll-cue span{margin-left:4px;color:var(--blue)}.button{display:inline-flex;align-items:center;justify-content:center;min-height:44px;padding:11px 19px;border:1px solid var(--ink);border-radius:999px;color:var(--ink);background:transparent;font-size:.92rem;font-weight:600;letter-spacing:-.02em;text-decoration:none;transition:background 160ms var(--ease),color 160ms var(--ease),transform 160ms var(--ease),border-color 160ms var(--ease)}.button:hover{color:#fff;background:var(--ink)}.button:active{transform:scale(.97)}.button--ink{color:#fff;background:var(--ink)}.button--ink:hover{color:#fff;background:#3a3a3c}.button--outline{border-color:var(--line)}.button--outline:hover{border-color:var(--ink)}.button--full{width:100%}
.statement-stage{display:grid;min-height:100svh;place-items:center;padding:96px 28px;text-align:center}.statement-copy{max-width:920px}.stage-number{margin-bottom:22px;font-size:.78rem;font-weight:600;letter-spacing:.12em}.statement-stage h2{margin:0 0 19px;font-size:clamp(4.7rem,16vw,12rem);font-weight:800;line-height:.88}.statement-stage p:not(.stage-number){max-width:410px;margin:0 auto;font-size:clamp(1.05rem,2vw,1.35rem);line-height:1.43;letter-spacing:-.02em}.stage--light{background:#fff}.stage--light .stage-number{color:var(--blue)}.stage--ink{color:var(--paper);background:var(--ink)}.stage--ink .stage-number{color:#a1a1a6}.stage--ink p:not(.stage-number){color:#d2d2d7}.stage--blue{color:#fff;background:var(--blue)}.stage--blue .stage-number,.stage--blue p:not(.stage-number){color:#fff}
.task-shelf,.applicant-section,.dashboard-section{max-width:1240px;margin:0 auto;padding:128px 28px}.shelf-heading{display:flex;align-items:flex-end;justify-content:space-between;gap:24px;margin-bottom:36px}.shelf-heading h2,.page-heading h1,.page-hero h1,.auth-intro h1,.profile-hero h1{margin-bottom:0;font-size:clamp(2.85rem,6vw,5.2rem);font-weight:750;line-height:.96}.text-link{color:var(--blue);font-size:.92rem;font-weight:600;text-decoration:none;white-space:nowrap}.text-link:hover{color:var(--blue-dark)}.task-filters{display:grid;grid-template-columns:minmax(220px,1fr) 185px 160px auto;gap:10px;margin-bottom:32px}.task-filters input,.task-filters select,.form-control,.admin-search input{width:100%;min-height:46px;padding:0 14px;border:1px solid var(--line);border-radius:12px;outline:none;color:var(--ink);background:#fff;transition:border-color 160ms var(--ease),box-shadow 160ms var(--ease)}.task-filters input:focus,.task-filters select:focus,.form-control:focus,.admin-search input:focus{border-color:var(--blue);box-shadow:0 0 0 4px rgba(0,113,227,.12)}.task-list,.applicant-list,.table-list{border-top:1px solid var(--line)}.task-row{display:grid;grid-template-columns:1fr auto;gap:35px;padding:32px 0;border-bottom:1px solid var(--line)}.task-row h3{margin-bottom:10px;font-size:clamp(1.55rem,3vw,2.4rem);line-height:1}.task-row h3 a,.applicant-row h3 a{ text-decoration:none}.task-row h3 a:hover,.applicant-row h3 a:hover{color:var(--blue)}.task-row p{margin-bottom:0;color:var(--muted);line-height:1.5}.task-row__meta{margin-bottom:11px!important;font-size:.78rem}.task-row__meta a{color:inherit}.task-row__side{display:flex;min-width:135px;flex-direction:column;align-items:flex-end;gap:7px;padding-top:4px}.task-row__side strong{font-size:1.1rem}.task-row__side span{color:var(--muted);font-size:.82rem}.task-row__side .text-link{margin-top:11px}.empty-state{padding:66px 24px;text-align:center}.empty-state h3{margin-bottom:13px;font-size:clamp(1.7rem,3vw,2.55rem)}.empty-state p{margin-bottom:22px;color:var(--muted)}.empty-state--compact{padding:44px 15px}.empty-state--compact h3{font-size:1.7rem}
.auth-layout{display:grid;grid-template-columns:minmax(0,1fr) minmax(360px,480px);gap:clamp(48px,10vw,160px);max-width:1120px;min-height:calc(100svh - 52px);align-items:center;margin:0 auto;padding:96px 28px}.auth-intro{align-self:center}.auth-intro h1{margin-bottom:18px}.auth-intro>p:not(.eyebrow),.page-heading>p:not(.eyebrow),.page-hero>p:not(.eyebrow){max-width:400px;color:var(--muted);font-size:1.08rem;line-height:1.5}.form-card{padding:34px;background:#fff;border:1px solid var(--line);border-radius:20px;box-shadow:var(--shadow)}.form-card h2{margin-bottom:28px;font-size:2rem}.form-field{margin-bottom:18px}.form-field label{display:block;margin-bottom:8px;font-size:.88rem;font-weight:600}.form-field textarea.form-control{min-height:120px;padding:12px 14px;resize:vertical}.help-text{display:block;margin-top:7px;color:var(--muted);font-size:.77rem;line-height:1.35}.field-error,.form-error{margin:7px 0 0;color:var(--error);font-size:.78rem;line-height:1.35}.form-error ul{padding-left:1.1rem;margin:0}.form-footnote{margin:18px 0 0;color:var(--muted);font-size:.86rem;text-align:center}.form-footnote a{color:var(--blue)}.narrow-page{max-width:750px;margin:0 auto;padding:116px 28px}.page-heading{margin-bottom:39px}.page-heading h1{margin-bottom:18px}.page-heading--center{text-align:center}.page-heading--center>p{margin-right:auto;margin-left:auto}.form-card--wide{max-width:610px;padding:38px;box-shadow:none}.narrow-page .form-card{background:transparent}
.detail-hero{display:grid;grid-template-columns:minmax(0,1fr) 245px;gap:56px;max-width:1240px;margin:0 auto;padding:90px 28px 70px;border-bottom:1px solid var(--line)}.back-link{display:inline-block;margin-bottom:47px;color:var(--muted);font-size:.86rem;text-decoration:none}.detail-hero h1{margin-bottom:19px;font-size:clamp(3.6rem,8vw,7.8rem);font-weight:800;line-height:.91}.detail-owner{margin-bottom:0;color:var(--muted)}.detail-owner a{color:inherit}.detail-aside{display:flex;flex-direction:column;align-items:flex-start;justify-content:flex-end;gap:12px}.detail-budget{font-size:2.6rem;letter-spacing:-.06em}.detail-aside>span{color:var(--muted);font-size:.9rem}.status{display:inline-flex;align-items:center;width:fit-content;min-height:25px;padding:4px 9px;border-radius:999px;background:var(--soft);color:var(--muted);font-size:.72rem;font-weight:650;letter-spacing:.02em}.status--open,.status--accepted{color:#005bbd;background:#e8f3ff}.status--in_progress{color:#7d4c00;background:#fff4e0}.status--completed{color:#0a6a30;background:#e7f7ec}.status--rejected,.status--cancelled,.status--removed{color:#8d1b13;background:#ffecea}.detail-layout{display:grid;grid-template-columns:minmax(0,1fr) 370px;gap:clamp(50px,10vw,150px);max-width:1240px;margin:0 auto;padding:75px 28px 100px}.task-description{max-width:695px}.task-description h2,.action-panel h2,.profile-copy h2{margin-bottom:20px;font-size:2.25rem}.task-description p{font-size:clamp(1.07rem,1.7vw,1.3rem);line-height:1.65}.action-panel{align-self:start;padding:31px;background:#fff;border:1px solid var(--line);border-radius:18px}.action-panel .quiet-copy{color:var(--muted);line-height:1.5}.applicant-section{border-top:1px solid var(--line)}.count-label{color:var(--muted);font-size:.84rem}.applicant-row{display:flex;align-items:flex-start;justify-content:space-between;gap:38px;padding:29px 0;border-bottom:1px solid var(--line)}.applicant-row h3{margin-bottom:9px;font-size:1.55rem}.applicant-row p{max-width:700px;margin-bottom:0;line-height:1.5}.applicant-row__actions{display:flex;flex-direction:column;align-items:flex-end;gap:15px;min-width:100px}
.page-hero{max-width:1000px;margin:0 auto;padding:118px 28px 85px;text-align:center}.page-hero>p:not(.eyebrow){margin-right:auto;margin-left:auto}.page-hero .button{margin-top:13px}.dashboard-section{padding-top:70px;padding-bottom:70px}.dashboard-section--tint{max-width:none;padding-right:max(28px,calc((100vw - 1184px)/2));padding-left:max(28px,calc((100vw - 1184px)/2));background:#fff}.table-row{display:grid;grid-template-columns:minmax(230px,1.8fr) minmax(120px,1fr) minmax(100px,.7fr) minmax(130px,1fr) 20px;align-items:center;gap:20px;min-height:76px;padding:14px 0;border-bottom:1px solid var(--line);color:var(--muted);font-size:.85rem;text-decoration:none;transition:color 160ms var(--ease)}.table-row:hover{color:var(--ink)}.table-row__title{color:var(--ink);font-size:1.04rem;font-weight:650;letter-spacing:-.025em}.profile-hero{display:grid;grid-template-columns:100px 1fr auto;align-items:center;gap:26px;max-width:1240px;margin:0 auto;padding:112px 28px 69px}.profile-monogram{display:grid;width:100px;height:100px;place-items:center;border-radius:50%;color:#fff;background:var(--ink);font-size:3rem;font-weight:700}.profile-location{margin-bottom:0;color:var(--muted)}.profile-grid{display:grid;grid-template-columns:minmax(220px,2fr) minmax(220px,2fr) 1fr 1fr;max-width:1240px;margin:0 auto;border-top:1px solid var(--line)}.profile-copy,.stat-block{min-height:220px;padding:37px 28px;border-right:1px solid var(--line)}.profile-copy:last-of-type,.stat-block:last-child{border-right:0}.profile-copy p{margin-bottom:0;color:var(--muted);line-height:1.55}.stat-block{display:flex;flex-direction:column;justify-content:space-between}.stat-block strong{font-size:clamp(3.3rem,7vw,6.5rem);letter-spacing:-.08em;line-height:.9}.stat-block span{color:var(--muted);font-size:.84rem}
.admin-wrap{display:grid;grid-template-columns:280px minmax(0,1fr);min-height:calc(100svh - 52px)}.admin-nav{padding:52px 30px;color:var(--paper);background:var(--ink)}.admin-nav .eyebrow{color:#a1a1a6}.admin-nav h1{margin-bottom:46px;font-size:2.4rem}.admin-nav nav{display:grid;gap:8px}.admin-nav nav a{padding:9px 0;color:#d2d2d7;font-size:.92rem;text-decoration:none}.admin-nav nav a:hover{color:#fff}.admin-content{padding:76px clamp(28px,6vw,92px)}.admin-content h2{margin-bottom:13px;font-size:clamp(2.8rem,5vw,5rem);line-height:.94}.admin-intro{margin-bottom:45px;color:var(--muted)}.metric-grid{display:grid;grid-template-columns:repeat(3,1fr);margin:47px 0 78px;border-top:1px solid var(--line);border-left:1px solid var(--line)}.metric{display:flex;min-height:180px;flex-direction:column;justify-content:space-between;padding:26px;border-right:1px solid var(--line);border-bottom:1px solid var(--line)}.metric strong{font-size:clamp(2.7rem,5vw,5rem);letter-spacing:-.075em;line-height:.95}.metric span{color:var(--muted);font-size:.82rem}.status-breakdown h3{margin-bottom:18px;font-size:1.5rem}.status-breakdown .table-row{grid-template-columns:1fr auto}.admin-search{display:flex;max-width:540px;gap:10px;margin:37px 0}.admin-search .button{min-height:46px}.table-row--admin{grid-template-columns:minmax(190px,1.7fr) 110px 130px 90px}.table-row--admin>div:first-child{display:grid;gap:4px}.table-row--admin>div:first-child span{font-size:.78rem}.text-action{padding:0;border:0;color:var(--blue);background:transparent;font-size:.82rem;font-weight:600}.text-action:hover{color:var(--blue-dark);text-decoration:underline}.site-footer{border-top:1px solid var(--line)}.footer-shell{display:flex;max-width:1240px;justify-content:space-between;gap:22px;margin:0 auto;padding:25px 28px;color:var(--muted);font-size:.76rem}.footer-shell p{margin-bottom:0}.footer-shell strong{color:var(--ink)}
html.is-motion-ready .reveal{opacity:0;transform:translateY(22px);transition:opacity 720ms var(--ease),transform 720ms var(--ease)}html.is-motion-ready .reveal.is-visible{opacity:1;transform:translateY(0)}@media(prefers-reduced-motion:reduce){*,*::before,*::after{scroll-behavior:auto!important;transition-duration:.01ms!important;animation-duration:.01ms!important}html.is-motion-ready .reveal{opacity:1;transform:none}}
@media(max-width:860px){.primary-nav{position:absolute;top:52px;right:0;left:0;display:none;flex-direction:column;align-items:stretch;gap:0;padding:12px 28px 22px;background:rgba(251,251,253,.98);border-bottom:1px solid var(--line)}.primary-nav.is-open{display:flex}.primary-nav a,.nav-link-button{padding:11px 0}.nav-cta{padding:10px 13px!important;margin-top:7px;text-align:center}.menu-toggle{display:block}.auth-layout,.detail-layout{grid-template-columns:1fr}.auth-layout{gap:36px}.detail-layout{gap:44px}.detail-hero{grid-template-columns:1fr;gap:35px}.detail-aside{flex-direction:row;align-items:center;justify-content:flex-start;flex-wrap:wrap}.profile-grid{grid-template-columns:1fr 1fr}.profile-copy:nth-child(2){border-right:0}.stat-block:nth-child(3),.stat-block:last-child{border-top:1px solid var(--line)}.admin-wrap{grid-template-columns:1fr}.admin-nav{padding:30px 28px}.admin-nav h1{margin-bottom:21px}.admin-nav nav{display:flex;gap:22px}.metric-grid{grid-template-columns:1fr}.metric{min-height:140px}.table-row--admin{grid-template-columns:minmax(160px,1fr) 90px 82px}.table-row--admin>div:last-child{grid-column:1/-1}.table-row--admin>span:nth-of-type(2){display:none}}
@media(max-width:620px){.nav-shell{padding:0 18px}.hero{padding-right:20px;padding-left:20px}.statement-stage,.task-shelf,.applicant-section,.dashboard-section{padding-right:20px;padding-left:20px}.task-filters{grid-template-columns:1fr 1fr}.task-filters .search-field{grid-column:1/-1}.task-filters .button{grid-column:1/-1}.task-row{grid-template-columns:1fr;gap:20px}.task-row__side{align-items:flex-start}.task-row__side .text-link{margin-top:3px}.shelf-heading{align-items:flex-start;flex-direction:column}.auth-layout,.narrow-page,.detail-hero,.detail-layout,.page-hero,.profile-hero{padding-right:20px;padding-left:20px}.form-card,.form-card--wide{padding:25px 20px}.applicant-row{flex-direction:column;gap:18px}.applicant-row__actions{align-items:flex-start}.table-row{grid-template-columns:minmax(0,1fr) auto;gap:8px 16px;padding:18px 0}.table-row>span:not(.table-row__title):not(.status),.table-row>:nth-child(4){display:none}.table-row>:last-child{grid-column:2;grid-row:1}.profile-hero{grid-template-columns:72px 1fr;gap:17px;padding-top:75px}.profile-hero .button{grid-column:1/-1;justify-self:start}.profile-monogram{width:72px;height:72px;font-size:2rem}.profile-grid{grid-template-columns:1fr}.profile-copy,.stat-block{min-height:160px;border-right:0;border-bottom:1px solid var(--line)}.stat-block{border-top:0!important}.footer-shell{flex-direction:column;padding:24px 20px}.admin-content{padding:54px 20px}.admin-search{flex-direction:column}.table-row--admin{grid-template-columns:minmax(0,1fr) auto}.table-row--admin>span:nth-of-type(1){grid-column:2;grid-row:1}.table-row--admin>div:last-child{grid-column:1/-1}.admin-nav nav{gap:17px}}

```

## `core/static/core/js/app.js`

```javascript
/* Quiet Utility reminder: motion is brief, respectful, and only clarifies a typography-first interface. */
(function () {
    "use strict";
    document.documentElement.classList.add("is-motion-ready");
    const revealItems = document.querySelectorAll(".reveal");
    if ("IntersectionObserver" in window) {
        const observer = new IntersectionObserver((entries) => {
            entries.forEach((entry) => { if (entry.isIntersecting) { entry.target.classList.add("is-visible"); observer.unobserve(entry.target); } });
        }, { threshold: 0.12 });
        revealItems.forEach((item) => observer.observe(item));
    } else { revealItems.forEach((item) => item.classList.add("is-visible")); }
    const menuToggle = document.querySelector("[data-menu-toggle]");
    const navigation = document.querySelector("[data-primary-nav]");
    if (menuToggle && navigation) { menuToggle.addEventListener("click", () => { const isOpen = navigation.classList.toggle("is-open"); menuToggle.setAttribute("aria-expanded", String(isOpen)); }); }
    const header = document.querySelector("[data-header]");
    const updateHeader = () => { if (header) header.classList.toggle("is-scrolled", window.scrollY > 8); };
    updateHeader(); window.addEventListener("scroll", updateHeader, { passive: true });
}());

```

## `core/templates/core/admin_base.html`

```html
{# Quiet Utility reminder: restrained workbench for protected moderation, with explicit route-level status. #}
{% extends "core/base.html" %}{% block content %}<section class="admin-wrap reveal"><aside class="admin-nav"><p class="eyebrow">Protected moderation</p><h1>TaskSwap admin.</h1><nav aria-label="Administration navigation"><a href="{% url 'admin_dashboard' %}">Overview</a><a href="{% url 'admin_users' %}">Users</a><a href="{% url 'admin_tasks' %}">Tasks</a></nav></aside><div class="admin-content">{% block admin_content %}{% endblock %}</div></section>{% endblock %}

```

## `core/templates/core/admin_dashboard.html`

```html
{# Quiet Utility reminder: moderation analytics are exact counts, not synthetic product metrics. #}
{% extends "core/admin_base.html" %}{% block title %}Admin overview · TaskSwap{% endblock %}{% block admin_content %}<p class="eyebrow">Overview</p><h2>Keep the exchange clear.</h2><p class="admin-intro">A compact view of the platform's real moderation data.</p><div class="metric-grid"><article class="metric"><strong>{{ total_users }}</strong><span>Total users</span></article><article class="metric"><strong>{{ tasks_this_week }}</strong><span>Tasks posted this week</span></article><article class="metric"><strong>{{ completion_rate|floatformat:1 }}%</strong><span>Completion rate</span></article></div><section class="status-breakdown"><h3>Tasks by status</h3><div class="table-list">{% for row in status_counts %}<div class="table-row"><span class="table-row__title">{{ row.status|title }}</span><span>{{ row.total }} task{{ row.total|pluralize }}</span></div>{% empty %}<p class="quiet-copy">No tasks have been created yet.</p>{% endfor %}</div></section>{% endblock %}

```

## `core/templates/core/admin_tasks.html`

```html
{# Quiet Utility reminder: moderation lists all states while removal preserves the underlying record. #}
{% extends "core/admin_base.html" %}{% block title %}Task moderation · TaskSwap{% endblock %}{% block admin_content %}<p class="eyebrow">Tasks</p><h2>Task moderation.</h2><p class="admin-intro">Every task is visible here, regardless of public status.</p><div class="table-list admin-table">{% for task in tasks %}<article class="table-row table-row--admin"><div><strong class="table-row__title">{{ task.title }}</strong><span>By {{ task.posted_by.name }} · {{ task.get_category_display }}</span></div><span class="status status--{{ task.status }}">{{ task.get_status_display }}</span><span>{{ task.created_at|date:"M j, Y" }}</span><div>{% if task.status != 'removed' %}<form method="post" action="{% url 'admin_remove_task' task.id %}">{% csrf_token %}<button class="text-action" type="submit">Remove</button></form>{% endif %}</div></article>{% empty %}<div class="empty-state empty-state--compact"><h3>No tasks created yet.</h3></div>{% endfor %}</div>{% endblock %}

```

## `core/templates/core/admin_users.html`

```html
{# Quiet Utility reminder: user moderation is explicit, server-validated, and never destructive by default. #}
{% extends "core/admin_base.html" %}{% block title %}User moderation · TaskSwap{% endblock %}{% block admin_content %}<p class="eyebrow">Users</p><h2>Account management.</h2><form method="get" class="admin-search"><label class="sr-only" for="admin-q">Search users</label><input id="admin-q" name="q" type="search" value="{{ query }}" placeholder="Search by name or email"><button class="button button--outline" type="submit">Search</button></form><div class="table-list admin-table">{% for account in users %}<article class="table-row table-row--admin"><div><strong class="table-row__title">{{ account.name }}</strong><span>{{ account.email }}</span></div><span>{% if account.is_active %}Active{% else %}Inactive{% endif %}</span><span>{{ account.created_at|date:"M j, Y" }}</span><div>{% if account.is_active and account.id != user.id %}<form method="post" action="{% url 'admin_deactivate_user' account.id %}">{% csrf_token %}<button class="text-action" type="submit">Deactivate</button></form>{% endif %}</div></article>{% empty %}<div class="empty-state empty-state--compact"><h3>No matching users.</h3></div>{% endfor %}</div>{% endblock %}

```

## `core/templates/core/base.html`

```html
{# Quiet Utility reminder: porcelain/ink/TaskSwap Blue, oversized system type, and deliberate empty space. #}
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <meta name="description" content="TaskSwap is a local place to post a small task and find practical help.">
    <title>{% block title %}TaskSwap{% endblock %}</title>
    {% load static %}
    <link rel="stylesheet" href="{% static 'core/css/styles.css' %}">
</head>
<body>
    <a class="skip-link" href="#main-content">Skip to content</a>
    <header class="site-header" data-header>
        <div class="nav-shell">
            <a href="{% url 'home' %}" class="brand" aria-label="TaskSwap home"><span class="brand-mark" aria-hidden="true">TS</span><span class="brand-wordmark">TaskSwap</span></a>
            <button class="menu-toggle" type="button" aria-controls="primary-nav" aria-expanded="false" data-menu-toggle><span class="sr-only">Toggle navigation</span><span></span><span></span></button>
            <nav id="primary-nav" class="primary-nav" aria-label="Main navigation" data-primary-nav>
                <a href="{% url 'home' %}">Browse</a>
                {% if user.is_authenticated %}
                    <a href="{% url 'task_create' %}">Post a task</a><a href="{% url 'dashboard' %}">Dashboard</a>
                    {% if user.is_admin %}<a href="{% url 'admin_dashboard' %}">Moderation</a>{% endif %}
                    <a href="{% url 'profile' %}" class="nav-account">{{ user.name }}</a>
                    <form method="post" action="{% url 'logout' %}" class="inline-form">{% csrf_token %}<button type="submit" class="nav-link-button">Sign out</button></form>
                {% else %}
                    <a href="{% url 'login' %}">Sign in</a><a href="{% url 'signup' %}" class="nav-cta">Join TaskSwap</a>
                {% endif %}
            </nav>
        </div>
    </header>
    {% if messages %}<div class="message-stack" aria-live="polite">{% for message in messages %}<div class="message message--{{ message.tags|default:'info' }}">{{ message }}</div>{% endfor %}</div>{% endif %}
    <main id="main-content">{% block content %}{% endblock %}</main>
    <footer class="site-footer"><div class="footer-shell"><p><strong>TaskSwap</strong> · Small asks. Practical help.</p><p>Local exchanges, clearly arranged.</p></div></footer>
    <script src="{% static 'core/js/app.js' %}" defer></script>
</body>
</html>

```

## `core/templates/core/dashboard.html`

```html
{# Quiet Utility reminder: dashboard surfaces live state rather than ornamental metrics. #}
{% extends "core/base.html" %}{% block title %}Your dashboard · TaskSwap{% endblock %}{% block content %}<section class="page-hero reveal"><p class="eyebrow">Your activity</p><h1>Keep the exchange moving.</h1><p>Everything you have posted and every offer you have made, in one place.</p><a class="button button--ink" href="{% url 'task_create' %}">Post a task</a></section>
<section class="dashboard-section reveal" aria-labelledby="posted-heading"><div class="shelf-heading"><div><p class="eyebrow">You asked</p><h2 id="posted-heading">My posted tasks.</h2></div><a class="text-link" href="{% url 'task_create' %}">Post another <span aria-hidden="true">→</span></a></div><div class="table-list">{% for task in posted_tasks %}<a class="table-row" href="{% url 'task_detail' task.id %}"><span class="table-row__title">{{ task.title }}</span><span>{{ task.get_category_display }}</span><span class="status status--{{ task.status }}">{{ task.get_status_display }}</span><span>{{ task.applications.count }} applicant{{ task.applications.count|pluralize }}</span><span>→</span></a>{% empty %}<div class="empty-state empty-state--compact"><h3>Your first task starts the exchange.</h3><a class="button button--ink" href="{% url 'task_create' %}">Post a task</a></div>{% endfor %}</div></section>
<section class="dashboard-section dashboard-section--tint reveal" aria-labelledby="applications-heading"><div class="shelf-heading"><div><p class="eyebrow">You offered</p><h2 id="applications-heading">My applications.</h2></div><a class="text-link" href="{% url 'home' %}">Browse tasks <span aria-hidden="true">→</span></a></div><div class="table-list">{% for application in applications %}<a class="table-row" href="{% url 'task_detail' application.task.id %}"><span class="table-row__title">{{ application.task.title }}</span><span>For {{ application.task.posted_by.name }}</span><span class="status status--{{ application.status }}">{{ application.get_status_display }}</span><span>{{ application.created_at|date:"M j, Y" }}</span><span>→</span></a>{% empty %}<div class="empty-state empty-state--compact"><h3>Find a task you can make easier.</h3><a class="button button--ink" href="{% url 'home' %}">Browse open tasks</a></div>{% endfor %}</div></section>{% endblock %}

```

## `core/templates/core/home.html`

```html
{# Quiet Utility reminder: use full-height statements, explicit task data, and no decorative imagery. #}
{% extends "core/base.html" %}
{% block title %}TaskSwap — Neighbours help neighbours{% endblock %}
{% block content %}
<section class="hero hero--home reveal" aria-labelledby="hero-heading"><div class="hero-copy"><p class="eyebrow">A local exchange for useful skills</p><h1 id="hero-heading">Make the ask.</h1><p class="hero-subtitle">Post a small task. Find a real hand nearby.</p><div class="hero-actions">{% if user.is_authenticated %}<a class="button button--ink" href="{% url 'task_create' %}">Post a task</a>{% else %}<a class="button button--ink" href="{% url 'signup' %}">Join TaskSwap</a>{% endif %}</div></div><a class="scroll-cue" href="#how-it-works">See how it works <span aria-hidden="true">↓</span></a></section>
<section id="how-it-works" class="statement-stage stage--light reveal" aria-label="How TaskSwap works"><div class="statement-copy"><p class="stage-number">01</p><h2>Post it.</h2><p>Describe the task, choose a deadline, and put a clear budget on it.</p></div></section>
<section class="statement-stage stage--ink reveal"><div class="statement-copy"><p class="stage-number">02</p><h2>Get help.</h2><p>Review thoughtful applications from people ready to lend their skill.</p></div></section>
<section class="statement-stage stage--blue reveal"><div class="statement-copy"><p class="stage-number">03</p><h2>Done.</h2><p>Choose your helper, complete the task, and keep your neighbourhood moving.</p></div></section>
<section class="task-shelf reveal" aria-labelledby="open-tasks-heading"><div class="shelf-heading"><div><p class="eyebrow">The task board</p><h2 id="open-tasks-heading">Open now.</h2></div>{% if user.is_authenticated %}<a class="text-link" href="{% url 'task_create' %}">Post your own <span aria-hidden="true">→</span></a>{% endif %}</div>
    <form class="task-filters" method="get" aria-label="Filter open tasks"><label class="search-field" for="id_q"><span class="sr-only">Search open tasks</span><input id="id_q" name="q" value="{{ query }}" type="search" placeholder="Search tasks"></label><label for="id_category" class="sr-only">Category</label><select id="id_category" name="category"><option value="">All categories</option>{% for value, label in categories %}<option value="{{ value }}" {% if selected_category == value %}selected{% endif %}>{{ label }}</option>{% endfor %}</select><label for="id_sort" class="sr-only">Sort results</label><select id="id_sort" name="sort"><option value="newest" {% if selected_sort == 'newest' %}selected{% endif %}>Newest first</option><option value="deadline" {% if selected_sort == 'deadline' %}selected{% endif %}>Deadline first</option></select><button class="button button--outline" type="submit">Refine</button></form>
    <div class="task-list" aria-live="polite">{% for task in tasks %}<article class="task-row"><div class="task-row__main"><p class="task-row__meta">{{ task.get_category_display }} · Posted by <a href="{% url 'public_profile' task.posted_by.id %}">{{ task.posted_by.name }}</a></p><h3><a href="{% url 'task_detail' task.id %}">{{ task.title }}</a></h3><p>{{ task.description|truncatechars:150 }}</p></div><div class="task-row__side"><strong>${{ task.budget|floatformat:2 }}</strong><span>By {{ task.deadline|date:"M j" }}</span><a class="text-link" href="{% url 'task_detail' task.id %}">View task <span aria-hidden="true">→</span></a></div></article>{% empty %}<div class="empty-state"><p class="eyebrow">Nothing matches yet</p><h3>Be the first to put an ask out there.</h3>{% if user.is_authenticated %}<a class="button button--ink" href="{% url 'task_create' %}">Post a task</a>{% else %}<a class="button button--ink" href="{% url 'signup' %}">Join to post</a>{% endif %}</div>{% endfor %}</div>
</section>
{% endblock %}

```

## `core/templates/core/login.html`

```html
{# Quiet Utility reminder: strong sign-in hierarchy; all paths are visible and direct. #}
{% extends "core/base.html" %}{% block title %}Sign in to TaskSwap{% endblock %}{% block content %}<section class="auth-layout reveal"><div class="auth-intro"><p class="eyebrow">Welcome back</p><h1>Pick up where you left off.</h1><p>See your posted tasks, applications, and next steps.</p></div><form method="post" class="form-card" novalidate>{% csrf_token %}<h2>Sign in</h2>{% include "core/partials/form_fields.html" with form=form %}{% if form.non_field_errors %}<div class="form-error">{{ form.non_field_errors }}</div>{% endif %}<button class="button button--ink button--full" type="submit">Sign in</button><p class="form-footnote"><a href="{% url 'password_forgot' %}">Forgot your password?</a></p><p class="form-footnote">New here? <a href="{% url 'signup' %}">Create an account</a>.</p></form></section>{% endblock %}

```

## `core/templates/core/partials/form_fields.html`

```html
{# Shared field renderer: labels, values, help text, and server-side validation errors. #}
{% for field in form %}<div class="form-field"><label for="{{ field.id_for_label }}">{{ field.label }}</label>{{ field }}{% if field.help_text %}<small class="help-text">{{ field.help_text|safe }}</small>{% endif %}{% for error in field.errors %}<p class="field-error">{{ error }}</p>{% endfor %}</div>{% endfor %}

```

## `core/templates/core/password_forgot.html`

```html
{# Quiet Utility reminder: leave account-existence information private while preserving clarity. #}
{% extends "core/base.html" %}{% block title %}Reset your password{% endblock %}{% block content %}<section class="narrow-page reveal"><div class="page-heading"><p class="eyebrow">Account access</p><h1>Reset your password.</h1><p>Enter your email and we will print a reset link to the development server console if an account exists.</p></div><form method="post" class="form-card form-card--wide" novalidate>{% csrf_token %}{% include "core/partials/form_fields.html" with form=form %}<button class="button button--ink" type="submit">Request reset link</button></form></section>{% endblock %}

```

## `core/templates/core/password_reset_confirm.html`

```html
{# Quiet Utility reminder: a valid reset link exposes only a simple secure next action. #}
{% extends "core/base.html" %}{% block title %}Choose a new password{% endblock %}{% block content %}<section class="narrow-page reveal"><div class="page-heading"><p class="eyebrow">Secure reset</p><h1>Choose a new password.</h1><p>This reset link is single-use and expires after 30 minutes.</p></div><form method="post" class="form-card form-card--wide" novalidate>{% csrf_token %}{% include "core/partials/form_fields.html" with form=form %}<button class="button button--ink" type="submit">Save new password</button></form></section>{% endblock %}

```

## `core/templates/core/password_reset_invalid.html`

```html
{# Quiet Utility reminder: tell the user clearly when a private credential cannot be used. #}
{% extends "core/base.html" %}{% block title %}Reset link unavailable{% endblock %}{% block content %}<section class="narrow-page reveal"><div class="page-heading page-heading--center"><p class="eyebrow">Reset link unavailable</p><h1>That link cannot be used.</h1><p>It may have expired or already been used. Request a fresh password reset link to continue.</p><a class="button button--ink" href="{% url 'password_forgot' %}">Request a new link</a></div></section>{% endblock %}

```

## `core/templates/core/profile.html`

```html
{# Quiet Utility reminder: personal data is constrained and task statistics remain precise. #}
{% extends "core/base.html" %}{% block title %}Your profile · TaskSwap{% endblock %}{% block content %}<section class="profile-hero reveal"><div class="profile-monogram" aria-hidden="true">{{ user.name|first|upper }}</div><div><p class="eyebrow">Your public profile</p><h1>{{ user.name }}</h1>{% if profile.location %}<p class="profile-location">{{ profile.location }}</p>{% endif %}</div><a class="button button--outline" href="{% url 'profile_edit' %}">Edit profile</a></section><section class="profile-grid reveal"><article class="profile-copy"><h2>About</h2><p>{{ profile.bio|default:"Add a few words about the way you like to help." }}</p></article><article class="profile-copy"><h2>Skills</h2><p>{{ profile.skills|default:"Add the practical skills you can offer." }}</p></article><div class="stat-block"><strong>{{ stats.tasks_posted }}</strong><span>tasks posted</span></div><div class="stat-block"><strong>{{ stats.tasks_completed }}</strong><span>tasks completed</span></div></section>{% endblock %}

```

## `core/templates/core/profile_edit.html`

```html
{# Quiet Utility reminder: only user-controlled public facts appear in this concise form. #}
{% extends "core/base.html" %}{% block title %}Edit profile · TaskSwap{% endblock %}{% block content %}<section class="narrow-page reveal"><div class="page-heading"><p class="eyebrow">Public profile</p><h1>Tell neighbours how you help.</h1><p>Keep it simple. These details are visible on your public TaskSwap profile.</p></div><form method="post" class="form-card form-card--wide" novalidate>{% csrf_token %}{% include "core/partials/form_fields.html" with form=form %}<button class="button button--ink" type="submit">Save profile</button></form></section>{% endblock %}

```

## `core/templates/core/public_profile.html`

```html
{# Quiet Utility reminder: show concise public expertise only, never private account data. #}
{% extends "core/base.html" %}{% block title %}{{ public_user.name }} · TaskSwap{% endblock %}{% block content %}<section class="profile-hero reveal"><div class="profile-monogram" aria-hidden="true">{{ public_user.name|first|upper }}</div><div><p class="eyebrow">TaskSwap member</p><h1>{{ public_user.name }}</h1>{% if profile.location %}<p class="profile-location">{{ profile.location }}</p>{% endif %}</div></section><section class="profile-grid reveal"><article class="profile-copy"><h2>About</h2><p>{{ profile.bio|default:"This member has not added a bio yet." }}</p></article><article class="profile-copy"><h2>Skills</h2><p>{{ profile.skills|default:"This member has not listed skills yet." }}</p></article><div class="stat-block"><strong>{{ completed_count }}</strong><span>tasks completed</span></div></section>{% endblock %}

```

## `core/templates/core/signup.html`

```html
{# Quiet Utility reminder: simple sign-up surface with one direct primary action. #}
{% extends "core/base.html" %}{% block title %}Join TaskSwap{% endblock %}{% block content %}<section class="auth-layout reveal"><div class="auth-intro"><p class="eyebrow">A useful local network</p><h1>Start with one ask.</h1><p>Join TaskSwap to post a task or offer a practical hand.</p></div><form method="post" class="form-card" novalidate>{% csrf_token %}<h2>Create your account</h2>{% include "core/partials/form_fields.html" with form=form %}<button class="button button--ink button--full" type="submit">Create account</button><p class="form-footnote">Already on TaskSwap? <a href="{% url 'login' %}">Sign in</a>.</p></form></section>{% endblock %}

```

## `core/templates/core/task_detail.html`

```html
{# Quiet Utility reminder: human task data, status, and ownership actions get clear hierarchy. #}
{% extends "core/base.html" %}{% block title %}{{ task.title }} · TaskSwap{% endblock %}{% block content %}
<section class="detail-hero reveal"><div class="detail-hero__copy"><a class="back-link" href="{% url 'home' %}">← Browse open tasks</a><p class="eyebrow">{{ task.get_category_display }}</p><h1>{{ task.title }}</h1><p class="detail-owner">Posted by <a href="{% url 'public_profile' task.posted_by.id %}">{{ task.posted_by.name }}</a> · {{ task.created_at|date:"M j, Y" }}</p></div><aside class="detail-aside" aria-label="Task summary"><p class="status status--{{ task.status }}">{{ task.get_status_display }}</p><strong class="detail-budget">${{ task.budget|floatformat:2 }}</strong><span>Deadline {{ task.deadline|date:"F j, Y" }}</span></aside></section>
<section class="detail-layout reveal"><article class="task-description"><h2>The ask</h2>{{ task.description|linebreaks }}</article><aside class="action-panel">{% if is_owner %}<p class="eyebrow">Your task</p><h2>Manage the next step.</h2>{% if task.status == 'in_progress' %}<form method="post" action="{% url 'complete_task' task.id %}">{% csrf_token %}<button class="button button--ink button--full" type="submit">Mark completed</button></form>{% elif task.status == 'completed' %}<p class="quiet-copy">This task is complete.</p>{% elif task.status == 'open' %}<p class="quiet-copy">Review applications below and select one person to help.</p>{% else %}<p class="quiet-copy">This task is not currently accepting new applicants.</p>{% endif %}{% elif user_application %}<p class="eyebrow">Your application</p><h2>Application {{ user_application.get_status_display|lower }}.</h2><p class="status status--{{ user_application.status }}">{{ user_application.get_status_display }}</p><p class="quiet-copy">Submitted {{ user_application.created_at|date:"M j" }}.</p>{% elif application_form %}<p class="eyebrow">Offer your help</p><h2>Make it personal.</h2><form method="post" action="{% url 'apply_to_task' task.id %}" novalidate>{% csrf_token %}{% include "core/partials/form_fields.html" with form=application_form %}<button class="button button--ink button--full" type="submit">Apply to help</button></form>{% elif not user.is_authenticated %}<p class="eyebrow">Ready to help?</p><h2>Join the exchange.</h2><p class="quiet-copy">Create an account to apply to this task.</p><a class="button button--ink button--full" href="{% url 'signup' %}">Join TaskSwap</a>{% else %}<p class="eyebrow">Task update</p><h2>This task is closed.</h2><p class="quiet-copy">The owner is no longer taking applications.</p>{% endif %}</aside></section>
{% if is_owner %}<section class="applicant-section reveal" aria-labelledby="applicant-heading"><div class="shelf-heading"><div><p class="eyebrow">Applicants</p><h2 id="applicant-heading">People ready to help.</h2></div><span class="count-label">{{ applicants|length }} total</span></div><div class="applicant-list">{% for application in applicants %}<article class="applicant-row"><div><p class="task-row__meta">Applied {{ application.created_at|date:"M j, Y" }}</p><h3><a href="{% url 'public_profile' application.applicant.id %}">{{ application.applicant.name }}</a></h3><p>{{ application.message }}</p></div><div class="applicant-row__actions"><span class="status status--{{ application.status }}">{{ application.get_status_display }}</span>{% if task.status == 'open' and application.status == 'pending' %}<form method="post" action="{% url 'accept_application' task.id application.id %}">{% csrf_token %}<button class="button button--ink" type="submit">Accept</button></form>{% endif %}</div></article>{% empty %}<div class="empty-state empty-state--compact"><h3>No applications yet.</h3><p>When someone applies, their note will appear here.</p></div>{% endfor %}</div></section>{% endif %}
{% endblock %}

```

## `core/templates/core/task_form.html`

```html
{# Quiet Utility reminder: let the task form breathe; one decision per field. #}
{% extends "core/base.html" %}{% block title %}Post a task · TaskSwap{% endblock %}{% block content %}<section class="narrow-page reveal"><div class="page-heading"><p class="eyebrow">New task</p><h1>Put the ask out there.</h1><p>Be clear about what you need, when you need it, and what you can offer.</p></div><form method="post" class="form-card form-card--wide" novalidate>{% csrf_token %}{% include "core/partials/form_fields.html" with form=form %}<button class="button button--ink" type="submit">Open this task</button></form></section>{% endblock %}

```

## `core/tests.py`

```python
"""End-to-end integration tests for the principal TaskSwap flows."""
from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Application, PasswordResetToken, Task, User


class TaskSwapFlowTests(TestCase):
    """Exercise workflows through the same routes a browser uses."""

    def setUp(self):
        self.owner = User.objects.create_user(
            email="owner@example.com", password="SafePass123!", name="Owner"
        )
        self.helper = User.objects.create_user(
            email="helper@example.com", password="SafePass123!", name="Helper"
        )
        self.task = Task.objects.create(
            title="Fix a shelf",
            description="Install a short shelf in a hallway.",
            category=Task.Category.HOME,
            budget="45.00",
            deadline=timezone.localdate() + timedelta(days=3),
            posted_by=self.owner,
        )

    def test_signup_creates_session_and_profile(self):
        response = self.client.post(reverse("signup"), {
            "name": "New Member",
            "email": "new@example.com",
            "password1": "DifferentSafe123!",
            "password2": "DifferentSafe123!",
        })
        self.assertRedirects(response, reverse("dashboard"))
        new_user = User.objects.get(email="new@example.com")
        self.assertTrue(new_user.check_password("DifferentSafe123!"))
        self.assertTrue(hasattr(new_user, "profile"))

    def test_apply_accept_and_complete_workflow(self):
        self.client.force_login(self.helper)
        response = self.client.post(reverse("apply_to_task", args=[self.task.id]), {
            "message": "I can bring the right tools and finish this carefully.",
        })
        self.assertRedirects(response, reverse("task_detail", args=[self.task.id]))
        application = Application.objects.get(task=self.task, applicant=self.helper)
        self.assertEqual(application.status, Application.Status.PENDING)

        self.client.force_login(self.owner)
        response = self.client.post(reverse("accept_application", args=[self.task.id, application.id]))
        self.assertRedirects(response, reverse("task_detail", args=[self.task.id]))
        self.task.refresh_from_db()
        application.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.IN_PROGRESS)
        self.assertEqual(application.status, Application.Status.ACCEPTED)

        response = self.client.post(reverse("complete_task", args=[self.task.id]))
        self.assertRedirects(response, reverse("task_detail", args=[self.task.id]))
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.COMPLETED)

    def test_password_reset_is_generic_and_single_use(self):
        with patch("builtins.print") as console_output:
            response = self.client.post(reverse("password_forgot"), {"email": self.owner.email}, follow=True)
        self.assertContains(response, "If this email exists, a reset link has been sent.")
        console_output.assert_called_once()
        reset = PasswordResetToken.objects.get(user=self.owner)
        response = self.client.post(reverse("password_reset_confirm", args=[reset.token]), {
            "new_password1": "NewestSafe123!",
            "new_password2": "NewestSafe123!",
        })
        self.assertRedirects(response, reverse("login"))
        reset.refresh_from_db()
        self.owner.refresh_from_db()
        self.assertTrue(reset.used)
        self.assertTrue(self.owner.check_password("NewestSafe123!"))
        self.assertEqual(self.client.get(reverse("password_reset_confirm", args=[reset.token])).status_code, 400)

    def test_profile_edit_and_public_profile_hide_private_email(self):
        self.client.force_login(self.owner)
        response = self.client.post(reverse("profile_edit"), {
            "bio": "I coordinate practical neighbourhood projects.",
            "skills": "Organising, repairs",
            "location": "Northside",
        })
        self.assertRedirects(response, reverse("profile"))
        public_response = self.client.get(reverse("public_profile", args=[self.owner.id]))
        self.assertContains(public_response, "Northside")
        self.assertNotContains(public_response, self.owner.email)

    def test_admin_routes_are_enforced_and_soft_delete_records(self):
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(reverse("admin_dashboard")).status_code, 403)

        moderator = User.objects.create_user(
            email="admin@example.com", password="SafePass123!", name="Moderator", is_admin=True
        )
        self.client.force_login(moderator)
        self.assertEqual(self.client.get(reverse("admin_dashboard")).status_code, 200)
        response = self.client.post(reverse("admin_remove_task", args=[self.task.id]))
        self.assertRedirects(response, reverse("admin_tasks"))
        self.task.refresh_from_db()
        self.assertEqual(self.task.status, Task.Status.REMOVED)
        self.assertTrue(Task.objects.filter(pk=self.task.id).exists())

    def test_homepage_search_and_category_filters_open_tasks_only(self):
        Task.objects.create(
            title="Hidden completed task",
            description="Already done.",
            category=Task.Category.TECH,
            budget="15.00",
            deadline=timezone.localdate() + timedelta(days=1),
            posted_by=self.owner,
            status=Task.Status.COMPLETED,
        )
        response = self.client.get(reverse("home"), {"q": "shelf", "category": "home", "sort": "deadline"})
        self.assertContains(response, "Fix a shelf")
        self.assertNotContains(response, "Hidden completed task")

```

## `core/urls.py`

```python
"""Application URL routes for public, account, task, and moderation experiences."""
from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("signup/", views.signup_view, name="signup"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("password/forgot/", views.password_forgot, name="password_forgot"),
    path("password/reset/<str:token>/", views.password_reset_confirm, name="password_reset_confirm"),
    path("tasks/new/", views.task_create, name="task_create"),
    path("tasks/<int:task_id>/", views.task_detail, name="task_detail"),
    path("tasks/<int:task_id>/apply/", views.apply_to_task, name="apply_to_task"),
    path("tasks/<int:task_id>/applications/<int:application_id>/accept/", views.accept_application, name="accept_application"),
    path("tasks/<int:task_id>/complete/", views.complete_task, name="complete_task"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("profile/", views.profile_view, name="profile"),
    path("profile/edit/", views.profile_edit, name="profile_edit"),
    path("users/<int:user_id>/", views.public_profile, name="public_profile"),
    path("admin/", views.admin_dashboard, name="admin_dashboard"),
    path("admin/users/", views.admin_users, name="admin_users"),
    path("admin/users/<int:user_id>/deactivate/", views.admin_deactivate_user, name="admin_deactivate_user"),
    path("admin/tasks/", views.admin_tasks, name="admin_tasks"),
    path("admin/tasks/<int:task_id>/remove/", views.admin_remove_task, name="admin_remove_task"),
]

```

## `core/views.py`

```python
"""Secure views for the complete TaskSwap task-exchange workflow."""
import secrets
from datetime import timedelta
from functools import wraps

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.exceptions import PermissionDenied
from django.db import transaction
from django.db.models import Count, Q
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from .forms import (
    ApplicationForm,
    EmailAuthenticationForm,
    NewPasswordForm,
    PasswordResetRequestForm,
    ProfileForm,
    SignupForm,
    TaskForm,
)
from .models import Application, PasswordResetToken, Profile, Task, User


def admin_required(view_func):
    """Require a logged-in account with the explicit TaskSwap admin flag on every route."""

    @login_required
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_admin:
            raise PermissionDenied("TaskSwap administration is restricted.")
        return view_func(request, *args, **kwargs)

    return wrapped_view


def home(request):
    """Show only currently open tasks, with safe server-side search/filter/sort controls."""
    tasks = Task.objects.filter(status=Task.Status.OPEN, posted_by__is_active=True).select_related("posted_by")
    query = request.GET.get("q", "").strip()
    selected_category = request.GET.get("category", "")
    selected_sort = request.GET.get("sort", "newest")

    if query:
        tasks = tasks.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if selected_category in Task.Category.values:
        tasks = tasks.filter(category=selected_category)

    if selected_sort == "deadline":
        tasks = tasks.order_by("deadline", "-created_at")
    else:
        selected_sort = "newest"
        tasks = tasks.order_by("-created_at")

    return render(request, "core/home.html", {
        "tasks": tasks,
        "categories": Task.Category.choices,
        "selected_category": selected_category,
        "selected_sort": selected_sort,
        "query": query,
    })


def signup_view(request):
    """Create an account and start a session using Django's password hashing."""
    if request.user.is_authenticated:
        return redirect("dashboard")
    form = SignupForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Your account is ready. Tell your neighbours what you need.")
        return redirect("dashboard")
    return render(request, "core/signup.html", {"form": form})


class TaskSwapLoginView(LoginView):
    """Use Django's session login with the email-focused authentication form."""

    template_name = "core/login.html"
    authentication_form = EmailAuthenticationForm
    redirect_authenticated_user = True


login_view = TaskSwapLoginView.as_view()


@require_POST
def logout_view(request):
    """End the current session through a CSRF-protected POST action."""
    logout(request)
    messages.success(request, "You have been signed out.")
    return redirect("home")


def password_forgot(request):
    """Create and print an opaque reset URL without exposing account existence."""
    form = PasswordResetRequestForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        email = form.cleaned_data["email"].lower()
        user = User.objects.filter(email__iexact=email, is_active=True).first()
        if user:
            # Invalidate outstanding requests so each issued link is single-use in practice.
            PasswordResetToken.objects.filter(user=user, used=False).update(used=True)
            token = secrets.token_urlsafe(32)
            reset_record = PasswordResetToken.objects.create(
                user=user,
                token=token,
                expires_at=timezone.now() + timedelta(minutes=30),
            )
            reset_url = request.build_absolute_uri(
                reverse("password_reset_confirm", kwargs={"token": reset_record.token})
            )
            print(f"[TaskSwap password reset] {reset_url}")

        # The same copy is sent for every valid email-shaped input to prevent enumeration.
        messages.success(request, "If this email exists, a reset link has been sent.")
        return redirect("login")
    return render(request, "core/password_forgot.html", {"form": form})


def password_reset_confirm(request, token):
    """Accept a password only when the presented token is valid, fresh, and unused."""
    reset_record = PasswordResetToken.objects.filter(token=token).select_related("user").first()
    if not reset_record or not reset_record.is_valid():
        return render(request, "core/password_reset_invalid.html", status=400)

    form = NewPasswordForm(reset_record.user, request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        reset_record.used = True
        reset_record.save(update_fields=["used"])
        messages.success(request, "Your password has been reset. Please sign in.")
        return redirect("login")
    return render(request, "core/password_reset_confirm.html", {"form": form})


@login_required
def task_create(request):
    """Create a task in the open state; status and ownership remain server-controlled."""
    form = TaskForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task = form.save(commit=False)
        task.posted_by = request.user
        task.status = Task.Status.OPEN
        task.save()
        messages.success(request, "Your task is open for applications.")
        return redirect("task_detail", task_id=task.id)
    return render(request, "core/task_form.html", {"form": form})


def task_detail(request, task_id):
    """Show a task, its owner controls, or a current applicant's state."""
    task = get_object_or_404(Task.objects.select_related("posted_by"), pk=task_id)
    if task.status == Task.Status.REMOVED and not (
        request.user.is_authenticated and (request.user.is_admin or request.user == task.posted_by)
    ):
        raise PermissionDenied("This task is no longer available.")

    is_owner = request.user.is_authenticated and request.user.id == task.posted_by_id
    user_application = None
    application_form = None
    applicants = None

    if is_owner:
        applicants = task.applications.select_related("applicant").all()
    elif request.user.is_authenticated:
        user_application = task.applications.filter(applicant=request.user).first()
        if task.status == Task.Status.OPEN and not user_application:
            application_form = ApplicationForm()

    return render(request, "core/task_detail.html", {
        "task": task,
        "is_owner": is_owner,
        "applicants": applicants,
        "user_application": user_application,
        "application_form": application_form,
    })


@login_required
@require_POST
def apply_to_task(request, task_id):
    """Create one pending application when a non-owner applies to an open task."""
    task = get_object_or_404(Task, pk=task_id)
    if task.posted_by_id == request.user.id:
        raise PermissionDenied("You cannot apply to your own task.")
    if task.status != Task.Status.OPEN:
        messages.error(request, "This task is not accepting applications.")
        return redirect("task_detail", task_id=task.id)
    if Application.objects.filter(task=task, applicant=request.user).exists():
        messages.info(request, "You have already applied to this task.")
        return redirect("task_detail", task_id=task.id)

    form = ApplicationForm(request.POST)
    if form.is_valid():
        application = form.save(commit=False)
        application.task = task
        application.applicant = request.user
        application.status = Application.Status.PENDING
        application.save()
        messages.success(request, "Your application has been sent.")
        return redirect("task_detail", task_id=task.id)
    return render(request, "core/task_detail.html", {
        "task": task,
        "is_owner": False,
        "application_form": form,
    }, status=400)


@login_required
@require_POST
def accept_application(request, task_id, application_id):
    """Atomically accept one applicant, reject the remainder, and start the task."""
    with transaction.atomic():
        task = get_object_or_404(Task.objects.select_for_update(), pk=task_id)
        if task.posted_by_id != request.user.id:
            raise PermissionDenied("Only the task owner can choose an applicant.")
        if task.status != Task.Status.OPEN:
            return HttpResponseBadRequest("Only open tasks can accept an application.")
        application = get_object_or_404(
            Application.objects.select_for_update(), pk=application_id, task=task
        )
        if application.status != Application.Status.PENDING:
            return HttpResponseBadRequest("Only pending applications can be accepted.")
        Application.objects.filter(task=task).exclude(pk=application.pk).update(status=Application.Status.REJECTED)
        application.status = Application.Status.ACCEPTED
        application.save(update_fields=["status"])
        task.status = Task.Status.IN_PROGRESS
        task.save(update_fields=["status"])

    messages.success(request, f"{application.applicant.name} has been selected. The task is now in progress.")
    return redirect("task_detail", task_id=task.id)


@login_required
@require_POST
def complete_task(request, task_id):
    """Let only the task owner transition an in-progress task to completed."""
    task = get_object_or_404(Task, pk=task_id)
    if task.posted_by_id != request.user.id:
        raise PermissionDenied("Only the task owner can complete this task.")
    if task.status != Task.Status.IN_PROGRESS:
        return HttpResponseBadRequest("Only in-progress tasks can be completed.")
    task.status = Task.Status.COMPLETED
    task.save(update_fields=["status"])
    messages.success(request, "Task marked completed.")
    return redirect("task_detail", task_id=task.id)


@login_required
def dashboard(request):
    """Show live task and application states for the current signed-in user."""
    posted_tasks = request.user.tasks.all().prefetch_related("applications")
    applications = request.user.applications.select_related("task", "task__posted_by")
    return render(request, "core/dashboard.html", {
        "posted_tasks": posted_tasks,
        "applications": applications,
    })


@login_required
def profile_view(request):
    """Render the owner's profile and activity statistics."""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    stats = {
        "tasks_posted": request.user.tasks.count(),
        "tasks_completed": request.user.tasks.filter(status=Task.Status.COMPLETED).count(),
    }
    return render(request, "core/profile.html", {"profile": profile, "stats": stats})


@login_required
def profile_edit(request):
    """Edit only the signed-in user's profile; never read ownership from a form field."""
    profile, _ = Profile.objects.get_or_create(user=request.user)
    # Explicit server-side ownership assertion keeps this route safe if it is ever refactored.
    if request.user.id != profile.user_id:
        raise PermissionDenied("You can only edit your own profile.")
    form = ProfileForm(request.POST or None, instance=profile)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Your public profile has been updated.")
        return redirect("profile")
    return render(request, "core/profile_edit.html", {"form": form})


def public_profile(request, user_id):
    """Render only explicitly public profile details and a completed-task count."""
    user = get_object_or_404(User, pk=user_id, is_active=True)
    profile, _ = Profile.objects.get_or_create(user=user)
    completed_count = user.tasks.filter(status=Task.Status.COMPLETED).count()
    return render(request, "core/public_profile.html", {
        "public_user": user,
        "profile": profile,
        "completed_count": completed_count,
    })


@admin_required
def admin_dashboard(request):
    """Present moderation KPIs built with database COUNT and GROUP BY aggregates."""
    week_ago = timezone.now() - timedelta(days=7)
    total_users = User.objects.count()
    tasks_this_week = Task.objects.filter(created_at__gte=week_ago).count()
    status_counts = Task.objects.values("status").annotate(total=Count("id")).order_by("status")
    task_total = sum(row["total"] for row in status_counts)
    completed_total = next((row["total"] for row in status_counts if row["status"] == Task.Status.COMPLETED), 0)
    completion_rate = (completed_total / task_total * 100) if task_total else 0
    return render(request, "core/admin_dashboard.html", {
        "total_users": total_users,
        "tasks_this_week": tasks_this_week,
        "completion_rate": completion_rate,
        "status_counts": status_counts,
    })


@admin_required
def admin_users(request):
    """List and search all user accounts for moderation decisions."""
    query = request.GET.get("q", "").strip()
    users = User.objects.all()
    if query:
        users = users.filter(Q(name__icontains=query) | Q(email__icontains=query))
    return render(request, "core/admin_users.html", {"users": users, "query": query})


@admin_required
@require_POST
def admin_deactivate_user(request, user_id):
    """Soft-deactivate an account without deleting related task records."""
    user = get_object_or_404(User, pk=user_id)
    if user.id == request.user.id:
        messages.error(request, "You cannot deactivate your own account.")
    elif user.is_superuser:
        messages.error(request, "Superuser accounts must be managed through Django administration.")
    else:
        user.is_active = False
        user.save(update_fields=["is_active"])
        messages.success(request, f"{user.name} has been deactivated.")
    return redirect("admin_users")


@admin_required
def admin_tasks(request):
    """List every task, including non-public states, for policy review."""
    tasks = Task.objects.select_related("posted_by").all()
    return render(request, "core/admin_tasks.html", {"tasks": tasks})


@admin_required
@require_POST
def admin_remove_task(request, task_id):
    """Soft-remove a task by changing only its status and preserving its record."""
    task = get_object_or_404(Task, pk=task_id)
    if task.status != Task.Status.REMOVED:
        task.status = Task.Status.REMOVED
        task.save(update_fields=["status"])
        messages.success(request, f"“{task.title}” has been removed from public browsing.")
    return redirect("admin_tasks")

```
