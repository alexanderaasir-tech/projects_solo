from django.db import models
import re
import datetime

# Create your models here.

# User manager to validate the post data entered in the index - registration - form - post data

class UserManager(models.Manager):
    def create_validator(self,reqPOST):

        #catch all errors in the dictionary and return to views.py
        errors = {}
        #Validation for blank first name and last name fiedls
        if len(reqPOST['first_name']) <3:
            errors['first_name'] = "Entered  first name is too short"
        if len(reqPOST['last_name']) <3:
            errors['last_name'] = "Entered  last name is too short"
        
        #email field blank validations
        if len(reqPOST['email']) < 1:
            errors['email'] = "Email cannot be blank "
        #email pattern validations
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(reqPOST['email']):    # test whether a field matches the pattern            
            errors['regex'] = "Invalid email address"

        #check for duplicate email validations since this will the user name which is unique
        users_with_email = User.objects.filter(email=reqPOST['email'])
        if len(users_with_email) >=1:
            errors['uniqueness'] = "Email already exists"

        #password validations
        if len(reqPOST['password'])<8:
            errors['password'] = "Entered password should be atleast 8 characters"
        #check if password and confirm password are the same
        if reqPOST['password'] != reqPOST['confirm_password']:
            errors['match'] = "Passwords dont match"
        return errors

#user model that matches fields in the index -> registration block of html
class User(models.Model):
    first_name = models.CharField(max_length=45)
    last_name = models.CharField(max_length=45)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Restaurant(models.Model):
    name = models.TextField()
    description = models.TextField()
    location = models.TextField()
    owner = models.ForeignKey(User, related_name="restaurant_created", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    # objects = JobManager()

class Item(models.Model):
    item = models.TextField()
    quantity = models.IntegerField()
    restaurant = models.ForeignKey(Restaurant, related_name = "item_created", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Order(models.Model):
    customer_qty = models.IntegerField()
    user_order = models.ForeignKey(User, related_name = "user_orders", on_delete = models.CASCADE)
    item_order = models.ForeignKey(Item, related_name = "items_ordered", on_delete = models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    # updated_at = models.DateTimeField(auto_now=True)
