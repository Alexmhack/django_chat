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

Hit the **Sign In** button and you get an error saying

```
Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote 
resource at http://localhost:8000/auth/users/create/. (Reason: CORS header 
‘Access-Control-Allow-Origin’ missing).[Learn More]
```
