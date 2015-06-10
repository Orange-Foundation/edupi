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
