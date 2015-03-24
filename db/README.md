
## SQLite database backend

SQLite requires write access to the directory containing the
database file (because writing lockfile). Therefor they both must
be writable by Apache's user (www-data).

    $ chown www-data:normalweb db
    $ chmod 770 db

And the user running 'manage.py syncdb' also needs write access. I use
the 'normalweb' group for that.

    $ django/manage.py syncdb

    $ chgrp normalweb normal.db 
    $ chmod g+w normal.db



## Protect the newmembers file!

    $ chown root:www-data newmembers
    $ chmod u=rw,g=w,o= newmembers	    # write-only for the apache user