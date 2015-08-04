# Document objectives

Some essential information for developers.


## Download, compile and install Python3.4 on a Debian like distribution (Debian, Raspbian)

- install sqlite first

        $> sudo apt-get install -y libsqlite3-dev

- get the source

        $> cd /tmp
        $> wget https://www.python.org/ftp/python/3.4.1/Python-3.4.1.tgz
        $> tar xvzf Python-3.4.1.tgz
        $> cd Python-3.4.1/

- configure, make, make install

        $> ./configure --prefix=/opt/python3.4         # this takes a little bit (~ 5 minutes)
        $> make                                        # this takes aaages (about an hour)
        $> sudo make install                           # this is rather quick again (~ 7 minutes)

- make a link

        $> sudo ln -s /opt/python3.4/bin/python3.4 /usr/bin/python3.4

- Test

        $> python3.4
        Python 3.4.1 (default, Jul 31 2015, 14:51:48)
        [GCC 4.6.3] on linux
        Type "help", "copyright", "credits" or "license" for more information.
        >>>


## How to make an EduPi release

The `master` is a development branch. The release is in the `release` branch.
To make a new release, we need the following steps:

- Checkout the `release` branch, and merge all new features from `master`.

- Change the js projects' version number in `cntapp/static/custom/src/main.js`
and `cntapp/static/final/src/main.js`, and `edupi/__init__`

- Compile js files, run from the source folder:

        $> r.js -o cntapp/static/cntapp/custom/src/app.build.js
        $> r.js -o cntapp/static/cntapp/final/src/app.build.js

- Run the test:

    (virtualenv)$> python manage.py test

- If all tests pass, then commit the changed files.

- Tag the current commit with a new version number and release:

        $> git tag -a vN.N.N
        $> git push origin vN.N.N

write the release notes when tagging.

Attention, do not merge the release branch into master.


## How to discover the IP address of the Raspberry Pi

By default, SSH is enabled on raspbian. On your linux machine, install nmap. Then run:

        $> nmap -p 22 --open -sV 192.168.1.0/24

change the network ip and the mask if necessary.
