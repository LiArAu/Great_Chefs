# Great Chefs

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/Django.svg)
![PyPI - Django Version](https://img.shields.io/pypi/djversions/djangorestframework.svg)
![PyPI - Status](https://img.shields.io/pypi/status/Django.svg)


<!-- 
<p align="center">
  <img src="./home.png" width=700 height=400 />
  <br><br><br>
  <img src="./detail.png" width=600 height=400 />
</p> -->

## ⚡ Features

🎯 **Multiple Login Choices** - You can sign up for a new account and log in, or simply use your google account to log in.

🎯 **New Creation** - You can create new recipes.

🎯 **Latest News First** - In the home page, recipes were ranked by publishing time so that you can read the latest one first.

🎯 **Search Recipe** - You can search interested recipe.

🎯 **Personal Collections** - You can have your own collection page.



## 🚀 Setup

These instructions will get you a copy of the project up and running on your local machine for deployement and development.

You'll need [Git](https://git-scm.com) and [Python 3.8+](https://www.python.org/downloads/) installed on your local computer.

```
python@3.8 or higher
git@2.17.1 or higher
```

## 🔧 How To Use

From your command line, clone and deploy:

```bash
# Clone this repository
$ git clone https://github.com/LiArAu/Great-Chefs

# Go into the repository
$ cd Great-Chefs
```

## 🛠️ Django Setup

After installing the requirements, we'll need to setup some Django commands.

### Perform database migration:

```bash
python manage.py check
python manage.py migrate
```

### Create Admin Account

> This is the admin account and only this user can login. You can manage recipe categories, publishers and readers as the superuser.

```bash
python manage.py createsuperuser
# follow instruction
```

### Create Staff Account

> You can create a group inside admin and make new staff users members in it. Not giving permissions by default is a security feature.

### Run Development Server

```bash
python manage.py runserver
```

Navigate to [http://127.0.0.1:8000/](http://127.0.0.1:8000/) endpoint in your browser.

Admin endpoint is at http://127.0.0.1:8000/admin/

#### Designed & Developed by [Yajing Li](https://www.github.com/LiArAu)

## Contribute
Found a bug, please [create an issue](https://github.com/LiArAu/Great-Chefs/issues)
