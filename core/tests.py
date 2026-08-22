"""End-to-end integration tests for the principal TaskSwap flows."""
from datetime import timedelta
from unittest.mock import patch

from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Application, PasswordResetToken, Task, TaskMessage, User


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

    def test_private_conversation_allows_only_accepted_task_participants(self):
        application = Application.objects.create(
            task=self.task,
            applicant=self.helper,
            message="I can help with this shelf installation.",
            status=Application.Status.ACCEPTED,
        )
        self.task.status = Task.Status.IN_PROGRESS
        self.task.save(update_fields=["status"])
        conversation_url = reverse("task_conversation", args=[self.task.id])

        self.client.force_login(self.owner)
        response = self.client.post(conversation_url, {
            "body": "Please come to 18 Cedar Lane at 10:00 on Saturday."
        })
        self.assertRedirects(response, conversation_url)
        owner_message = TaskMessage.objects.get(task=self.task, sender=self.owner)
        self.assertIn("Cedar Lane", owner_message.body)

        self.client.force_login(self.helper)
        response = self.client.get(conversation_url)
        self.assertContains(response, "18 Cedar Lane")
        response = self.client.post(conversation_url, {
            "body": "Confirmed. I will bring a drill and arrive at 10:00."
        })
        self.assertRedirects(response, conversation_url)
        self.assertEqual(TaskMessage.objects.filter(task=self.task).count(), 2)

        unrelated_user = User.objects.create_user(
            email="unrelated@example.com", password="SafePass123!", name="Unrelated"
        )
        self.client.force_login(unrelated_user)
        self.assertEqual(self.client.get(conversation_url).status_code, 403)
        self.assertEqual(self.client.post(conversation_url, {"body": "Let me in."}).status_code, 403)

        moderator = User.objects.create_user(
            email="moderator@example.com", password="SafePass123!", name="Moderator", is_admin=True
        )
        self.client.force_login(moderator)
        self.assertEqual(self.client.get(conversation_url).status_code, 200)

        # A task without an accepted application cannot expose a conversation to anyone.
        unopened_task = Task.objects.create(
            title="Open task without a helper",
            description="A conversation must not exist yet.",
            category=Task.Category.OTHER,
            budget="20.00",
            deadline=timezone.localdate() + timedelta(days=2),
            posted_by=self.owner,
        )
        self.client.force_login(self.owner)
        self.assertEqual(self.client.get(reverse("task_conversation", args=[unopened_task.id])).status_code, 403)

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
