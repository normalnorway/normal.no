MARKDOWN=markdown_py -x toc -o html5

all: how-to-contribute.html

view: how-to-contribute.html
	x-www-browser $^

how-to-contribute.html: how-to-contribute.head how-to-contribute.md
	cat $^ | $(MARKDOWN) | sed -e "s/@@DATE@@/`date --iso`/" > $@

# Note: Outdated!
# This file is found under:
# http://git.normal.no/git/normal.no/about/
# But note: cgit uses caching, so will not show up immediately!
#upload: how-to-contribute.html
#	scp $^ git.normal.no:/srv/www/git.normal.no/readme.html

#%.html : %.md
#	$(MARKDOWN) $< | sed -e "s/@@DATE@@/`date --iso`/" > $@
