from django.contrib.auth.models import AbstractUser,UserManager
from django.db import models 

# Create your models here.

class User(AbstractUser):
    is_password_change = models.BooleanField(default=True)
    account_type = models.TextField(blank=False,max_length=64)
    is_institution_setup = models.BooleanField(null=False,default=True)
    user_role = models.TextField(blank=False,max_length=128)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateField(null=False, auto_now=True)
    date_time_created = models.DateTimeField(null=False, auto_now=True)


    def if_email_exist(self,request_email):
        num_results = User.objects.filter(self.email == request_email ).count()
        return num_results

    def find_user_by_email(self, email):
        queryset = self.get_queryset()
        return queryset.filter(email=email)
    

    def complete_institution_setup(self,user):
        user.is_institution_setup = True
        user.save()






    



