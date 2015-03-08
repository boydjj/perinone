

all:
	python manage.py test

reset:
	rm -rf db.sqlite3
	python manage.py syncdb
