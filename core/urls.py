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
    path("tasks/<int:task_id>/conversation/", views.task_conversation, name="task_conversation"),
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
