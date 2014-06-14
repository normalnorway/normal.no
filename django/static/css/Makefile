# @todo merge and compress all css files
# lessc *.less > all.css
# update: but some files need single copy, like tinymcs inline styles

#LESSC=`which lessc`
LESSC=lessc

cssfiles := $(patsubst %.less,%.css,$(wildcard *.less))

all: $(cssfiles)

%.css : %.less
	$(LESSC) $^ > $@
