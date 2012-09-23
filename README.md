# fantasy-ultimate

A fantasy Ultimate site based on the Leaguevine API

## Environment setup

### Python environments

If you are running Ubuntu or MacOS (?), python will be pre-installed. If you are running windows, you will have to install it yourself.

virtualenv is a very slick tool that is used to create sandboxed virtual python environments so that you can install a specific set of python packages without affecting your native python environment or any other virtual python environments. It is recommended that run in a virtual python environment, although this setup has not been tested on Windows.

### Non-python dependencies (Ubuntu >= 11.04)

On Ubuntu you can install all of the non-python dependencies by running:

    sudo apt-get install nginx mysql-server python-setuptools python-virtualenv python-dev python-mysqldb git-core build-essential

and then to ensure that you have a new enough version of pip (at least 1.1), run:

    sudo easy_install -U pip

### Non-python dependencies (MacOS)

THIS SECTION IS INCOMPLETE

You will need to install XCode and go into the Downloads preferences pane and ensure that the command-line tools are installed.

Next, install virtualenv by running:

    sudo pip install virtualenv

### Non-python dependencies (Windows)

Um, you're kind of on your own here...if you do get the environment up and running on windows, please keep track of what you need to do so we can include instructions here.

### Set up virtualenv

If you don't want to run in a virtualenv (even though it's highly recommended that you do), you can skip this section. In future sections where you are told to switch to the virtualenv, you can ignore that step. If you are not using a virtualenv, then anytime you need to install packages using pip, you will need to do so as root (sudo pip install ...).

First you'll want to install virtualenvwrapper, a set of extensions for virtualenv that will make your life much easier:

    sudo pip install virtualenvwrapper

Next, add the following line to your .bashrc:

    . /usr/local/bin/virtualenvwrapper.sh

and restart your shell. Now create your virtualenv (*not* as root, and *not* with sudo) by running:

    mkvirtualenv lvfu

'lvfu' is the name of your virtual environment -- you could name it whatever you like. Executing this command will create the virtual environment and set up your shell to use it -- you should see (lvfu) prepended to your command prompt, indicating that you are in the lvfu virtualenv. In the future when you spawn a new shell and want to start using the lvfu virtualenv, just execute:

    workon lvfu

### Install python dependencies

To install the project's python dependencies, first switch to your virtualenv (workon lvfu), then go to the root directory of the project and run:

    pip install -r requirements.txt

You do *not* need to (and should not) run this as root.

We keep requirements.txt up-to-date with all required dependencies, so this is all that's needed. If the dependencies change and you need to update, just run the above command again -- it will update all packages as needed.

### Set up database

To set up the MySQL database that Django will use, run:

    mysql -u root -p
    (enter password, which you can just leave blank if you like)

    mysql> create database lvfu;
    mysql> create user 'lvfu'@'localhost' identified by 'lvfu';
    mysql> grant all privileges on *.* to 'lvfu'@'localhost' with grant option;

    <ctrl-d> to exit

To test that the database and MySQLdb (the python -> MySQL connector) are set up properly, run the follow in your virtualenv:

    python
    >>> from MySQLdb import _mysql
    >>> db = _mysql.connect("localhost","lvfu","lvfu","lvfu")
    >>> <ctrl-d> to exit

You shouldn't expect any output, but if you can execute these two commands without any errors, then python can talk to you new MySQL database, and you should be ready to run Django.

### Configure Django

In the lvfu sub-directory of the project, you will find a file called local_settings.txt. This is where you put Django configuration values that are specific to your environment/setup. First, copy the file to local_settings.py, then edit it and modify any needed variables -- an explanation of each is included in comments in the file.

Next, tell Django to set up the database by switching to your virtualenv, going to the root of the project, and executing:

    ./manage.py syncdb

when prompted to create a super-user, choose whatever username and password you like. This will create a user account in Django's authentication system that you can use to access the administrative interface.

## Eclipse setup

If you plan to use eclipse as your editor, this section describes how to set it up to work with this project.

### Eclipse plugins

THIS SECTION MAY BE INCOMPLETE.

To install plugins in Eclipse, go to Help -> Install New Software, click add, enter the name and URL of the plugin repository, wait for the list of plugins to load, then select the desired plugin(s) and proceed. These are the plugins you'll want to install:

#### PyDev

This is a Python IDE for eclipse.

Repository URL: http://pydev.org/updates
Package: PyDev

#### AnyEdit

Everybody hates hard tabs, but it's very difficult to configure Eclipse to never use them. This is a clever plugin that processes files each time you save them and converts hard tabs to spaces.

Repository URL: http://andrei.gmxhome.de/eclipse/
Package: Eclipse 3.5 - 3.8 plugins --> AnyEditTools

Once installed, go to Window -> Preferences -> General -> Editors -> AnyEdit Tools. On the "Auto - Convert" tab, enable "Convert tabs <-> spaces" and select "Tabs to spaces". Then go to the Convert... tab and make sure the "Tab width/number of spaces for tab" value is set to 4.

NOTE: If you prefer, you can make these settings project specific by following the Project setup instructions below, and then modifying the "AnyEdit Tools" section of the project preferences instead of the global preferences described in the previous paragraph.

### Project setup

First, (if you are using a virtualenv), set up a python interpreter that uses the virtualenv:

* Window -> Preferences
* Go to PyDev -> Interpreter - Python
* Click the "New..." button on the top right
* Fill in 'lvfu' for the name
* Click the "Browse..." button next to the executable field
* Select <your home directory>/.virtualenvs/lvfu/bin/python
* Click "OK"
* Make sure all of the files under the .virtualenv directory are selected, and also that the /usr/lib/python<VERSION> files are selected.
* Click "OK"
* Click "OK"

Next, import the project into your workspace:

* File -> Import
* Choose "General -> ExistingProjects into Workspace"
* Choose "Select root directory"
* Click "Browse...", browse to the project's *parent* directory and hit OK
* Select the project from the "Projects:" list
* Click "Finish"

Now, configure the project to use the virtualenv Python interpreter:

* Right click on the project and choose Properties
* Go to "PyDev Interpreter/Grammar"
* In the "Interpreter" drop-down, choose "lvfu"
* Click OK
