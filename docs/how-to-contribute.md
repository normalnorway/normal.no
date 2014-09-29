<!--
http://git.normal.no/git/normal.no/tree/docs/how-to-contribute.md

See the Makefile for how to build and upload.

rename getting-started.md ?

TODO:
Python Web Development: Understanding Django for Beginners
http://www.youtube.com/watch?v=zTNA0MtZwso
Kan du ikke python, eller har veldig lyst til å lære => kanskje
heller finne noe annet å gjøre? :) [bidra med]
-->

<meta charset="utf-8" />
<style type="text/css">
  pre {
    background-color: rgb(238, 238, 238);
    border: 1px solid black;
    padding: 1ex;
    width: 52em;
  }
  p { width: 50em; }
  h2 { margin-top: 3ex; }
</style>


Hvordan komme i gang
====================

_Sist oppdatert: @@LAST-UPDATE@@_

Er noe uklart ta kontakt med <mailto:mikal@normal.no> eller
<mailto:torkel@normal.no>.

Nettsiden er laget i rammeverket [Django], er skrevet i [Python] og bruker
[SQLite] som database.

Denne guiden tar utgangspunkt i at du bruker Debian eller Ubuntu GNU/Linux.

[Django]: https://www.djangoproject.com/
[Python]: http://www.python.org/
[SQLite]: http://sqlite.org/


## Installasjon ##


### Windows ###

Windows er jo så lett å bruke så dette klarer du helt sikkert selv :)

* <http://www.python.org/getit/windows/>
* <https://code.djangoproject.com/wiki/WindowsInstall>
* <http://www.youtube.com/watch?v=rIVwVOpwpsA>
* <http://msysgit.github.io/>

Og hvis du får det til, skriv gjerne ned en oppskrift for andre.


### Linux/Unix ###

Start terminalprogrammet og lim inn kommandoene under.

Først må du installere noen programmer (pakker) som prosjektet trenger
for å fungere. Dette må gjøres som administrator (root).

    apt-get install python-pip
    apt-get install sqlite3
    apt-get install git

    pip install pillow

Django kan installeres både som root og som en vanlig bruker.
Installerer du som vanlig bruker, legger alt seg under $HOME/.local og
$HOME/.local/bin/ må legges til i PATH for at komandoen django-admin.py
skal virke (valgfritt).

    pip install django

Nettsiden bruker følgende Python-moduler. De må installeres:

    pip install markdown

Resten burde gjøres som din vanlige bruker – eller hvis du er paranoid,
lag en egen bruker kun for dette.

#### Last ned kildekoden ####

Neste steg er å laste ned kildekoden til nettsidene. Til det bruker vi
et versjonskontroll-system ved navn [Git][]. Git gjør det bl.a. mulig
for flere personer å redigere de samme filene samtidig.

[Git]: http://en.wikipedia.org/wiki/Git_(software)

Still deg i den mappen du vil laste ned i. I dette eksemplet har jeg
valgt hjemmemappen min, dvs. `/home/torkel/`. Dit kommer jeg ved
å skrive `cd $HOME`.

    git clone http://git.normal.no/git/normal.no
    cd normal.no

Du har nå lastet ned alle filene og står i (root) mappen til prosjektet.
Hos meg blir det `/home/torkel/normal.no/`.

#### Konfigurer / oppsett ####

Sjekk at standard konfigurasjonen er ok:

    edit django/website/settings.py

Så trenger du en databasefil med noen testdata:

    cd db
    wget http://torkel.normal.no/normal.db

Siste steg er å lage deg en bruker så du får logget inn:

    python django/manage.py createsuperuser



## Django ##

Django kommer med en innebygget webserver man kan bruke under utvikling.
Den oppdager hvilke filer som blir redigert og laster de automatisk inn
på nytt.

Django's webserver starter du slik:

    python django/manage.py runserver

(Du må stå i katalogen som inneholder filen `manage.py`; som er
`/home/torkel/normal.no/` i mitt tilfelle.)

Webserveren lytter på localhost:8000 så nå er det bare å åpne [den
adressen i nettleseren](http://localhost:8000/).  
Administrasjons-panelet finner du her: <http://localhost:8000/admin>.

Eventuelt prøv denne kommandoen:

    xdg-open http://localhost:8000/



## Gjøre endringer i koden ##

Sett at du skal gjøre en liten endringen i html-malen til
nettguiden. Da redigerer du denne filen `django/templates/nettguide.html`.

Når du er ferdig bruk `git diff` for å vise hvilke endringer som er gjort:

    git diff

    --- i/django/templates/nettguide.html
    +++ w/django/templates/nettguide.html
    -<p>Send ditt forslag her: TODO</p>
    +<p>Vennligst send ditt forslag til <a href="mailto:webmaster@normal.no">
    +webmaster@normal.no</a>.</p>

Linjer som starter med '-' er fjernet, og linjer som starter med '+' er
lagt til.

Du kan også bruke `git status` for å se _hvilke_ filer som er endret.

Hvis du angrer på endringene du har gjort i en fil, kan den
tilbakestilles slik:

    git checkout django/templates/nettguide.html

TODO: Forklare mer om hvordan GIT fungerer.

<!--
git add docs/how-to-contribute.md docs/Makefile
git diff &ndash;&ndash;staged
-->


## Hvordan sende endringer? ##

Du har gjort noen endringer i koden, og du ønsker å sende de til oss.
Den enkleste måten å gjøre det på, er å kjøre kommandoen `git diff` og
sende oss teksten den genererer. Dette er nemmelig en "oppskrift"
(patch) for endringene dine.

    cd /home/torkel/normal.no
    git diff > min-endring.patch

Så sender du filen `min-endring.patch` til <mailto:torkel@normal.no>
eller <mikal@normal.no> med en kort beskrivelse (med mindre de er
selvforklarende).

Dette kan gjøres fra kommandolinja:

    git diff | mail torkel@normal.no -s 'beskriv endringen din her'

Eller ennå bedre; lær deg Git og be oss om skrivetilgang.

* <http://rogerdudler.github.io/git-guide/>
* <http://stackoverflow.com/questions/315911/git-for-beginners-the-definitive-practical-guide>
* <http://git-scm.com/book>

**Send en nyttig patch eller to, og vi gir deg skrivetilgang.**
