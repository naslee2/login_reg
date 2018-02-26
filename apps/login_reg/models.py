from __future__ import unicode_literals
from django.db import models
import re, bcrypt
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
PASSWORD_REGEX=re.compile(r'^[a-zA-Z0-9]+$')
NAME_REGEX = re.compile(r'^[a-zA-Z]+$')

class UserManager(models.Manager):
    def validator(self, postData):
        errors={}
        if len(postData['first_name']) < 1:
            errors['first_name'] = "First name should be more than 1 character!"
        elif not NAME_REGEX.match(postData['first_name']):
            errors['first_name'] = "First name should not have any numbers!"

        if len(postData['last_name']) < 1:
            errors['last_name'] = "Last name should be more than 1 character!"
        elif not NAME_REGEX.match(postData['last_name']):
            errors['last_name'] = "Last name should not have any numbers!"

        if EMAIL_REGEX.match(postData['email']):
            dup = User.objects.filter(email=postData['email'])
            if len(dup) > 0:
                errors['email'] = "Email is already registered!"
        else:
            errors['email'] = "Must put in a Valid Email!"

        if len(postData['password'])< 7:
            errors['password'] = "Must put in a Valid Password!"
        elif not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Must put in a Valid Password!"
            
        if len(postData['confirm_pw'])< 7:
            errors['confirm_pw'] = "Must put in a Valid Password!"
        elif not PASSWORD_REGEX.match(postData['confirm_pw']):
            errors['confirm_pw'] = "Must put in a Valid Password!"
        elif not postData['password'] == postData['confirm_pw']:
            errors['confirm_pw'] = "Passwords must be the same!"
        if len(errors) < 1:
            reg_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
            reg_user = User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'], email=postData['email'], password=reg_hash)
            errors['valid_user'] = reg_user
        return errors

    def validator2(self, postData):
        errors2={}
        check = User.objects.filter(email=postData['login_email'])
        if check:
            check2 = check[0].email
            check3 = check[0].password
            if bcrypt.checkpw(postData['login_password'].encode(), check3.encode()):
                errors2['success'] = check[0] 
                return errors2
            else: 
                errors2['login_password'] = "Invalid 0101"
                return errors2
        else:
            errors2['login_password'] = "Invalid 0011"
            return errors2

class User(models.Model):
    first_name=models.CharField(max_length=255)
    last_name=models.CharField(max_length=255)
    email=models.CharField(max_length=255)
    password=models.CharField(max_length=45)
    password=models.CharField(max_length=45)
    objects= UserManager()
   