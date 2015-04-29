[![Build Status](https://travis-ci.org/yuancheng2013/edupi.svg?branch=master)](https://travis-ci.org/yuancheng2013/edupi)
[![Coverage Status](https://coveralls.io/repos/yuancheng2013/edupi/badge.svg?branch=master)](https://coveralls.io/r/yuancheng2013/edupi?branch=master)

# Edupi

## What is it?
Edupi is a light-weight content management Web application.

## Getting started

* Prepare a neat directory

        $> mkdir ~/edupi-dev/
        $> cd ~/edupi-dev/

* Create a virtualenv

        $> virtualenv --python=python3 virtualenv
        $> source virtualenv/bin/activate

* Prepare directories

        $> mkdir static database media

* Get the code

        $> git clone https://github.com/yuancheng2013/edupi.git
        $> cd edupi

* Install MagicWand

        $> sudo apt-get install libmagickwand-dev

* Install required packages

    We assume that you have already `node.js`, `npm`, `bower` installed.

        $> pip install -r requirements.txt
        $> pip install -r requirements-dev.txt
        $> python manage.py bower install

* Apply migrations and run the application in development mode.

        $> python manage.py migrate
        $> python manage.py runserver
