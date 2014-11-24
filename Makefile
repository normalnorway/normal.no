.PHONY: activate test


# 1) Merge changes from 'master' to 'production'.
# 2) Push the changes.
# 3) Activate on production server
#activate: test
activate:
	git checkout production
	git merge master
	git push
	git checkout master

test:
	(cd django && ./manage.py test)
	#python django/tests.py  # run by django
	python test/livesite.py
	#fab test
