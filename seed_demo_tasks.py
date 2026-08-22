"""Create idempotent local-only TaskSwap listings for preview and UI testing."""
import os
from datetime import timedelta

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tasksite.settings")

import django

django.setup()

from django.utils import timezone

from core.models import Profile, Task, User


def main():
    """Create a named demo poster and a small, representative open task board."""
    demo_user, created = User.objects.get_or_create(
        email="local.demo@taskswap.test",
        defaults={"name": "TaskSwap Demo", "is_active": True},
    )
    if created:
        demo_user.set_password("LocalDemoOnly123!")
        demo_user.save(update_fields=["password"])

    Profile.objects.update_or_create(
        user=demo_user,
        defaults={
            "bio": "Local demo account used to populate the TaskSwap preview.",
            "skills": "Community coordination, practical planning",
            "location": "Local preview",
        },
    )

    today = timezone.localdate()
    task_data = [
        {
            "title": "Assemble a flat-pack bookshelf",
            "description": "I have a medium bookshelf still in its boxes and would appreciate a careful hand assembling it in my living room. The instructions and all fittings are ready.",
            "category": Task.Category.HOME,
            "budget": "55.00",
            "deadline": today + timedelta(days=4),
        },
        {
            "title": "Set up a home Wi-Fi mesh",
            "description": "Help place and configure two mesh nodes so the home office and back room have a more reliable connection. The equipment is already purchased.",
            "category": Task.Category.TECH,
            "budget": "70.00",
            "deadline": today + timedelta(days=2),
        },
        {
            "title": "Coach me through a budget spreadsheet",
            "description": "I would like a one-hour session learning how to organise monthly expenses in a simple spreadsheet that I can keep using on my own.",
            "category": Task.Category.LEARNING,
            "budget": "35.00",
            "deadline": today + timedelta(days=5),
        },
        {
            "title": "Design a clean fundraiser poster",
            "description": "Create an A4 digital poster for a small neighbourhood sports fundraiser. The copy, date, location, and logo are ready to share.",
            "category": Task.Category.CREATIVE,
            "budget": "45.00",
            "deadline": today + timedelta(days=6),
        },
        {
            "title": "Photograph a community clean-up",
            "description": "Take a handful of candid photographs at a two-hour Saturday morning clean-up so organisers can share a short recap afterwards.",
            "category": Task.Category.EVENTS,
            "budget": "90.00",
            "deadline": today + timedelta(days=7),
        },
        {
            "title": "Move two planters to a rooftop garden",
            "description": "Help move two medium planters safely up one flight of stairs and position them on the shared rooftop garden. A trolley is available.",
            "category": Task.Category.HOME,
            "budget": "40.00",
            "deadline": today + timedelta(days=3),
        },
    ]

    for data in task_data:
        Task.objects.update_or_create(
            posted_by=demo_user,
            title=data["title"],
            defaults={**data, "status": Task.Status.OPEN},
        )

    print(f"TaskSwap demo board ready: {len(task_data)} open listings under {demo_user.email}")


if __name__ == "__main__":
    main()
