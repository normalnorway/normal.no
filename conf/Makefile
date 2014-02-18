
# TODO make overridable from env or with: make ServerName=normal.no
#ServerName?=dev.normal.no
#ServerPath?=/srv/www/$(ServerName)

apache.conf: apache.conf.in
	sed 's/@@ServerName@@/dev.normal.no/g' $< > $@
