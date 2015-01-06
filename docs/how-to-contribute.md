<!--
http://git.normal.no/git/normal.no/tree/docs/how-to-contribute.md

See the Makefile for how to build and upload.

TODO:
rename getting-started.md?
url-namespace
html5. define browser support (lowest IE version)
css for <code>
more line-spacing?
-->

<!-- markdown don't touches stuff inside block tags, but head is not
a block tag, so it messes it up. Therefor we wrapp head inside a div
even tough it's not legal html -->
<div>
<meta charset="utf-8" />
<style type="text/css">
  pre {  /* box with code */
    background-color: rgb(238, 238, 238);
    border: 1px solid black;
    padding: 1ex;
    width: 52em;
  }
  p > code {    /* inline code */
    font-size: 90%;
    background-color: rgba(0,0,0,0.04);
    padding: 0.33em 0.1em;
    border-radius: 3px;
  }
  p { width: 50em; line-height: 1.44; }
  h2 { margin-top: 3ex; }
  div.toc {
    border: 1px dashed black;
    float: right;
    margin-right: 1em;
    padding-right: 1em;
  }
</style>
</div>


[TOC]

<!--
Hvordan komme i gang
====================
-->

_Sist oppdatert: @@LAST-UPDATE@@_

Denne guiden hjelper deg å komme i gang med å gjøre endringer i koden
eller designet til Normals nettsider – [normal.no](http://normal.no).

Er noe uklart ta kontakt med <mailto:torkel@normal.no> eller
<mailto:post@normal.no>.

Nettsiden bruker rammeverket [Django], er skrevet
i programmeringsspråket [Python] og bruker [SQLite] som database.

For å holde orden på alle filer – samt tilate at flere redigerer disse
samtidig – bruker vi et [versjonskontrollsystem][SCM] som kalles [Git][].

Denne guiden tar utgangspunkt i at du bruker Debian eller Ubuntu
GNU/Linux, men de samme prinsipper gjelder for Windows, Mac, eller andre
Linux-distribusjoner.

[Django]: https://www.djangoproject.com/
[Python]: http://www.python.org/
[SQLite]: http://sqlite.org/
[SCM]: http://no.wikipedia.org/wiki/Versjonskontrollsystem


## Innledning ##

Hvis du bare skal endre på designet (html-maler) virker nok denne guiden
noe overveldene, og du kan hoppe over punktene `Installasjon` og
`Django`, og du trenger strengt tatt ikke installere noe ekstra på
maskinen din – selv om Git annbefales på det varmeste! Git brukes for
å laste ned alle filene og sende endringer tilbake. Hvis du synes det
blir for knotete, kan også filene lastes ned her: [Html maler][];
[css, javascript og bilder][css-js-images].

[Html maler]: http://git.normal.no/git/normal.no/tree/django/templates
[css-js-images]: http://git.normal.no/git/normal.no/tree/django/static

Hvis du ikke kan programmere eller ikke har noe erfaring med Python eller
webutvikling, burde du kanskje heller finne noe annet å bidra med. Hvis
du derimot er teknisk annlagt, lærer fort og brenner for oppgaven; sjekk
ut denne videoen:
[Python Web Development: Understanding Django for Beginners](http://www.youtube.com/watch?v=zTNA0MtZwso).

Skal du bare gjøre endringer i innhold (tekst og bilder), er ikke dette
guiden for deg. Det gjøres via admin-grensesnittet her:
<http://normal.no/admin/>


## Installasjon ##


### Windows ###

Windows er jo så lett å bruke så dette klarer du helt sikkert selv :)

* [GIT for Windows](http://msysgit.github.io/)
* [Python for Windows](https://www.python.org/downloads/windows/)
* [Django for Windows](https://docs.djangoproject.com/en/1.7/howto/windows/)
* [Video: How to install Django in Windows 7](http://www.youtube.com/watch?v=rIVwVOpwpsA)

Og hvis du får det til, skriv gjerne ned en oppskrift for andre.


### Linux/Unix ###

Start terminalprogrammet og lim inn kommandoene under.

Først må du installere noen programmer (pakker) som prosjektet trenger
for å fungere. Dette må gjøres som administrator (root).

    apt-get install python-pip
    apt-get install sqlite3
    apt-get install git

Django kan installeres både som administrator (root) og som en vanlig
bruker.  Installerer du som vanlig bruker, installeres alle filene under
katalogen `$HOME/.local/`. Derfor må `$HOME/.local/bin/` legges til
i `PATH` for at komandoen `django-admin.py` skal virke (ikke nødvendig).
Det enkleste er å installere som administrator, og det gjør du slik:

    pip install django

Nettsiden bruker følgende Python-moduler. De installeres slik:

    pip install pillow
    pip install markdown

Resten burde gjøres som din vanlige bruker – eller hvis du er paranoid,
lag en egen bruker kun for dette.


### Last ned kildekoden ###

Neste steg er å laste ned kildekoden til nettsidene. Til det bruker vi
et versjonskontroll-system ved navn [Git][]. Git gjør det bl.a. mulig
for flere personer å redigere de samme filene samtidig.

[Git]: http://en.wikipedia.org/wiki/Git_(software)

Still deg i den mappen du vil laste ned i. I dette eksemplet har jeg
valgt hjemmemappen min, dvs. `/home/torkel/`. Dit kommer jeg ved
å skrive `cd $HOME`.

    git clone http://git.normal.no/git/normal.no
    cd normal.no
    git submodule init
    git submodule update

Du har nå lastet ned alle filene og står i mappen til prosjektet.
Hos meg blir det `/home/torkel/normal.no/`.


### Konfigurer / oppsett ###

Sjekk at standard konfigurasjonen er ok:

    edit django/website/settings.py

Så trenger du en databasefil med testdata:

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



## Gjøre endringer ##

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
eller <post@normal.no> med en kort beskrivelse (med mindre de er
selvforklarende).

Dette kan gjøres fra kommandolinja:

    git diff | mail torkel@normal.no -s 'beskriv endringen din her'

Eller ennå bedre; lær deg Git og be oss om skrivetilgang.

* <http://rogerdudler.github.io/git-guide/>
* <http://stackoverflow.com/questions/315911/git-for-beginners-the-definitive-practical-guide>
* <http://git-scm.com/book>

**Send en nyttig patch eller to, og vi gir deg skrivetilgang.**
