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


class TaskMessage(models.Model):
    """A private coordination message visible only after a task accepts a helper."""

    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="messages")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="task_messages")
    body = models.TextField(max_length=2000)
    created_at = models.DateTimeField(default=timezone.now, editable=False)

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["task", "created_at"])]

    def __str__(self):
        return f"Message on {self.task} from {self.sender}"


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
