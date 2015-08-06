For the moment, there is no bash script for installing EduPi on a Raspberry Pi.

You can install it via SSH and fabric.
Please checkout [`deploy`](../deploy/README.md) for how to deploy EduPi automatically on your Raspberry Pi.

Here is a detailed process for installing on a Raspbian, which is in fact the same as the fabric script.
It may take about 2 hours starting with a clean Raspbian.

It's highly recommended to read this doc for trouble shooting.


## Install EduPi dependencies

This would be a long process.

**Common packages**

```
$> sudo apt-get update
$> sudo apt-get install nginx python3-pip upstart libmagickwand-dev
$> sudo pip-3.2 install virtualenv
```

**nodejs, bower**

```
$> wget http://node-arm.herokuapp.com/node_latest_armhf.deb --directory-prefix=/tmp/
$> sudo dpkg -i /tmp/node_latest_armhf.deb
$> curl -L https://www.npmjs.com/install.sh | sudo sh
$> sudo npm install -g bower
```

**Python 3.4**

EduPi only works on Python 3.4 or version later.
However, the raspbian `2015-05-05-raspbian-wheezy.img` only has Python 3.2, so you cannot install it via
`sudo apt-get install python3`

Please checkout how to install Python 3.4 [here](how-to.md#download-compile-and-install-python34-on-a-debian-like-distribution-debian-raspbian).

## Install EduPi

1. Create directories.

    ```
    $> mkdir -p /home/pi/sites/edupi.fondationorange.org
    $> cd /home/pi/sites/edupi.fondationorange.org
    $> mkdir database static media stats virtualenv
    ```

2. Create virtualenv.

    ```
    $> virtualenv --python=python3.4 virtualenv/
    ```

3. Get the latest release.

    ```
    $> git clone https://github.com/yuancheng2013/edupi.git
    $> cd edupi
    $> git reset --hard origin/release
    ```

    Checkout the all releases [here](https://github.com/yuancheng2013/edupi/releases).
    You can replace `origin/release` by a specific commit SHA1 code.

4. Update virtualenv, front-end packages, and database.

    ```
    $> ../virtualenv/bin/pip install -r requirements.txt
    $> ../virtualenv/bin/python3 manage.py bower install
    ```

5. Create super user.

    ```
    $> ../virtualenv/bin/python manage.py createsuperuser
    ```

6. Update static files.

    ```
    $> ../virtualenv/bin/python3 manage.py collectstatic --noinput
    ```

### EduPi Configuration

1. Nginx config

    create file `/etc/nginx/sites-enabled/edupi.fondationorange.org`:

    ```
    $> sudo vi /etc/nginx/sites-enabled/edupi.fondationorange.org
    ```

    and paste:

    ```
    server {
        listen 8021;
        server_name edupi.fondationorange.org;
        client_max_body_size 500M;
        location /static {
            alias /home/pi/sites/edupi.fondationorange.org/static;
        }
        location /media {
            access_log /var/log/nginx/edupi_media_access.log;
            alias /home/pi/sites/edupi.fondationorange.org/media;
        }
        location / {
            proxy_pass http://unix:/tmp/edupi.fondationorange.org.socket;
            proxy_read_timeout 300;
            proxy_set_header Host $host:$server_port;
        }
    }
    ```

    To `start`, `stop`, `restart` nginx, please use nginx service:

    ```
    $> sudo service nginx start
    $> sudo service nginx stop
    $> sudo service nginx restart
    ```

2. Nginx logrotate config

    Edit file `/etc/logrotate.d/nginx`:

    ```
    $> sudo vi /etc/logrotate.d/nginx
    ```

    Replace `create 0640 www-data adm` by `create 0644 www-data adm`

3. Autostart with `Upstart`

    Edit file `/etc/init/gunicorn-edupi.fondationorange.org.conf`

    ```
    $> sudo vi /etc/init/gunicorn-edupi.fondationorange.org.conf
    ```

    and paste:
    
    ```
    description "Gunicorn server for edupi.fondationorange.org"
    start on net-device-up
    stop on shutdown
    respawn
    setuid pi
    chdir /home/pi/sites/edupi.fondationorange.org/edupi
    env LANG=en_US.UTF-8
    env LC_ALL=en_GB.UTF-8
    exec ../virtualenv/bin/gunicorn --bind unix:/tmp/edupi.fondationorange.org.socket\
     edupi.wsgi:application \
     --timeout=120 --graceful-timeout=10 \
     --log-level info
    ```

    The application will run when you reboot the system.

    To `start`, `stop`, and `restart` the service:

    ```
    $> sudo start gunicorn-edupi.fondationorange.org
    $> sudo stop gunicorn-edupi.fondationorange.org
    $> sudo restart gunicorn-edupi.fondationorange.org
    ```

4. run edupi server

    ```
    $> sudo service restart nginx
    $> sudo start gunicorn-edupi.fondationorange.org
    ```

5. test

    config your machine's hosts file `/etc/hosts/`
    
    add rule:

    `RASPBERRY_IP   edupi.fondationorange.org`

    Start your usage with `http://edupi.fondationorange.org:8021/`

6. log files

    * `/var/log/nginx/access.log` for nginx access log.
    * `/var/log/nginx/edupi_media_access.log` for media files' access.
    * `/var/log/upstart/gunicorn-edupi.fondationorange.org.log` for gunicorn log.
    You should search edupi server crush in this log file.
    * `/home/pi/sites/edupi.fondationorange.org/edupi/logfile` for edupi logger.
