from .models import ReportMetric,MonthReportSummary,MonthReport
from django.core.exceptions import ObjectDoesNotExist
import json
from django.db.models import Count, Q
from django.db.models import Sum
import datetime
from repurta.utils import *
#from institution.models import Institution




def get_user_business_report_metrics(business,institution ):
    user_business_report_metrics = ReportMetric.objects.filter(is_deleted=False,business=business,institution=institution).select_related("institution_custom_metric")
    return user_business_report_metrics

def get_business_report_metric_by_id(id):
    business_report_metric_data = ReportMetric.objects.select_related("institution_custom_metric").get(is_deleted=False,id=id)
    return business_report_metric_data


def get_submitted_business_report(business):
    submitted_business_report = MonthReport.objects.filter(is_deleted=False,business=business).select_related("month_report_summary","report_metric")
    return submitted_business_report



        return submitted_business_report_institution


def get_all_business_monthly_defaulters(institution):

    today = datetime.datetime.now()
    current_year = today.year
    current_month = today.month

    if institution is not None:
        submitted_business_report = MonthReportSummary.objects.filter(is_deleted=False,institution=institution,
        date_created__year = current_year,date_created__month = current_month).prefetch_related("business","institution")
        return submitted_business_report



def get_summary_submitted_monthly_report_by_id(id):
    try:
        get_summary_submitted_monthly_report_by_id = MonthReportSummary.objects.select_related("business","user","institution").get(is_deleted=False,id=id)
        #return get_summary_submitted_monthly_report_by_id
    except MonthReportSummary.DoesNotExist:
        get_summary_submitted_monthly_report_by_id = None
    
    return get_summary_submitted_monthly_report_by_id





def update_numeric_report_data_monthly_business_report(month_report_summary,id,data): 
    update_numeric_report_data_monthly_business_report = MonthReport.objects.filter(is_deleted=False,month_report_summary=month_report_summary,id=id).update(report_value_numeric=data)
    return update_numeric_report_data_monthly_business_report


def update_non_numeric_report_data_monthly_business_report(month_report_summary,id,data): 
    update_non_numeric_report_data_monthly_business_report = MonthReport.objects.filter(is_deleted=False,month_report_summary=month_report_summary,id=id).update(report_value_non_numeric=data)
    return update_non_numeric_report_data_monthly_business_report


def update_monthly_summary(month_summary,report_category,reporting_date): 
    update_monthly_summary = MonthReportSummary.objects.filter(is_deleted=False,id=month_summary).update(report_category=report_category,reporting_date=reporting_date)
    return update_monthly_summary

def delete_monthly_summary(month_summary): 
    delete_monthly_summary = MonthReportSummary.objects.filter(id=month_summary).update(is_deleted=True)
    return delete_monthly_summary


def delete_monthly_summary_breakdown(month_report_summary): 
    delete_monthly_summary_breakdown = MonthReport.objects.filter(month_report_summary=month_report_summary).update(is_deleted=True)
    return delete_monthly_summary_breakdown




def get_business_report_charts(business):

    try:
          get_business_report_charts = MonthReport.objects.filter(is_deleted=False,report_category='Published',business=business).order_by("report_metric")
    
   
    except MonthReport.DoesNotExist:
        get_business_report_charts = None
    
    return get_business_report_charts


def get_report_metric_numeric_in_monthly_report(business,report_metric):

    try:
        get_report_metric_numeric_in_monthly_report = MonthReport.objects.values('report_metric.institution_custom_metric.metric_name').filter(is_deleted=False,business=business,report_metric=report_metric).annotate(total=Count('id')).prefetch_related("report_metric","month_report_summary")
    
    except MonthReport.DoesNotExist:
        get_report_metric_numeric_in_monthly_report = None
    
    return get_report_metric_numeric_in_monthly_report





def get_business_metrics_progress_ii(business):

    try:
          view_business_metrics_progress = MonthReport.objects.exclude(report_value_numeric__isnull=True).values("report_metric").annotate(report_value_numeric_total = Sum('report_value_numeric')).filter(is_deleted=False,report_category='Published',business=business).prefetch_related("report_metric","month_report_summary")
    
   
    except MonthReport.DoesNotExist:
        view_business_metrics_progress = None
    
    return view_business_metrics_progress





def get_business_month_report_by_report_metric(business,reportmetric):

    try:
          business_report_metrics = MonthReport.objects.filter(is_deleted=False,business=business,report_metric=reportmetric).prefetch_related("report_metric","month_report_summary")
    
   
    except MonthReport.DoesNotExist:
        business_report_metrics = None
    
    return business_report_metrics



def get_business_month_report_by_report_metric_total(business,reportmetric):

    try:
          business_report_metrics_total = MonthReport.objects.exclude(report_value_numeric__isnull=True).filter(is_deleted=False,
          business=business,report_metric=reportmetric).aggregate(data_sum=Sum('report_value_numeric'))
    
   
    except MonthReport.DoesNotExist:
        business_report_metrics_total = None
    
    return business_report_metrics_total


#BEGIN INSTITUTION DATA

def get_total_report_submissions(institution):

    try:
          today = datetime.datetime.now()
          current_year = today.year
          #current_month = today.month
          report_summary_submitted = MonthReportSummary.objects.filter(is_deleted=False,institution=institution,date_created__year = current_year).count()
    
    except MonthReportSummary.DoesNotExist:
        report_summary_submitted = None
    return report_summary_submitted



def get_total_published_report_submissions(institution):

    try:
          today = datetime.datetime.now()
          current_year = today.year
          #current_month = today.month
          report_summary_published = MonthReportSummary.objects.filter(is_deleted=False,institution=institution,date_created__year = current_year,report_category=report_published_value).count()
    
    except MonthReportSummary.DoesNotExist:
        report_summary_published = None
    return report_summary_published


def get_total_pending_report_submissions(institution):

    try:
          today = datetime.datetime.now()
          current_year = today.year
          #current_month = today.month
          report_summary_draft = MonthReportSummary.objects.filter(is_deleted=False,institution=institution,date_created__year = current_year,report_category=report_draft_value).count()
    
    except MonthReportSummary.DoesNotExist:
        report_summary_draft = None
    return report_summary_draft













#END


