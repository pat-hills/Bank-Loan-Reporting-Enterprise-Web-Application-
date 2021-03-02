from django.db import models
from django.db import models
from business.models import Business,BusinessCustomMetric
from institution.models import Institution,InstitutionCustomMetric
from appusers.models import User


class ReportMetric(models.Model):
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateField(null=False, auto_now=True)
    date_time_created = models.DateTimeField(null=False, auto_now=True)
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=True,related_name="business_report_metric")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=True,related_name="institution_report_metric")
    business_custom_metric = models.ForeignKey(BusinessCustomMetric, on_delete=models.CASCADE, null=True,related_name="business_custom_report_metric")
    institution_custom_metric = models.ForeignKey(InstitutionCustomMetric, on_delete=models.CASCADE, null=True,related_name="institution_custom_report_metric")
    
    def __str__(self):
         return "%s %s" % (self.id)



class MonthReportSummary(models.Model):    
    report_category = models.CharField(max_length=256, null=True)
    reporting_date = models.DateField(null=False)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateField(null=False, auto_now=True)
    date_time_created = models.DateTimeField(null=False, auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,related_name="user_month_report_summary")
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False,related_name="business_month_report_summary")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=False,related_name="institution_month_report_summary")
    report_metric = models.ForeignKey(ReportMetric, on_delete=models.CASCADE, null=True,related_name="report_metric_summary")

    def __str__(self):
         return "%s %s" % (self.id)

    
    def find_and_verify_report_date_exist(self, reporting_date,business):
        reporting_date = self.objects.filter(is_deleted=False, reporting_date=reporting_date,business = business,report_category='Published')
        return reporting_date


    def update_report_summary(self,request):
        self.reporting_date = request
        self.report_category = request
        self.save() 



class MonthReport(models.Model):
    report_code = models.CharField(max_length=128,null=True,default="0000")
    report_value_non_numeric = models.TextField(null = True) 
    report_value_numeric = models.IntegerField(null = True)
    report_value = models.CharField(null = True,max_length=256) 
    report_category = models.CharField(max_length=256, null=True)
    reporting_date = models.DateField(null=False)
    is_deleted = models.BooleanField(default=False)
    date_created = models.DateField(null=False, auto_now=True)
    date_time_created = models.DateTimeField(null=False, auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False,related_name="user_month_report")
    business = models.ForeignKey(Business, on_delete=models.CASCADE, null=False,related_name="business_month_report")
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE, null=False,related_name="institution_month_report")
    report_metric = models.ForeignKey(ReportMetric, on_delete=models.CASCADE, null=False,related_name="report_metric")
    month_report_summary = models.ForeignKey(MonthReportSummary, on_delete=models.CASCADE, null=True,related_name="month_report_summary")

    
    def __str__(self):
         return "%s %s" % (self.id)




# Create your models here.
