# Preview correction checklist

- [x] Inspect the current managed startup command and identify why it serves the React starter page.
- [x] Point the managed development preview at Django's `manage.py runserver` process through the package-level preview command.
- [x] Restart the preview service and verify that TaskSwap, not the example page, is rendered.

# CSRF preview-origin checklist

- [x] Add the managed preview domain pattern to Django's trusted CSRF origins.
- [x] Restart the service and confirm a CSRF-protected POST succeeds from the preview host.

# CSRF cookie delivery checklist

- [x] Configure Django's preview cookies for secure cross-site iframe delivery.
- [x] Ensure public form routes explicitly issue a CSRF cookie before a submission.
- [x] Restart and verify that the preview browser receives the CSRF cookie and accepts a CSRF-protected form submission.

# Demo task checklist

- [x] Add a demo account and representative open tasks across TaskSwap categories.
- [x] Verify that the homepage task board renders the seeded listings.

# Private task conversation checklist

- [x] Add a task message model and migration that links each message to an accepted task and sender.
- [x] Enforce owner, accepted-helper, and administrator access in the private conversation route.
- [x] Add conversation access and message posting controls to accepted tasks and the dashboard.
- [x] Test posting, visibility, and denied access for unrelated users.
