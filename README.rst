Customize the following to your project
=======================================

- Change ``strapless_web`` everywhere to whatever your project name should be.

- Rename the 2 strapless_web directories to your new project name. Simple ``mv``.

- Change the ``SECRET_KEY`` in the settings/base.py

- In Vagrantfile change:
    - the port mappings to something new / that doesn't conflict with anything else you have running locally.
    - the private_network ip address to something else that won't collide with other projects

- Put in ansible/dev the ip address you chose in Vagrantfile and also in ansible/staging whatever is the staging ip address.


Dev setup
=========

- Install Vagrant (if not already installed): http://www.vagrantup.com/downloads.html
- Install VirtualBox (if not already installed): https://www.virtualbox.org/
- Install Ansible (if not already installed): on OSX ideally via Homebrew ``brew update && brew install ansible``
- ``vagrant up``
- ``vagrant reload``
- ``vagrant ssh``
- ``cd /vagrant/strapless_web/ && python manage.py runserver 0.0.0.0:8000``
- Now open your browser and point to http://127.0.0.1:8004 to see the app running
- http://127.0.0.1:8084 should also run, thats through nginx and uwsgi that gets configured.
    - TODO: Might have to do ``sudo /etc/init.d/uwsgi restart`` since it doesn't auto start sometimes.


Deploying to AWS
================

- Add a "ansible/other_vars/aws.yml" file that has the AWS secrets (encrypted with Ansible vault). This file will need to be given to each developer who would like to deploy to AWS with a shared password/secret for it to work. Format of the file.
        ---
        aws_access_key: "***"
        aws_secret_key: "******"
- Change any AWS params in "group_vars/all" file like zone / instance sizes etc.
- Override any AWS params in the "env_vars/*" files like zone / instance sizes / branch name etc.



Coding guidelines / standards
=============================

- Order of imports: python -> django -> libraries -> our code. Thats the order to follow in the python files, with one newline in between each of them. Two newlines before starting any code after the imports.

- Tabs should map to "spaces" and 1 tab = 4 spaces. If using TextMate check the "Soft Tabs" option.

- If in a view or app python file *do not* do ``from models import BlahModel``... always do ``from app_name.models import BlahModel``. Also never do "from settings import STATIC_URL" always do ``from django.conf import settings`` and then access the specific variable via the ``settings`` object.
