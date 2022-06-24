import django, os
os.environ['DJANGO_SETTINGS_MODULE'] = 'alurareceita.settings'
django.setup()
django.core.management.execute_from_command_line(['manage.py', 'makemigrations'])
django.core.management.execute_from_command_line(['manage.py', 'migrate'])
django.core.management.execute_from_command_line(['manage.py createsuperuser --noinput'])
django.core.management.execute_from_command_line(['manage.py', 'loaddata', 'initial-data.json'])
