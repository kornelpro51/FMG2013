### Fetchmyguest application installation


Before, you install the application, make sure your system has

	memcached
	libmemcached
	libevent
	redis
	wget
	geos

Do this sequence of commands, clearly, python, virtualenv, git, and pip must be installed (Google for instructions) (Linux environment reccomended):

	virtualenv --distribute new_folder
	cd new_folder/
	source bin/activate

The last command activate the virtualenv

Then you want to clone the project in the new virtualenv folder:

	git clone git@github.com:vperez23/FMG2013.git@dev fetchmyguest

Install the requirements:

	cd fetchmyguest
	pip install -r requirements.txt


create a local database in postgresql named `fetch`

and generate the tables if you don't replicate the existing db

	python ./manage.py syncdb --all
	python ./manage.py migrate --fake

then you can run your local django server

	python ./manage.py supervisor


##### Important

This app requires the  H-store extension installed on PostgreSQL

    CREATE EXTENSION hstore;

From the database sql shell.

### Local settings

The configuration by default points to the production settings, if local develeopment settings are requred you should create a local settings file, in `*/settings/local.py` and configure a environment variable to point to this settings, typically in a virtualenv:
	
	...
	_OLD_VIRTUAL_PATH="$PATH"
	PATH="$VIRTUAL_ENV/bin:$PATH"
	export PATH
	export DJANGO_SETTINGS_MODULE='fetchmyguest.settings.local'
	
	# unset PYTHONHOME if set.
	...
	
This a `local.py` example:

	from dev import *
	
	RAVEN_CONFIG = {
	                'dsn': '',
	}
	BIND = "0.0.0.0:8080"

Important is to import `dev` `prod` or `base`, then everithing can overridden. 
