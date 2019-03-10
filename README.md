# mentor-api

You need to install pipenv using `pip3 install pipenv`. (pip3 is available in your system if you have python3)

pipenv is like yarn and pipfile is alike package.json. All the packages are listed there. You can now go to this repo in your system
and type `pipenv install`. This will install all the required packages for this application. You should be in the location where
there is pipfile and pipfile.lock. 

After you have required packages, navigate inside mentorapi directory and check if its working or not using `python manage.py runserver`.
if its running, you need to migrate the file. To migrate, you have to do `python manage.py migrate`. you have now admin panel
ready with you where users will only be there initially. For our database ready, please type following command subsequently

```python manage.py makemigrations``` . This will watch for all the tables we have created and if there is any changes that is ready to
migrate.

```python manage.py migrate```. This will now sync up to database and all the tables will be shown in admin.

Now run the server using 

```python manage.py runserver```

load up the url ```localhost:8000``` in the browser. you might see django default page as we are not handling the view part so there's no
any template to show up. You should instead go to ```localhost:8000/admin```. 

The username and pass for admin is admin@gmail.com and admin123.
