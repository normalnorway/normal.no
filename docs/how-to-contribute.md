<!--
http://git.normal.no/git/normal.no/tree/docs/how-to-contribute.md

Se the Makefile for how to build and upload.

rename getting-started.md ?
-->

<style type="text/css">
  pre {
    background-color: rgb(238, 238, 238);
    border: 1px solid black;
    padding: 1ex;
    width: 52em;
    /*
    width: auto;
    */
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

Denne guiden tar utgangspunkt i at du bruker et Debian eller Ubuntu
GNU/Linux system.

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

Start et terminalprogram slik at du kan lime inn kommandoene under.

Først må du installere noen programmer (pakker) som prosjektet trenger
for å fungere. Dette må gjøres som administrator (root).

    apt-get install python-imaging
    apt-get install python-pip
    apt-get install sqlite3
    apt-get install git

Django kan installeres både som root og som en vanlig bruker.
Installerer du som vanlig bruker, legger alt seg under $HOME/.local og
$HOME/.local/bin/ må legges til i PATH for at komandoen django-admin.py
skal virke.

    pip install django

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

Legg inn en standard konfigurasjonsfil:

    cp conf/settings_local.py-dist django/website/settings_local.py

Så trenger du en databasefil med noen testdata:

    wget http://torkel.normal.no/normal.db

Siste steg er å lage deg en bruker så du får logget inn:

    python django/manage.py createsuperuser



## Starte og bruke Django ##

Django inneholder en egen webserver man kan bruke for utvikling. Den er
så «smart» at det merker når du har redigert én eller flere filer
og laster de da automatisk inn på nytt. Så det er veldig sjelden du
trenger å restarte Django.

Django starter du slik:

    python django/manage.py runserver

(Dette innebærer at du står i katalogen `/home/torkel/normal.no/`)

Så er det bare å gå til denne adresse i nettleseren din
<http://localhost:8000/>. Administrasjons-panelet finner du på denne
adressen <http://localhost:8000/admin>.

Hvis du ikke ønsker å røre musa, gjør disse to kommandoene høyst
sannsynlig jobben :)

    xdg-open http://localhost:8000/
    xdg-open http://localhost:8000/admin



## Gjøre endringer i koden ##

Sett at du skal gjøre en liten endringen i html templaten til
nettguiden. Da redigerer du denne filen `django/templates/nettguide.html`.

For å se hvilke endringer du har gjort, bruk `git diff`:

    git diff

    --- i/django/templates/nettguide.html
    +++ w/django/templates/nettguide.html
    -<p>Send ditt forslag her: TODO</p>
    +<p>Vennligst send ditt forslag til <a href="mailto:webmaster@normal.no">
    +webmaster@normal.no</a>.</p>

Linjer som starter med '-' er fjærnet og de som starter med '+' er lagt
til.

Man kan også bruke `git status` for å se hvilke filer som er endret.

Sett at jeg angrer på endringen jeg gjorde i nettguiden over. Da kan jeg
tilbakestille filen slik:

    git checkout django/templates/nettguide.html

TODO: Forklare mer om hvordan GIT fungerer.

<!--
git add docs/how-to-contribute.md docs/Makefile
git diff &ndash;&ndash;staged
-->


## Hvordan sende endringer? ##

Sett at du har gjort noen endringer i koden du ønsker å sende tilbake
til NORMAL. Den enkleste måten å gjøre dette på er å sende oss det
`git diff` viser. Dette er nemmelig en "oppskrift" (patch) for
endringene dine.

Først må du stille deg i root-mappen for prosjektet. Så kjører du `git
diff` og sender output til en fil:

    cd /path/to/normal.no
    git diff > min-endring.patch

Så kan du sende filen `min-endring.patch` til <mailto:mikal@normal.no>
eller <torkel@normal.no> med en kort beskrivelse.

Eller for de som har lært seg å bruke kommandolinja:

    git diff | mail torkel@normal.no -s 'beskriv endringen din her'

Eller ennå bedre; lær deg Git:

* <http://rogerdudler.github.io/git-guide/>
* <http://stackoverflow.com/questions/315911/git-for-beginners-the-definitive-practical-guide>

**Send en nyttig patch eller to, og vi gir deg skrivetilgang.**
