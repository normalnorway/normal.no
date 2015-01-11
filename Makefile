.PHONY: bugfix minor test


bugfix:
	git commit -m bugfix

minor:
	git commit -m minor


## Done on local dev system
# Note: Can not have local changes. Can do git stash push + pop.
# 1) Merge changes from 'master' into 'production'.
# 2) Push the changes.
master-to-production:
	git checkout production
	git merge master
	git push
	git checkout master

activate: master-to-production
	ssh normal.no '(cd /srv/www/normal.no ; ./update.sh)'
	# @todo run livetest after and abort if it fails
	# @todo run django tests before (and abort on failure)


test:
	(cd django && ./manage.py test)
	#python django/tests.py  # run by django
	python test/livesite.py
	#fab test
