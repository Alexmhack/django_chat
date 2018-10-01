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

For more details on this project visit this [link](https://danidee10.github.io/2018/01/01/realtime-django-1.html)

vue-cli also sets up hotreloading for us which really improves the developer’s 
experience. As soon as you hit save after editing a component, the change is 
immediately reflected in the browser.

# Configure Vue Router
Create two components inside **chatire-frontend/src/components** folder. One will we ```Chat.vue``` for showing the chat screen and the other is ```UserAuth.vue``` that will be shown to unauthenticated users for login and sign up.

Edit the ```chatire-frontend/src/router/index.js``` file and add

```
import Vue from 'vue'
import Router from 'vue-router'
import Chat from '@/components/Chat'
import UserAuth from '@/components/UserAuth'

Vue.use(Router)

const router = new Router({
  routes: [
    {
      path: '/chats',
      name: 'Chat',
      component: Chat
    },

    {
      path: '/auth',
      name: 'UserAuth',
      component: UserAuth
    }
  ]
})

router.beforeEach((to, from, next) => {
  if (sessionStorage.getItem('authToken') !== null || to.path === '/auth') {
    next()
  }
  else {
    next('/auth')
  }
})

export default router
```

The beforeEach guard is called before a navigating to any route in our application.

If a token is stored in the sessionStorage we allow the navigation to proceed by 
calling next() else we redirect to the auth component.

No matter the route a user navigates to in our application this function will check 
if the user has an auth token and redirect them appropraitely.

# Login / Signup Template
Add the below piece of code in ```UseAuth.vue```

```
<template>
  <div class="container">
    <h1 class="text-center">Welcome to Chatire!</h1>
    <div id="auth-container" class="row">
      <div class="col-sm-4 offset-sm-4">
        <ul class="nav nav-tabs nav-justified" id="myTab" role="tablist">
          <li class="nav-item">
            <a class="nav-link active" id="signup-tab" data-toggle="tab" href="#signup" role="tab" aria-controls="signup" aria-selected="true">Sign Up</a>
          </li>
          <li class="nav-item">
            <a class="nav-link" id="signin-tab" data-toggle="tab" href="#signin" role="tab" aria-controls="signin" aria-selected="false">Sign In</a>
          </li>
        </ul>

        <div class="tab-content" id="myTabContent">

          <div class="tab-pane fade show active" id="signup" role="tabpanel" aria-labelledby="signin-tab">
            <form @submit.prevent="signUp">
              <div class="form-group">
                <input v-model="email" type="email" class="form-control" id="email" placeholder="Email Address" required>
              </div>
              <div class="form-row">
                <div class="form-group col-md-6">
                  <input v-model="username" type="text" class="form-control" id="username" placeholder="Username" required>
                </div>
                <div class="form-group col-md-6">
                  <input v-model="password" type="password" class="form-control" id="password" placeholder="Password" required>
                </div>
              </div>
              <div class="form-group">
                <div class="form-check">
                  <input class="form-check-input" type="checkbox" id="toc" required>
                  <label class="form-check-label" for="gridCheck">
                    Accept terms and Conditions
                  </label>
                </div>
              </div>
              <button type="submit" class="btn btn-block btn-primary">Sign up</button>
            </form>
          </div>

          <div class="tab-pane fade" id="signin" role="tabpanel" aria-labelledby="signin-tab">
            <form @submit.prevent="signIn">
              <div class="form-group">
                <input v-model="username" type="text" class="form-control" id="username" placeholder="Username" required>
              </div>
              <div class="form-group">
                <input v-model="password" type="password" class="form-control" id="password" placeholder="Password" required>
              </div>
              <button type="submit" class="btn btn-block btn-primary">Sign in</button>
            </form>
          </div>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script>
  const $ = window.jQuery // JQuery

  export default {

    data () {
      return {
        email: '', username: '', password: ''
      }
    }

  }
</script>

<style scoped>
  #auth-container {
    margin-top: 50px;
  }

  .tab-content {
    padding-top: 20px;
  }
</style>
```

I am using **Sublime Text 3** which has not pre-installed **Vue Markdown** so install
**Vue Component** package in **Sublime Text**

In the above snippet we use ```v-model``` was uesd for two way binding of all input
fields. This means that whatever is entered in the input fields can be accessed on
javascript side using ```this.field_name```

We also use ```@submit.prevent``` that listens form submitting and calls
the specified functions (which will be implemented soon).

Since we are using **bootstrap** we initialize ```$``` $ that points to the globally registered window.jQuery for using ```jquery``` instead of installing ```jquery``` from ```npm```

Now we will use **jQuery AJAX** methods to communicate with **django server**

Don’t forget to include bootstrap’s CSS and JavaScript in the main ```index.html``` 
page which is located in **chatire-frontend** folder

```
# index.html file
<!DOCTYPE html>
<html>
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1.0">
    <title>chatire-frontend</title>
    <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/css/bootstrap.min.css" integrity="sha384-Zug+QiDoJOrZ5t4lssLdxGhVrurbmBWopoEl+M6BdEfwnCJZtKxi1KgxUyJq13dy" crossorigin="anonymous">
    <style>
      .nav-tabs .nav-item.show .nav-link, .nav-tabs .nav-link.active {
        outline: none;
      }
    </style>
  </head>

  <body>

    <!-- Scripts -->
    <script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.2/jquery.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/popper.js/1.12.9/umd/popper.min.js" integrity="sha384-ApNbgh9B+Y1QKtv3Rn7W3mgPxhU9K/ScQsAP7hUibX39j7fakFPskvXusvfa0b4Q" crossorigin="anonymous"></script>
    <script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-beta.3/js/bootstrap.min.js" integrity="sha384-a5N7Y/aK3qNeh15eJKGWxsqtnX/wWdSZSKp+81YjTmS15nvnvxKHuzaWwXHDli+4" crossorigin="anonymous"></script>
    <div id="app"></div>
    <!-- built files will be auto injected -->

  </body>

</html>
```

# Auth Token
We have to let users login or sign up and then redirect them to the ```Chat``` route
To achieve that we have to implement the ```signIn``` and ```signUp``` methods we 
specified earlier.

In **UserAuth.vue**
```
<script>
  const $ = window.jQuery // JQuery

  export default {

    data () {
      return {
        email: '', username: '', password: ''
      }
    },

    methods: {
      signUp () {
        $.post("http://localhost:8000/auth/users/create/", this.$data, (data) => {
          alert("Your account has been created. You will be Signed In automatically!")
          this.signIn()
        })
        .fail((response) => {
          alert(response.responseText)
        })
      },

      signIn () {
        const credentials = {username: this.username, password: this.password}

        $.post("http://localhost:8000/auth/token/create/", credentials, (data) => {
          sessionStorage.setItem('authToken', data.auth_token)
          sessionStorage.setItem('username', this.username)
          this.router.push('/chats')
        })
        .fail((response) => {
          alert(response.ResponseText)
        })
      }
    }

  }

</script>
```

```methods``` contains both of the methods and send ajax post request to djoser 
endpoint for creating a new user.

Before hitting the **Sign In** button make sure that you run ```npm run dev``` and ```python manage.py runserver ```. You will get an error in the console...

```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote 
resource at http://localhost:8000/auth/users/create/. (Reason: CORS header 
‘Access-Control-Allow-Origin’ missing).[Learn More]
```

# CORS
Basically CORS is a mechanicsm that subverts the same origin policy. The same origin policy is what prevents a website on a different domain from making a XmlHttpRequest (Ajax) to another website/webservice. You can use CORS to weaken the security mechanicsm a little and tell the webserver that it’s safe to allow Ajax requests from a particular domain(s).

This is happening due to our **AJAX** request being sent from ```localhost:8080/```
to ```127.0.0.1:8000/``` In our case, even though both webservers are running on 
localhost, due to the fact that they’re on different ports (8080 and 8000) they’re 
seen as different domains.

**For the domains to match the scheme (http or https), hostname (localhost) and the port must match.**

So how do we enable CORS in our django application? There is third-party app we can 
install to do that called [django-cors-headers](https://github.com/ottoyiu/django-cors-headers)

```
pip install django-cors-headers
```

add it your ```INSTALLED_APPS```

```
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # packages
    'rest_framework',
    'rest_framework.authtoken',
    'djoser',
    'corsheaders',
]
```

Include the middleware, (Make sure it comes before
django.middleware.common.CommonMiddleware)

```
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',

    # django-cors-headers middleware comes before CommonMiddleware
    'corsheaders.middleware.CorsMiddleware',

    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]
```

Finally set ```CORS_ORIGIN_ALLOW_ALL = True``` in ```settings.py```

Note that this enables CORS for all domains. This is fine for development but when 
you’re in production you only want to allow certain domain(s) this can be controlled 
with:

Example:

CORS_ORIGIN_WHITELIST = (
    'google.com',
    'hostname.example.com',
    'localhost:8000',
    '127.0.0.1:9000'
)

**Behnind the scenes, django-cors-headers uses a Middleware to add appropriate headers to each request that tells Django that the request is safe and it should be allowed.**

**Try sign up by filling form and hit the button, you will get an alert saying your
account has been created**

Head over to [127.0.0.1:8000/admin](http://127.0.0.1:8000/admin) and after logging 
in head to users and you find a new user has been created. In admin site head to
**Token** there you will find a token has been created for the new user.

# Logout
If you haven't noticed I will remind you that we used ```sessionStorage``` which
means that whenever a user opens a new browser window or restarts the browser he
will be asked to sign in again in that window.

Instead we can use ```localStorage``` which enables all these features in the browser
window.

Just replace ```sessionStorage``` to ```localStorage``` in ```UserAuth.vue``` file this way you can also implement a function that removes the ```authToken``` from storage using ```localStorage.removeItem('authToken')```

**UserAuth.vue**
```
signIn () {
        const credentials = {username: this.username, password: this.password}

        $.post("http://localhost:8000/auth/token/create/", credentials, (data) => {
          localStorage.setItem('authToken', data.auth_token)
          localStorage.setItem('username', this.username)
          this.router.push('/chats')
        })
        .fail((response) => {
          alert(response.ResponseText)
        })
      }
```

# Chat Application With Django
So far our project has used djoser for user authentication backend and then 
connecting with frontend ```vue.js``` application to it.

In this part we will create ```APIs``` using **django-rest-framework** for providing
endpoints to start new chat sessions, join chat sessions, post new messages, and 
fetch a chat session's history.

1. When a user sends a message, this message would be forwarded to django through the API.

2. After django has received the message, It would also be forwarded to RabbitMQ.

3. RabbitMQ uses an exchange to broadcast the messages to multiple queues. The queues are communication channels that would eventually deliver the messages to the clients. The Workers are background processes that do the actual work of broadcasting and delivering messages.

## Implementation

In this part, our goal is to implement the API with django rest framework. The API would allow users start new chat sessions, join existing sessions and send messages. It would also allow us retrieve messages from a chat session.

Let’s start a new django app called chat

```
python manage.py startapp chat
```

Add the new app to ```INSTALLED_APPS```

Now we will create a model for our app. This model will store chat data like messages, chat sessions and associated users.

**chat/models.py**
```
from django.db import models
from django.contrib.auth import get_user_model

from uuid import uuid4

User = get_user_model()

def deserialize_user(user):
	"""Deserialize user instance to JSON"""
	return {
		'id': user.id, 'username': user.username, 'email': user.email,
		'first_name': user.first_name, 'last_name': user.last_name
	}


class TrackableDateModel(models.Model):
	"""Abstract model to track the creation/update date for a model"""

	created_date = models.DateTimeField(auto_now_add=True)
	updated_date = models.DateTimeField(auto_now=True)

	class Meta:
		abstract = True


def _generate_unique_uri():
	return str(uuid4()).replace('-', '')[:15]


class ChatSession(TrackableDateModel):
	"""A chat session. The uri's are generated by taking
	the first 15 characters from a UUID"""

	owner = models.ForeignKey(User, on_delete=models.PROTECT)
	uri = models.URLField(default=_generate_unique_uri)


class ChatSessionMessage(TrackableDateModel):
	"""Store messages for a session"""

	user = models.ForeignKey(User, on_delete=models.PROTECT)
	chat_session = models.ForeignKey(
		ChatSession, related_name='messages', on_delete=models.PROTECT
	)
	message = models.TextField(max_length=2500)

	def to_json(self):
		"""Deserialize message to JSON"""
		return {'user': deserialize_user(self.user), 'message': self.message}


class ChatSessionMember(TrackableDateModel):
	"""Store all users in a chat session"""

	chat_session = models.ForeignKey(
		ChatSession, related_name='members', on_delete=models.PROTECT
	)
	user = models.ForeignKey(User, on_delete=models.PROTECT)
```

```uuid``` provides ```uudi4``` which gives us a unique uuid object with ```-``` in 
between which can be converted to str and replace those hypens. We only use the first
15 unique characters.

The next step is to create views (API endpoints) that would be used by our Vue app 
to manipulate data on the server.

We can easily make use of django rest framework to create them (We won’t make use of 
serializers since our models are pretty simple). Let’s do that now in views.py

Now let's create views for chats

```
from django.shortcuts import render
from django.contrib.auth import get_user_model

from .models import (
  deserialize_user, ChatSession, ChatSessionMessage, ChatSessionMember
)

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import permissions

class ChatSessionView(APIView):
  """Manage Chat Session"""

  permission_classes = (permissions.IsAuthenticated,)

  def post(self, request, *args, **kwargs):
    """create a new chat session"""
    user = request.user

    chat_session = ChatSession.objects.create(owner=user)

    return Response({
      'status': 'SUCCESS', 'uri': chat_session.uri,
      'message': 'New chat session created'
    })

  def patch(self, request, *args, **kwargs):
    """Add a user to a chat session"""
    User = get_user_model()
    uri = kwargs['uri']
    username = request.data['username']
    user = User.objects.get(username=username)

    chat_session = ChatSession.objects.get(uri=uri)
    owner = chat_session.owner

    if owner is not user:  # Only allow non owners join the room
      chat_session.members.get_or_create(
        user=user, chat_session=chat_session
      )

    owner = deserializer_user(owner)
    members = [
      deserialize_user(chat_session.user)
      for chat_session in chat_session.members.all()
    ]
    members.insert(0, owner)  # make the owner first member

    return Response({
      'status': 'SUCCESS', 'members': members,
      'message': f"{user.username} joined chat session",
      'user': deserialize_user(user)
    })


class ChatSessionMessageView(APIView):
  """Create / Get chat session messages"""
  permission_classes = (permissions.IsAuthenticated,)

  def get(self, request, *args, **kwargs):
    """return all messages in a chat session"""
    uri = kwargs['uri']
    chat_session = ChatSession.objects.get(uri=uri)
    messages = [
      chat_session_message.to_json()
      for chat_session_message in chat_session.messages.all()
    ]

    return Response({
      'id': chat_session.id, 'uri': chat_session.uri,
      'messages': messages
    })

  def post(self, request, *args, **kwargs):
    """create a new message in a chat session."""
    uri = kwargs['uri']
    message = request.data['message']

    user = request.user
    chat_session = ChatSession.objects.get(uri=uri)

    ChatSessionMessage.objects.create(
      user=user, chat_session=chat_session, message=message
    )

    return Response({
      'status': 'SUCCESS', 'uri': chat_session.uri, 'message': message,
      'user': deserialize_user(user)
    })
```

Now let's add urls

```
from django.urls import path

from .views import (
  ChatSessionView, ChatSessionMessageView
)

urlpatterns += [
  path('chats/', ChatSessionView.as_view()),
  path('chats/<uri>/', ChatSessionView.as_view()),
  path('chats/<uri>/messages/', ChatSessionMessageView.as_view()),
]
```

Also include chat urls in base urls

```
urlpatterns += [
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
    path('api/', include('chat.urls')),
]
```

Our endpoints are ready and any AUTHENTICATED user make requests to them

Let’s try it out in **terminal** or **cmd**:

```
# command
curl -X POST http://127.0.0.1:8000/auth/token/create/ --data "username=admin&password=trydjango"

# output
{"auth_token":"6e6b6b6f4f1efe2e3f88db8dbec8da74cc556cf6"}

# put auth_token in next command
curl -X POST http://127.0.0.1:8000/api/chats/ -H "Authorization: Token 6e6b6b6f4f1efe2e3f88db8dbec8da74cc556cf6"

# output
{"status":"SUCCESS","uri":"467f53e415044c0","message":"New chat session created"}
F:\coder\django_chat\chat>

# create auth token for another user
curl -X POST http://127.0.0.1:8000/auth/token/create/ --data "username=alex&password=trydjango"
{"auth_token":"169fcd5067cc55c500f576502637281fa367b3a6"}

# use uri in next command
curl -X PATCH http://127.0.0.1:8000/api/chats/467f53e415044c0/ --data "username=alex" -H "Authorization: Token 169fcd5067cc55c500f576502637281fa367b3a6"

# output
'Authorization: Token 9c3ea2d194d7236ac68d2faefba017c8426a8484'
{"status":"SUCCESS","members":[{"id":1,"username":"admin","email":"admin@gmail.com","first_name":"","last_name":""},{"id":2,"username":"alex","email":"","first_name":"","last_name":""}],"message":"alex joined that chat","user":{"id":2,"username":"alex","email":"","first_name":"","last_name":""}}
```

Let's send some messages...

```
# command to send message from the auth token generated by usernam = admin
curl -X POST http://127.0.0.1:8000/api/chats/63c5a282c5b640d/messages/ --data "message=Hello there" -H "Authorization: Token
6e6b6b6f4f1efe2e3f88db8dbec8da74cc556cf6"

# output
{"status":"SUCCESS","uri":"63c5a282c5b640d","message":"Hello there","user":{"id":1,"username":"admin","email":"","first_name":"","last_name":""}}

# command to send message from alex user using alex user token
curl -X POST http://127.0.0.1:8000/api/chats/63c5a282c5b640d/messages/ --data "message=Ohh hey there admin whats up" -H "Authorization: Token 0e7497a938f06c83f6f07853480e24ad0448e188"

# output
{"status":"SUCCESS","uri":"63c5a282c5b640d","message":"Ohh hey there admin whats up","user":{"id":3,"username":"archit","email":"archit@services.com","first_name":"","last_name":""}}

curl http://127.0.0.1:8000/api/chats/63c5a282c5b640d/messages/ -H "Authorization: Token 6e6b6b6f4f1efe2e3f88db8dbec8da74cc556cf6"

# messages history
{"id":4,"uri":"63c5a282c5b640d","messages":[{"user":{"id":1,"username":"admin","email":"","first_name":"","last_name":""},"message":"Hello there"},{"user":{"id":1,"username":"admin","email":"","first_name":"","last_name":""},"message":"Hello there"},{"user":{"id":3,"username":"archit","email":"","first_name":"","last_name":""},"message":"Ohh hey there admin whats up"}]}
F:\coder\django_chat\chat>
```
