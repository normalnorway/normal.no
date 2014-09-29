MARKDOWN=markdown_py -x toc
#MARKDOWN=markdown_py -o html5


all: how-to-contribute.html
	firefox $^

# This file is found under:
# http://git.normal.no/git/normal.no/about/
# But note: cgit uses caching, so will not show up immediately!
upload: how-to-contribute.html
	scp $^ git.normal.no:/srv/www/git.normal.no/readme.html


# Suffix rule from markdown to html
%.html : %.md
	$(MARKDOWN) $< | sed -e "s/@@LAST-UPDATE@@/`date --iso`/" > $@
#	$(MARKDOWN) $< > $@
