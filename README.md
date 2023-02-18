# Pipeline status
- ![Main branch status](https://github.com/J3olchara/yandex_django/actions/workflows/python-package.yml/badge.svg?branch=main) - main
- ![Master branch status](https://github.com/J3olchara/yandex_django/actions/workflows/python-package.yml/badge.svg?branch=master) - master
- ![q3 branch status](https://github.com/J3olchara/yandex_django/actions/workflows/python-package.yml/badge.svg?branch=q3) - q3

# How to run it on windows
1. Clone this repo and prepare workplace
> - git clone https://github.com/J3olchara/yandex_django
> - cd yandex_django
> - python -m venv venv
> - venv\scripts\activate

2. Download application dependencies:
> - if you want to make some tests you need to run:
>
> python -m pip install -r requirements\test.txt
> - if you want to develop some features you need to run:
> 
> python -m pip install -r requirements\dev.txt
>
> - or if you want to run it in production you need to run:
>
> python -m pip install -r requirements\prod.txt

3. Get a secret variables for your application:
  > create .env file with example.env variables. 

Prevent third parties from getting values of your .env variables

4. finally run it by this command:
> python lyceum\manage.py runserver localhost:80

Then the application will start on http://localhost:80


# How to run in on Linux OS

1. Clone this repo and prepare workplace
  > - git clone https://github.com/J3olchara/yandex_django
  > - cd yandex_django
  > - python3 -m venv venv
  > - venv/bin/activate

2. Download application dependencies:
  > - if you want to make some tests you need to run:
  >
  > python3 -m pip3 install -r requirements/test.txt
  > - if you want to develop some features you need to run:
  > 
  > python3 -m pip3 install -r requirements/dev.txt
  >
  > - or if you want to run it in production you need to run:
  >
  > python3 -m pip3 install -r requirements/prod.txt

3. Get a secret variables for your application:
  > create .env file with example.env variables. 

Prevent third parties from getting values of your .env variables

4. finally run it by this command:
  > python3 lyceum/manage.py runserver localhost:80

Then the application will start on http://localhost:80
