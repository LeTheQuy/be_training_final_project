# Category App Backend system

## Short Description

This is BE system that provides some Restful API to serve Simple Category application. The application provides a list
of items within a variety of categories as well as provides a user registration and authentication system. Registered
users will have the ability to post, edit, and delete their own items.

More detail about DB design, API specs, project structure, Please
visit [here](https://docs.google.com/document/d/13WE0p50ecmviwt3JmI6BuaJbkb8jQMxjvuPZZ38LapA/edit#heading=h.vcozbswwqf8l)

Technical stack: Python, MySQL, Flask, SQLAlchemy, JWT, bcrypt, marshmallow

## Installation and Setup

Install [Python3.6+](https://www.python.org/downloads/) and [pip](https://pypi.python.org/pypi/pip)

Clone project:

    $ mkdir ~/category_app
    $ cd ~/category_app
    $ git clone git@github.com:LeTheQuy/be_training_final_project.git

Set up [Virtualenv](https://virtualenv.pypa.io/en/stable/):

    $ pip install virtualenv
    $ cd ~/category_app/be_training_final_project
    $ virtualenv env
    $ source ~/env/bin/activate

Install project dependencies:

    $ cd ~/be_training_final_project
    $ pip install -r requirements.txt

## Database Setup and Configuration

Install [mysql 5.7](https://dev.mysql.com/downloads/mysql/5.7.html) and run the server:

    $ mysql.server start

Create a local development database:

    $ mysql -u root
    mysql> create database be_training

Update local config file at

    $ cd ~/be_training/config/local.py

Run prepare dummy data for testing

    $ python prepare_data.py

## Launching BE API

    $ python run.py

## Testing

Setup test dependencies:

    $ pip install pytest
    $ pip install pytest-cov
    $ mysql -u root
    mysql> create database be_training_test;

Run the tests:

    $ ENV=test pytest test 

Run the tests with coverage information:

    $ ENV=test py.test test --cov=main