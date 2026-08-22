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
