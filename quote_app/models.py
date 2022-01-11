from django.db import models
import re

class User_Manager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email_address']):           
            errors['email_address'] = ("Invalid email address!")
        if len(postData['password']) <2:
            errors['password'] = 'Password must exceed 2 characters'
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData["last_name"]) < 3:
            errors["last_name"] = "Last name should be at least 3 characters"
        if postData['password'] != postData['confirm_password']:
            errors['password'] = 'Password and Confirm Password do not match'
        return errors
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email_address = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = User_Manager()

class Quote_Manager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if len(postData['author']) < 2:
            errors["author"] = "Quoted by should be at least 2 characters"
        if len(postData["desc"]) < 10:
            errors["desc"] = "Quote needs to be at least 10 characters"
        return errors

class Quote(models.Model):
    author = models.CharField(max_length=255)
    desc = models.TextField()
    user_quote = models.ForeignKey(User, related_name ="post", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = Quote_Manager()

