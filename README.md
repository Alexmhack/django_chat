# django_chat
Creating a chatbot system using django2 and vue.js along with many modules.

**Start django project**

We will name our django project **chatire** you can name it whatever you want. The 
trailing **dot** at the end creates django project in the **current** folder.

```
django-admin startproject chatire .
```

Now ```migrate``` and ```createsuperuser```

```
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

# Authentication And User Management
Our project will have system for login and signing up users. This will be done by 
implementing a user and authentication management so users can create account and 
login.

Thanks to Django’s excellent and vibrant community, most of the work has been done 
for us. Hence we’re going to make use of a third-party django library called djoser

Install it using ```pip```

```
pip install djoser
pip install djangorestframework
```

[Djoser](http://djoser.readthedocs.io/) is a REST Implementation of Django’s inbuilt 
authentication system. So instead of forms and views that return html, it provides us 
with REST endpoints for user registration, token creation, user management etc.

## Configuring Djoser
We will be using djoser at the very basic level, there is a lot more that can be done 
with djoser. 

Configure our project for **djoser**

```
INSTALLED_APPS = [
    'django.contrib.admin',
    ...
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
]
```

Add **djoser urls** to ```urls.py```

```
# djoser urls
urlpatterns += [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
```

Now include the ```rest_framework.authentication.TokenAuthentication``` to **django rest frameword authentication classes**. Add this to the bottom of ```settings.py``` file.

```
# django rest frameworks authentication classes
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
    ),
}
```

Now we will try out the **djoser** endpoint.

Run the server using ```python manage.py runserver``` and in **git bash** or **terminal** type 

```
curl -X POST http://127.0.0.1:8000/auth/users/create/ --data "username=alexmhack&password=trydjango"
{"email":"","username":"alexmhack","id":2}
```

**NOTE:** If you get any errors saying ```password not recognized as internal 
command... then``` use double quotes in like this 
```"username=alexmhack&password=trydjango"```. Also don't forget to add ```/``` 
at the end of the url.

This command has created a new user, you can check the console where server is running...
```
[...] "POST /auth/users/create/ HTTP/1.1" 201 37
```

Alternatively you can use ```&email=``` field to give the username email also.

# Vue.js
We’ll make use of vue-cli to quickly create a Vue app ```(instead of the <script> tag method)```. This method allows us to leverage the full power of ES6+ and single file Vue components.

Install ```vue-cli``` using ```npm```

```
npm install -g vue-cli
```

Let's create a new project based on webpack template with vue-cli

```
vue init webpack chatire-frontend
```

This will download the webpack and ask for project details. Be sure to accept 
**install vue-router** option. And also **npm install** option. 

After the process completes run the dev server using

```
npm run dev
```

Locate to [localhost:8000](http://127.0.0.1:8000/)
