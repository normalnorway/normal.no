.PHONY: relase deploy wip test livetest

all:
	@echo I do nothing by default!

# @todo rename make-relase
release:
	@echo finish me
	#sh minify-js.sh
	# ensure clean working tree
	# git fetch
	# git checkout live
	# git rebase master	# origin/master?
	# or: git pull origin/master --rebase
	# @todo might fail if can't fast-forward
	# git push live
	# git checkout master

wip:
	git commit -am wip


#activate: make-release
deploy:
	ssh normal.no '(cd /srv/www/normal.no ; sh update.sh)'
	# @todo run livetest after and abort if it fails
	# @todo run django tests before (and abort on failure)


# Offline tests
test:
	(cd django && ./manage.py check)
	#(cd django && ./manage.py test)
	(cd django && ./manage.py test -v 2)
	$(MAKE) -C django/static/css/ test
	@#python django/tests.py  # already run by django manage.py test
	@#@todo jslint


# Test the live site: http://normal.no
# @todo test this after activate new version, and rollback if test fails
# rename livetest?
test-live:
	python test/livesite.py
