.PHONY: all rebase wip bugfix minor deploy test livetest

all:
	@echo I do nothing by default!

rebase:
	echo Rebasing from upstream branch ...
	git stash
	git pull --rebase
	git stash pop

bugfix:
	git commit -am bugfix
	git push

minor:
	git commit -am minor

wip:
	git commit -am wip

#activate: make-release
# @todo run livetest as last step and abort (rollback) if it fails
deploy: test
	ssh normal.no '(cd /srv/www/normal.no ; sh update.sh)'


# Run tests
# @todo jslint
test:
	(cd django && ./manage.py check)
	(cd django && ./manage.py test -v 2)
	$(MAKE) -C django/static/css/ test


# Test urls on the live site
livetest:
	python test/livesite.py
