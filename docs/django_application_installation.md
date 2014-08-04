### Django application installation


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

	python ./manage.py runserver
	
	
