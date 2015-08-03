EduPi should be developed on a Unix Like system.
In this tutorial, we suppose that you are using a Linux distribution.


## Development environment

* OS: Ubuntu 14.04
* Python 3.4

I haven't tested but I think any Linux distribution with `Python3.4` should work.


## Getting started:

* Install MagicWand, this is necessary for image processing in EduPi.

        $> sudo apt-get install libmagickwand-dev

* Prepare a neat directory

        $> mkdir ~/edupi-dev/
        $> cd ~/edupi-dev/

* Create a virtualenv

        $> virtualenv --python=python3.4 virtualenv
        $> source virtualenv/bin/activate

        You might not have python3.4 installed on your Linux distribution.
        Check the `how-to.md` document for installing python3.4 on a Debian-like distribution.

* Prepare directories

        (virtualenv)$> mkdir static database media

* Get the code

        (virtualenv)$> git clone https://github.com/yuancheng2013/edupi.git
        (virtualenv)$> cd edupi

* Install required packages

    We assume that you have already `node.js`, `npm`, `bower` installed.

        (virtualenv)$> pip install -r requirements.txt
        (virtualenv)$> pip install -r requirements-dev.txt
        (virtualenv)$> python manage.py bower install


* Run the tests

        (virtualenv)$> python manage.py test

There are some functional tests that is based on FireFox,
so you might need a FireFox installed on your development machine if you want to test this part.


* Create database

        $> python manage.py migrate

* Collect static files

        $> python manage.py collectstatic

* Create a supper user, you need it to go into the admin page

        (virtualenv)$> python manage.py createsuperuser

* Run the application in development mode.

        (virtualenv)$> python manage.py runserver
        
* Open your browser and try to login into the custom 
page (it's also an admin page) with URL:  http://127.0.0.1:8000/custom/

Login with the account that you have previously created and have fun :)
