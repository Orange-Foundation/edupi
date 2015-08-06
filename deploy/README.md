This [fabric](http://www.fabfile.org/) script helps to configure and deploy web projects on a Raspberry Pi.

## Usage

### Installation

We suppose that you have a clean [Raspbian](https://www.raspberrypi.org/downloads/) installed in your (micro-)SD card,
and you should have already expended the file system.

Also, your Raspberry pi should be in the same network as your local machine so that you can access it via SSH.
Then run this script on your own machine, so that it will deploy configuration files on your Raspberry.

Dependencies:


    $> pip install fabric

Clone the project on your local machine, go into the project directory and you are ready to go:


    $> git clone https://github.com/Orange-Foundation/edupi.git
    $> cd edupi/deploy


### Configure hotspot


Run the following command, then reboot your Raspberry.
You should see a new Hotspot created with a name started with `FONDATION_ORANGE`,
followed by seven characters that identify your server.
Replace the `RASPBERRY_IP` with it's real IP in your sub network.

    $> fab config_hotspot:host=pi@RASPBERRY_IP

If you want to change this name, modify the `SSID_PREFIX` in `sysconf/etc/rc.local` and re-run the command above.

### Install some dependencies

This command will install some dependencies for EduPi.

    $> fab install_deps:host=pi@RASPBERRY_IP

### Deploy EduPi

**Deploy**

If you want to deploy manually, see [this doc](../doc/deploy.md).

Below are the command that help to deploy automatically.

Before deploying Edupi, please ensure that you have Python3.4 installed in your rpi.
Checkout [how to install Python3.4](../doc/how-to.md).

Then you are ready to go:

    $> fab deploy_edupi:host=pi@RASPBERRY_IP

By default, the command above will install the latest release from the release branch on your Raspberry.

If you want to install any other version, you can get the commit SHA1 code from Github, and append to the command.
For example, `d9bdc37827cc360d618060ab8866a58572ca42da` is a commit for
[`v1.4.1`](https://github.com/Orange-Foundation/edupi/releases/tag/v1.4.1).
You can install it by running:

    $> fab deploy_edupi:host=pi@RASPBERRY_IP,commit=d9bdc37827cc360d618060ab8866a58572ca42da

or simply:

    $> fab deploy_edupi:host=pi@RASPBERRY_IP,commit=tags/v1.4.1

EduPi will run automatically after boot.


**Test it**

Connect a mobile device to the Pi's Hotspot,
open a browser and enter the URL: http://edupi.fondationorange.org:8021 to enter into the index page.

If you want to test it with your local machine which not only share the same network with your raspberry but also
has access to the outside Internet, you need to change your `hosts` file. On Linux, add the following line to `/etc/hosts`:

    RASPBERRY_IP fondationorange.org edupi.fondationorange.org

You can then use your browser to test it:

    Normal user   : http://edupi.fondationorange.org:8021/
    Administrator : http://edupi.fondationorange.org:8021/custom/

There is a default super user account created with this deployment script:

    user: pi
    password: raspberry

**For development**

If you have forked edupi, you can deploy with your code after you pushed that on your github.

    $> fab deploy_edupi:host=pi@RASPEBRRY_PI,commit=COMMIT_CODE,user=GITHUB_USER

In this case, please always add your username in the command.

## Uninstall EduPi

Remove edupi's configuration files and source, but not the data. Run:

    $> fab uninstall_edupi:host=pi@RASPBERRY_PI

If you want to remove all the EduPi data on your server:

    $> fab uninstall_edupi:host=pi@RASPBERRY_PI,purge_data=true
