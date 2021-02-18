# InstaGo - Simple Django Blog Projects

InstaGo is just a simple developer blogging site made with Django - The python web framework.
Here you can write blogs in a very simple way, with a WYSIWYG editor, authentication facility, searching blogs and people, etc..
You can comment and like posts that you love and make friends.

#### Requirements
You will need the following packages:
- pipenv
- django
- mysqlclient
- pillow
- django-quill-editor

You can install these with python 3.8 and pipenv installed using command `pipenv install` after creating environment with `pipenv shell`.

**Note**
After installing all dependencies/packages migrate to the desired database (sqlite3 by default) with `python manage.py migrate` and for static files run `python manage.py collectstatic`.