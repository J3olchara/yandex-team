# Pipeline status
- ![Main branch status](https://github.com/J3olchara/yandex_django/actions/workflows/python-package.yml/badge.svg?branch=main) - main
- ![Master branch status](https://github.com/J3olchara/yandex_django/actions/workflows/python-package.yml/badge.svg?branch=master) - master
- ![q3 branch status](https://github.com/J3olchara/yandex_django/actions/workflows/python-package.yml/badge.svg?branch=q3) - q3

# How to run
To run this application in dev on windows you need to run:
- git clone https://github.com/J3olchara/yandex_django
- cd yandex_django
- python -m venv venv
- venv\scripts\activate


if you want to make some tests you need to run:
- python pip install -r requirements_test.txt

if you want to develop some features you need to run:
- python pip install -r requirements_dev.txt

or if you want to run it in production you need to run:
- python pip install -r requirements_prod.txt

Get a secret key for your application:
- create .env file with example.env variables. Come up with your own value for varibales. (!!! IMPORTANT !!!)

finally run it by this command:
- python lyceum\manage.py runserver localhost:80

Then the application will start on http://localhost:80