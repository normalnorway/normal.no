DOMAIN=normal.no
PREFIX=/srv/www/$(DOMAIN)

# @VARNAME@ => {{VARNAME}} ?

apache.conf: apache.conf.in
	sed -e 's/@DOMAIN@/$(DOMAIN)/g' \
	    -e 's|@PREFIX@|$(PREFIX)|g' < $< > $@


config-to-stdout:
	@if [ x$(DOMAIN) = x ]; then \
	    echo "Error: Missing domain name!" ;\
	    echo "usage: Make DOMAIN=normal.no [PREFIX=/srv/www/normal.no]" ;\
	    false ;\
	fi
	sed -e 's/@DOMAIN@/$(DOMAIN)/g' -e 's|@PREFIX@|$(PREFIX)|g' < $<
