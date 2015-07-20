# Converts all less files to css and compress them.
# Note: Requires GNU Make
# @todo add check to main target?
# @todo all.min.css?

.PHONY: all production clean check test

LESSC=lessc
LESSCFLAGS=--no-js --clean-css --compress
# Note: --clean-css compress a little bit better than --compress
# Update: With Debians node-less (1.4.2), --clean-css does not compress!

# XXX Hack for lessc 2.5.0 on srv1
# Unable to interpret argument clean-css - if it is a plugin
#   (less-plugin-clean-css), make sure that it is installed under or at
#   the same level as less
# The compress option has been deprecated. We recommend you use
#   a dedicated css minifier, for instance see less-plugin-clean-css.
LESSCFLAGS=--no-js --compress


cssfiles := $(patsubst %.less,%.css,$(wildcard *.less))
# SOURCES = site.less style.less classes.less sections.less
# OBJS    = ${SOURCES:.less=.less}

# can do this instead. don't need gnu make? a: yes, wildcard
#SOURCES = site.less style.less classes.less sections.less
#SOURCES = $(wildcard *.less)
#OBJS    = ${SOURCES:.less=.css}

all: all.css tinymce.css

# Like 'all' but removes css files not needed on the production server.
# @todo add check target?
production: all
	$(MAKE) clean


all.css: $(cssfiles)
	cat $^ > all.css

# For TinyMCEs content_css
tinymce.css: style.css classes.css sections.css
	cat $^ > $@

test: check
check:
	@for file in *.less ; do	\
	    echo Checking $$file ... ;	\
	    $(LESSC) --lint $$file ;	\
	done

# @todo join clan & clean-all
clean:
	rm -fv $(cssfiles)

clean-all: clean
	rm -fv all.css tinymce.css

# @todo move check to own target. then put that target first in 'all' target
%.css : %.less
	@if [ x = x`/bin/which $(LESSC)` ]; then		\
	    echo "Error: The lessc compiler is missing!";	\
	    echo "Install it with: apt-get install node-less";	\
	    echo "        or with: npm install less -g";	\
	    exit 1;						\
	fi
	$(LESSC) $(LESSCFLAGS) $^ > $@
