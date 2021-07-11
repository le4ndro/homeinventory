Home Inventory
==============

Home Inventory is a web application for keep track of your stuff.

Features
---------

* For Django 3.2
* Works with Python 3
* Twitter Bootstrap_ v4.0.0  - beta
* 12-Factor_ based settings via django-environ_
* Optimized development and production settings
* Customizable PostgreSQL version


.. _Bootstrap: https://github.com/twbs/bootstrap
.. _django-environ: https://github.com/joke2k/django-environ
.. _12-Factor: http://12factor.net/

Usage
------

First, clone the project::

  $ git clone https://github.com/le4ndro/homeinventory.git

It's better work with a virtual environment, so create one using virtualenv and activate it.

Install requirements for the project::

  $ cd homeinventory/
  $ pip install -r requirements/local.txt


Create database on postgresql::

  $ createdb homeinventory

Or use pgadmin

Create your environment file::

  $ cp env.example .env

Edit your .env file with your parameters

Now you can run migrations and run the application::

  $ python manage.py migrate
  $ python manage.py runserver

To create admin user::

  $ python manage.py createsuperuser
