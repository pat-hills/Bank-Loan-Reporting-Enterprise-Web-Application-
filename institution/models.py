from django.db import models
from appusers.models import User
from .signals import unique_slug_generator
from django.db.models.signals import pre_save



# Create your models here.FinancialInstitutionCustomMetric

class Institution(models.Model):
    name = models.CharField(max_length=128,null=False)
    slug = models.SlugField(max_length = 250, null = True, blank = True) 
    contact = models.CharField(max_length=128, null=True)
    location = models.CharField(max_length=128, null=False)
    district = models.CharField(max_length=128, null=False)
    region = models.CharField(max_length=128, null=False)
    country = models.CharField(max_length=128, null=False)
    tagline = models.TextField(null=False, default='Tagline')
    mission = models.TextField(null=True)
    vision = models.TextField(null=True)
    founder = models.CharField(max_length=128,null=True)
    logo = models.ImageField(upload_to='institutionLogo/', null=False)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateField(null=False, auto_now=True)
    date_time_created = models.DateTimeField(null=False, auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,related_name="user_institution")
    
    def __str__(self):
         return "%s %s" % (self.name,self.tagline)
    
 
  
def pre_save_receiver(sender, instance, *args, **kwargs): 
    if not instance.slug: 
        instance.slug = unique_slug_generator(instance) 



pre_save.connect(pre_save_receiver, sender = Institution)
 


class InstitutionCustomMetric(models.Model):
    metric_name = models.CharField(max_length=128,null=False)
    slug = models.SlugField(max_length = 250, null = True, blank = True) 
    metric_short_name = models.CharField(max_length=128,default='msn', null=False)
    unit_measurement = models.CharField(max_length=128, null=False)
    preferred_chart = models.CharField(max_length=128, null=True)
    description = models.CharField(max_length=128, null=True)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateField(null=False, auto_now=True)
    date_time_created = models.DateTimeField(null=False, auto_now=True)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=False,related_name="institution_metric")
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=False,related_name="user_created_by_metric")

    def __str__(self):
         return "%s %s" % (self.metric_name,self.metric_short_name)

    



