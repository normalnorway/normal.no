<!--
TODO:
@deb node-less to regenerate css files (add to docs/install also)
can make changes directly on github
url-namespace. can link to wiki
html5. define browser support (lowest IE version)
coding standards
  Python 2.6 and Django 1.6 only! :(
rename CONTRIBUTING.md?
Github: Howto clone the repo and send pull requests
Github: Howto use the issue tracker
gitk / gitg
unit test: ./manage.py test
http://effectivedjango.com/

TODO Styling:
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
    padding-right: 1em;
  }
</style>
</div>


[TOC]

<!--
Hvordan komme i gang
====================
-->

_Sist oppdatert: @@DATE@@_

**Denne guiden hjelper deg å komme i gang med å gjøre endringer i koden
eller designet til Normals nettsider – [normal.no](http://normal.no).**

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

Hvis du kun skal endre designet (html- og css-maler) virker nok denne
guiden noe overveldene, og du kan hoppe over punktene `Installasjon` og
`Django`, og du trenger ikke å installere noe ekstra på
maskinen din – selv om Git annbefales på det varmeste! Git brukes for
å laste ned alle filene og sende endringer tilbake. Hvis du synes det
blir for knotete, kan også filene lastes ned her: [Html maler][];
[css,javascript og bilder][css-js-images].

[Html maler]: https://github.com/normalnorway/normal.no/tree/master/django/templates
[css-js-images]: https://github.com/normalnorway/normal.no/tree/master/django/static

Hvis du ikke kan programmere eller ikke har noe erfaring med Python eller
webutvikling, burde du kanskje heller finne noe annet å bidra med. Hvis
du derimot er teknisk annlagt, lærer fort, og brenner for oppgaven; sjekk
ut denne videoen:
[Python Web Development: Understanding Django for Beginners](http://www.youtube.com/watch?v=zTNA0MtZwso).

Skal du bare gjøre endringer i innhold (tekst og bilder), er ikke dette
guiden for deg. Slike endringer gjøres via admin-grensesnittet:
<https://normal.no/admin/>


## Installasjon ##


### Windows ###

Forfatter har ikke tilgang til Windows, så her må du klare deg selv. Men
det burde være grei skuring. Hvis du setter opp på Windows så bidra
gjerne til denne guiden ved å skrive ned hvordan du gjorde det. Her er
noen lenker som hjelper deg på vei:

* [GIT for Windows](http://msysgit.github.io/)
* [Python for Windows](https://www.python.org/downloads/windows/)
* [Django for Windows](https://docs.djangoproject.com/en/dev/howto/windows/)
* [Video: How to install Django in Windows 7](http://www.youtube.com/watch?v=rIVwVOpwpsA)


### Mac / OSX ###

Apple sitt operativsystem er Unix-basert, så se seksjonen under. Men
istedenfor å bruke `apt-get` for å installere pakker (programmer) kan du
bruke [Homebrew](http://brew.sh/).


### Linux/Unix ###

*Start et terminalprogram og lim inn kommandoene under.*

Først må du installere noen programmer (pakker) som prosjektet trenger
for å fungere. Dette må gjøres som administrator (root).

    sudo apt-get install git
    sudo apt-get install python-pip
    sudo apt-get install sqlite3

Så må du installere Python pakkene som prosjektet bruker. Disse finnes
som system-pakker som kan installeres med `apt-get`, men det er bedre
å installere disse via [Python Package Index](https://pypi.python.org/pypi)
fordi da får du aller siste versjon. Man bruker programmet `pip` for
å installere Python pakker.

Pyton pakker kan installeres både som administrator (root) og som en
vanlig bruker. Installerer du som vanlig bruker (anbefales), installeres
alle filene i `$HOME/.local/`, og vil kun være tilgengelig for din
bruker. (`pip` installerer som administrator som standard, så du må bruke
`pip --user` for å installere som egen bruker.)

<!--
    $ mkdir -p $HOME/.pip
    $ echo -e "[install]\nuser = yes" >> $HOME/.pip/pip.conf
-->

<!--
Django kan installeres både som administrator (root) og som en vanlig
bruker. Installerer du som vanlig bruker, installeres alle filene under
katalogen `$HOME/.local/`. Derfor må `$HOME/.local/bin/` legges til
i `PATH` for at komandoen `django-admin.py` skal virke (ikke nødvendig).
Det enkleste er å installere som administrator, og det gjør du slik:
-->

<!--
Resten burde gjøres som din vanlige bruker – eller hvis du er paranoid,
lag en egen bruker kun for dette.
-->

Nettsiden bruker følgende Python-pakker. De installeres slik:

    pip install --user django
    pip install --user pillow
    pip install --user markdown

<!-- @todo mark with css class. how? -->
Merk: Får du beskjeden «Requirement already satisfied (use --upgrade to
upgrade): ...», betyr det at pakken alt er installert som en
system-pakke. Du kan oppgradere den hvis du vil, men det er valgfritt.


### Last ned kildekoden ###

Neste steg er å laste ned kildekoden til nettsidene. Til det bruker vi
versjonskontroll-systemet [Git][]. Git gjør det bl.a. mulig for flere
personer å redigere de samme filene samtidig.

[Git]: http://en.wikipedia.org/wiki/Git_(software)

Still deg i mappen du vil laste ned i. I dette eksemplet har jeg valgt
hjemmemappen min, dvs. `/home/torkel/`. Dit kommer jeg ved å skrive `cd`.

    git clone https://github.com/normalnorway/normal.no.git
    cd normal.no
    sh bootstrap.sh

Alle filer som trengs er nå lastet ned og du står nå i mappen til
prosjektet. Hos meg blir det `/home/torkel/normal.no/`.


### Konfigurer / oppsett ###

For å sjekke at alt er i orden kan du kjøre denne kommandoen:

    python django/manage.py check

<!--
Sjekk at standard konfigurasjonen er ok:

    edit django/website/settings.py

Så trenger du en databasefil med testdata:

    cd db
    wget http://torkel.normal.no/normal.db
-->

Hvis du vil logge inn i admin-systemet må du først lage deg en bruker:

    python django/manage.py createsuperuser



## Django ##

Django kommer med en innebygget webserver man kan bruke under utvikling.
Den oppdager når filer blir redigert og laster de automatisk inn på nytt.

Django's webserver starter du slik:

    python django/manage.py runserver

Webserveren lytter på <http://localhost:8000>. Administrasjons-panelet
finner du her: <http://localhost:8000/admin>.

<!--
Eventuelt prøv denne kommandoen:

    xdg-open http://localhost:8000/
-->



## Hvordan gjøre endringer (Hvordan bruke Git) ##

Sett at du skal gjøre en liten endringen i html-malen til
nettguiden. Da redigerer du denne filen `django/templates/nettguide.html`.

Når du er ferdig bruk `git diff` for å se endringene som er gjort
(ikke nødvendig, men en god rutine):

    git diff

    --- i/django/templates/nettguide.html
    +++ w/django/templates/nettguide.html
    -<p>Send ditt forslag her: TODO</p>
    +<p>Vennligst send ditt forslag til <a href="mailto:webmaster@normal.no">
    +webmaster@normal.no</a>.</p>

Linjer som starter med '-' er fjernet, og linjer som starter med '+' er
lagt til.

Du kan også bruke `git status` for å se _hvilke_ filer som er endret:

    git status

    # On branch master
    # Changes not staged for commit:
    #   (use "git add <file>..." to update what will be committed)
    #   (use "git checkout -- <file>..." to discard changes in working directory)
    #
    #       modified:   django/templates/menu.html
    #       modified:   django/templates/support/petition.html
    #       modified:   docs/how-to-contribute.md


Hvis du angrer på endringene du har gjort i en fil, kan filen
tilbakestilles slik:

    git checkout django/templates/nettguide.html


Lær mer om Git:

* [git - the simple guide](http://rogerdudler.github.io/git-guide/)
* [Git for Beginners](http://www.sitepoint.com/git-for-beginners/)
* [Got 15 minutes and want to learn Git?](https://try.github.io/)
* [The Git Book](http://git-scm.com/book/en/v2)

[Grafiske Git-klienter](http://git-scm.com/downloads/guis)


## Hvordan sende endringer? ##

**Oppdatering: Bruk heller Github for å sende endringer. Det er enklere.
Se avsnittet under.**

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

<!--
* <http://rogerdudler.github.io/git-guide/>
* <http://stackoverflow.com/questions/315911/git-for-beginners-the-definitive-practical-guide>
* <http://git-scm.com/book>
-->

**Send en nyttig patch eller to, og vi gir deg skrivetilgang.**



## Github ##

[Github](https://github.com/) har et web-basert grensesnitt til Git,
wiki-sider og bugtracker. Tjenesten er gratis så lenge innholdet er
tilgjengelig for alle.

*Merk: Dette er ikke testet ut ennå.*

* Registrer deg en Github-konto: <https://github.com/join>
* Gå til <https://github.com/normalnorway/normal.no>
* Klikk på «Fork» øverst til høyre. (Lag din egen private kopi).
* Gjør én eller flere endringer
* Når du er fornøyd med en endring sender du en «Pull Request».


<!--
Hvis du blir en aktiv bidragsyter, gir vi deg gjerne skrivetilgang.

https://docs.djangoproject.com/en/dev/internals/contributing/writing-code/working-with-git/

How to Get Started with Github - Beginner Tutorial
https://www.youtube.com/watch?v=73I5dRucCds
Part 1 :: GitHub for Windows
https://www.youtube.com/watch?v=1UiICgvrsFI
-->
