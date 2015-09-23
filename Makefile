.PHONY: all pill wip bugfix minor deploy test livetest

all:
	@echo I do nothing by default!

pull:
	echo Rebasing from upstream branch ...
	git stash
	git pull --rebase
	git stash pop

wip:
	git commit -am wip

bugfix:
	git commit -am bugfix

minor:
	git commit -am minor


#activate: make-release
# @todo run livetest as last step and abort (rollback) if it fails
deploy: test
	ssh normal.no '(cd /srv/www/normal.no ; sh update.sh)'


# @todo rename make-relase
#release:
#	@echo finish me
	#sh minify-js.sh
	# ensure clean working tree
	# git fetch
	# git checkout live
	# git rebase master	# origin/master?
	# or: git pull origin/master --rebase
	# @todo might fail if can't fast-forward
	# git push live
	# git checkout master


# Run tests
# @todo jslint
test:
	(cd django && ./manage.py check)
	(cd django && ./manage.py test -v 2)
	$(MAKE) -C django/static/css/ test


# Test the live site: http://normal.no
livetest:
	python test/livesite.py
