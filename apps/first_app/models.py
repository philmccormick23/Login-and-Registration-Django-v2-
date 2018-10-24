from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

# Create your models here.
class UserManager(models.Manager):
    def registration_validator(self, post_data):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        errors = {}
        if len(post_data['first_name']) < 2:
            errors['first_name'] = 'Please enter a first name.'
        if len(post_data['last_name']) < 2:
            errors['last_name'] = 'Please enter a last name.'
        if len(post_data['email']) < 1:
            errors['email'] = 'Please enter an email address.'
        elif not EMAIL_REGEX.match(post_data['email']):
            errors['email'] = 'Please enter a valid email address.'
        if len(post_data['password']) < 8:
            errors['password'] = 'Password must be at least 8 characters.'
        if post_data['confirm'] != post_data['password']:
            errors['confirm'] = 'Password is not confirmed.'
        if len(User.objects.filter(email=post_data['email'])) > 0:
            errors['email'] = 'Email address already registered.'
        return errors
    
    def login_validator(self, post_data):
        errors = {}
        logged_user = User.objects.filter(email=post_data['email'])
        if len(post_data['email']) < 1:
            errors['email'] = 'Please enter an email address.'
        if len(post_data['password']) < 1:
            errors['password'] = 'Please enter a password.'
        if len(User.objects.filter(email=post_data['email'])) == 0:
            errors['email'] = 'Email has not been registered.'
            return errors
        else:
            logged_user = User.objects.filter(email=post_data['email'])[0]
            print(logged_user.password)
        if bcrypt.checkpw(post_data['password'].encode('UTF-8'), logged_user.password.encode('UTF-8')):
            pass
        else:
            errors['password'] = 'Incorrect password.'
        return errors
    
   

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add = True)
    updated_at = models.DateTimeField(auto_now = True)    
    objects = UserManager()