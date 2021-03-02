from django.db import models
from appusers.models import User
from business.models import Business
from institution.models import Institution

# Create your models here.

class Loan(models.Model):
    amount = models.FloatField(max_length=128,null=False)
    reason = models.TextField(max_length = 256, null = True, blank = True) 
    transaction_code = models.CharField(max_length=256, null=False)
    term_of_loan = models.CharField(max_length=128, null=True)
    date_of_payment = models.DateField(max_length=128, null=True)
    business_number = models.CharField(max_length=128, null=False)
    loan_status = models.CharField(max_length=128, null=False,default="UNPAID") 
    loan_category = models.CharField(max_length=128, null=False, default="PENDING") 
    business_certificate = models.ImageField(upload_to='businessDocument/', null=False)
    is_deleted = models.BooleanField(default=False)
    institution_action_by = models.CharField(max_length=128, null=True) 
    date_created = models.DateField(null=False, auto_now=True)
    date_time_created = models.DateTimeField(null=False, auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,related_name="user_loan")
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False,related_name="business_loan")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=False,related_name="institution_loan")
    
    def __str__(self):
         return "%s %s" % (self.amount,self.transaction_code)
