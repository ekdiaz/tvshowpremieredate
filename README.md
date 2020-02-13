# tvshowpremieredate
Email notification website for TV show premieres. https://tvshowpremieredate.pythonanywhere.com

TVShowPremiereDate emails out notifications as soon as a tv show's
premiere date is known, thus ending the need for incessantly checking
when your favorite shows are coming out. TVShowPremiereDate is hosted at
tvshowpremieredate.pythonanywhere.com and uses TVMaze API.

# Features
- Allows you to subscribe to your favorite TV shows
- Sends out emails whenever a new season premiere date is known for shows you
  are subscribed to
- Sends out reminder emails one week before the premiere date of any shows you 
  are subscribed to


# Installation
The following is mostly following these guides:
- https://help.pythonanywhere.com/pages/DeployExistingDjangoProject/
- https://help.pythonanywhere.com/pages/DjangoStaticFiles
- https://help.pythonanywhere.com/pages/UsingMySQL/
So check there for any issues.

## Getting started on Python Anywhere:
- Create an account on https://pythonanywhere.com (it can be a beginner account
  you will just have to log in once a month to keep it running)

## Downloads
- Go to the consoles tab and make a Bash console
- Run ```git clone https://github.com/ekdiaz/tvshowpremieredate.git```
- Run ```mkvirtualenv --python=/usr/bin/python2.7 mysite-virtualenv```
- Run ```pip install django``` (might take a while)
- Run ```pip install django-extensions```
- Run ```pip install --no-binary :all: mysql-python```
- Run ```pip install requests```

## Creating a web app
- Go to the web tab of PythonAnywhere
- Add a new web app (upgrade to choose your domain name if you want, otherwise click Next)
- Select Manual configuration
- Choose Python 2.7
- Click next until it says All done!

## Settings
- Enter the name of your virtualenv (mysite-virtualenv) in the Virtualenv section on the web 
  tab and click OK
- On the web tab under the Code section, click the file that ends in wsgi.py, this will open
  an editor
- Delete everything from the Django section and uncomment that section
- Change path to '/home/username/tvshowpremieredate' (replacing username with your 
  PythonAnywhere username
- Save

## Set up database
- Go to the Databases tab
- Initialize MySQL by creating a password
- Go to the Files tab
- Navigate to /home/username/tvshowpremieredate/mysite/settings.py
- Fill in NAME, USER, and PASSWORD in the following snippet in the settings.py file:
  ```
  DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '[Insert database name here]',
        'USER': '[Insert database user here]',
        'PASSWORD': '[Insert database password here]',
        'HOST': '[Insert database host address here]',
    }
  }```
- Save
- Go back to your Bash console
- Run ```cd tvshowpremieredate```
- Run ```./manage.py migrate``` (might take a while)

## Set up email script
- Make a gmail account to send emails from
- Turn on Less secure app access here: https://myaccount.google.com/u/1/security
- Again, go to /home/username/tvshowpremieredate/mysite/settings.py
- Fill in your email user and password for EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
- Go to the Tasks tab
- Create a scheduled task for a chosen time, tell it to run (with your username)
  ```python /home/username/tvshowpremieredate/syncdaily5.py```


## Clean up settings file (sorry)
- Find and replace all 'tvshowpremieredate' with your username in settings.py
- Also find and replace all 'mysite' with 'tvshowpremieredate/mysite'
- Set ROOT_URLCONF to 'mysite.urls'
- Set WSGI_APPLICATION to 'tvshowpremieredate.mysite.wsgi.application'
- Create a Secret Key using a tool like https://miniwebtool.com/django-secret-key-generator/
- Set SECRET_KEY to the secret key you generated

## Set up static files
- Run ```python2.7 manage.py collectstatic``` in Bash console
- Go to the Web tab under the Static files section, create two entries:
  - URL: /static/ Directory: /home/username/tvshowpremieredate/mysite/static
  - URL: /media/ Directory: /home/username/tvshowpremieredate/mysite/media
  
## Finish
- Go to the Web tab
- Click Reload
- Open your site!!



# Support
If you are having issues, please let me know.
We have a mailing list located at: tvshowpremieredate@gmail.com



