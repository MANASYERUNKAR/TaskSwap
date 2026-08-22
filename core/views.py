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
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.http import require_POST

from .forms import (
    ApplicationForm,
    EmailAuthenticationForm,
    NewPasswordForm,
    PasswordResetRequestForm,
    ProfileForm,
    SignupForm,
    TaskForm,
    TaskMessageForm,
)
from .models import Application, PasswordResetToken, Profile, Task, TaskMessage, User


def admin_required(view_func):
    """Require a logged-in account with the explicit TaskSwap admin flag on every route."""

    @login_required
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_admin:
            raise PermissionDenied("TaskSwap administration is restricted.")
        return view_func(request, *args, **kwargs)

    return wrapped_view


@ensure_csrf_cookie
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


@ensure_csrf_cookie
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


@method_decorator(ensure_csrf_cookie, name="dispatch")
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


@ensure_csrf_cookie
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


@ensure_csrf_cookie
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
def task_conversation(request, task_id):
    """Let the owner, accepted helper, or an administrator coordinate on an accepted task."""
    task = get_object_or_404(Task.objects.select_related("posted_by"), pk=task_id)
    accepted_application = task.applications.filter(
        status=Application.Status.ACCEPTED
    ).select_related("applicant").first()

    if not accepted_application:
        raise PermissionDenied("A private conversation opens only after a helper is accepted.")

    is_owner = request.user.id == task.posted_by_id
    is_accepted_helper = request.user.id == accepted_application.applicant_id
    if not (is_owner or is_accepted_helper or request.user.is_admin):
        raise PermissionDenied("This conversation is private to the accepted task participants.")

    form = TaskMessageForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        task_message = form.save(commit=False)
        task_message.task = task
        task_message.sender = request.user
        task_message.save()
        messages.success(request, "Your private message has been sent.")
        return redirect("task_conversation", task_id=task.id)

    counterpart = accepted_application.applicant if is_owner else task.posted_by
    thread = task.messages.select_related("sender").all()
    return render(request, "core/task_conversation.html", {
        "task": task,
        "accepted_application": accepted_application,
        "counterpart": counterpart,
        "thread": thread,
        "form": form,
        "is_owner": is_owner,
        "is_admin_view": request.user.is_admin and not (is_owner or is_accepted_helper),
    })


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
