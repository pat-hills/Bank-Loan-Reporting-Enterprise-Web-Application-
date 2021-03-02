from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from business.services import *
from institution.services import *
from loan.services import *
from .services import *
from .models import *
from django.contrib import messages
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from collections import OrderedDict
import datetime

# Create your views here.



@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def submit_business_report(request):
    if request.method == "POST":


        report_category = request.POST["report_category"]
        date_of_reporting =  request.POST["date_of_report"]
        user_business = get_user_business(request)
        user_active_institution_on_loan = get_user_business_active_institution_on_loan(request)
        user_business_report_metrics = get_user_business_report_metrics(user_business,user_active_institution_on_loan.institution)

        find_and_verify_report_date_exist_qs = MonthReportSummary.find_and_verify_report_date_exist(MonthReportSummary,user_business)

        if find_and_verify_report_date_exist_qs.exists():
            messages.add_message(request, messages.WARNING, 'Reporting date alreading exist in report!.')
            return HttpResponseRedirect(reverse("businessreport:submit_business_report"))




        usr_month_report_summary = MonthReportSummary.objects.create(business=user_business,institution=user_active_institution_on_loan.institution,report_category=report_category,user=request.user,reporting_date=date_of_reporting)
        usr_month_report_summary.save()

        for post_data in user_business_report_metrics:
            if post_data.institution_custom_metric.unit_measurement == "Text" :

                data = request.POST[post_data.institution_custom_metric.metric_name]
                report_metric_data = get_business_report_metric_by_id(post_data.id)
                MonthReport.objects.create(report_category=report_category,report_value_non_numeric=data,reporting_date=date_of_reporting,business=user_business,
                institution=user_active_institution_on_loan.institution,report_metric=report_metric_data,user=request.user,month_report_summary=usr_month_report_summary)

            else:
                data = request.POST[post_data.institution_custom_metric.metric_name]
                report_metric_data = get_business_report_metric_by_id(post_data.id)
                MonthReport.objects.create(report_category=report_category,report_value_numeric=data,reporting_date=date_of_reporting,business=user_business,
                institution=user_active_institution_on_loan.institution,report_metric=report_metric_data,user=request.user,month_report_summary=usr_month_report_summary)


        messages.add_message(request, messages.SUCCESS, 'Successfully submitted business report!.')
        return HttpResponseRedirect(reverse("businessreport:all_submitted_business_report"))
        #return HttpResponseRedirect(reverse("business:business_dashboard",args=(user_business.slug,)))
                 
        
 
    else:

        user_business = get_user_business(request)
        user_active_institution_on_loan = get_user_business_active_institution_on_loan(request)
        user_business_report_metrics = get_user_business_report_metrics(user_business,user_active_institution_on_loan.institution)
         
        context = {'user_business_report_metrics' : user_business_report_metrics}
        
        return render(request, 'businessreport/submit_business_report.html',context)



@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def all_submitted_business_report(request):

    user_business = get_user_business(request)
    user_latest_application = get_users_latest_loan_application(user_business)
    if not user_latest_application:
        messages.add_message(request, messages.WARNING, 'You have no applied loan status to view and submit business reports!.')
        return HttpResponseRedirect(reverse("loan:business_loans",args=(request.session["business_name"],)))
    elif user_latest_application.loan_category == "PENDING":
        messages.add_message(request, messages.WARNING, 'You have pending loan status to view and submit business reports!.')
        return HttpResponseRedirect(reverse("loan:business_loans",args=(request.session["business_name"],)))

    elif user_latest_application.loan_category == "DENY":
        messages.add_message(request, messages.WARNING, 'You have deny loan status contact bank more information!.')
        return HttpResponseRedirect(reverse("loan:business_loans",args=(request.session["business_name"],)))
         

    user_submitted_report = get_summary_submitted_monthly_business_report(user_business,institution=None)
    
     
   
    return render(request, "businessreport/all_submitted_business_report.html",{ 

        "user_submitted_report" : user_submitted_report,
          "user_latest_application" : user_latest_application
        
     })






@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def edit_break_down_summary_monthly_report(request,month_report_summary):

    if request.method == "POST":


        category = request.POST["report_category"]
        date_of_reporting =  request.POST["date_of_report"]
        month_report_summary =  request.POST["month_report_summary"]

        user_business = get_user_business(request)

        break_down_report = get_break_down_monthly_summary_business_report(month_report_summary)
        business_summary = get_summary_submitted_monthly_report_by_id(month_report_summary)


        #find_and_verify_report_date_exist_qs = MonthReportSummary.find_and_verify_report_date_exist(MonthReportSummary,date_of_reporting,user_business)

        #if find_and_verify_report_date_exist_qs.exists():
        #    messages.add_message(request, messages.WARNING, 'Reporting date alreading exist in report!.')
        #    return HttpResponseRedirect(reverse("businessreport:edit_break_down_summary_monthly_report", args=(month_report_summary,)))    


        update_summary = update_monthly_summary(month_report_summary,report_category=category,reporting_date=date_of_reporting)

        if update_summary:
            for post_data in break_down_report:
                if post_data.report_metric.unit_measurement=="Text":
                    data = request.POST[post_data.report_metric.metric_name]
                    month_report_id = post_data.pk
                    update_non_numeric_report_data_monthly_business_report(business_summary,month_report_id,data)
                else:
                    data = request.POST[post_data.report_metric.metric_name]
                    month_report_id = post_data.pk
                    update_numeric_report_data_monthly_business_report(business_summary,month_report_id,data)

            messages.add_message(request, messages.SUCCESS, 'Successfully edited business report!.')
            return HttpResponseRedirect(reverse("businessreport:all_submitted_business_report"))

 
    else:

        user_business = get_user_business(request)
        month_summary = get_summary_submitted_monthly_report_by_id(month_report_summary)

        user_b = month_summary.business
        user_s = month_summary.user

        if user_business != user_b:
            messages.add_message(request, messages.WARNING, 'Unauthorize permission to view record!.')
            return HttpResponseRedirect(reverse("businessreport:all_submitted_business_report"))
    
        else:

            break_down_report = get_break_down_monthly_summary_business_report(month_summary) 
            df = DateFormat(month_summary.reporting_date)
            df.format(get_format('DATE_FORMAT'))
            date_report_format = df.format('Y-m-d')

            if break_down_report is None:
                messages.add_message(request, messages.WARNING, 'Unauthorize permission to view record!.')
                return HttpResponseRedirect(reverse("businessreport:all_submitted_business_report"))
         
            context = {'break_down_report' : break_down_report ,"month_summary" : month_summary,"date_report_format" :date_report_format}
        
            return render(request, 'businessreport/edit_view_break_down_summary_monthly_report.html',context)




@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def delete_monthly_report(request,month_report_summary):

    if request.method == "POST":


        month_report_summary =  request.POST["id"]
        month_summary = get_summary_submitted_monthly_report_by_id(month_report_summary)
        delete_summary = delete_monthly_summary(month_report_summary)

        if delete_summary:
            delete_monthly_summary_breakdown(month_summary)

            messages.add_message(request, messages.WARNING, 'Successfully deleted business report!.')
            return HttpResponseRedirect(reverse("businessreport:all_submitted_business_report"))

 
    else:

        return render(request, 'businessreport/all_submitted_business_report.html')



# @login_required
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# def charts_graphs_metrics(request,business_name):

#     user_business = get_user_business(request)

#     dataSource = OrderedDict()


#     chartConfig = OrderedDict()
#     chartConfig["caption"] = "Countries With Most Oil Reserves [2017-18]"
#     chartConfig["xAxisName"] = "Country"
#     chartConfig["yAxisName"] = "Reserves (MMbbl)"
#     chartConfig["numberSuffix"] = "K" 
#     dataSource["chart"] = chartConfig
#     dataSource["data"] = []

#     data_source_db = get_business_report_charts(user_business)
#     if data_source_db:
#         for key_data in data_source_db:
#             if key_data.report_metric.institution_custom_metric.unit_measurement != "Text":
#                 data = {}
#                 #df = DateFormat(key_data.reporting_date)
#                 #df.format(get_format('DATE_FORMAT'))
#                 #date_report_format = df.format('Y-m-d')
#                 #data['label'] = date_report_format
#                 data['label'] = key_data.report_metric.institution_custom_metric.metric_name
#                 data['value'] = key_data.report_value_numeric
#                 dataSource["data"].append(data)
#                 column2D = FusionCharts("line", "charts_graphs_metrics" , "100%", "350", "charts_graphs_metrics-container", "json", dataSource)
#                 context = {'output' : column2D.render()}
#         return render(request, 'businessreport/business_charts_report.html',context)

#     return render(request, "businessreport/business_charts_report.html")







@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def view_business_charts_graphs_reports(request,business_name):

    if request.method == "POST":


        user_business = get_user_business(request)
        # month_summary = get_summary_submitted_monthly_report_by_id(month_report_summary)
        # delete_summary = delete_monthly_summary(month_report_summary)

        # if delete_summary:
        #     delete_monthly_summary_breakdown(month_summary)

        #     messages.add_message(request, messages.WARNING, 'Successfully deleted business report!.')
        #     return HttpResponseRedirect(reverse("businessreport:all_submitted_business_report"))

 
    else:

        user_business = get_user_business(request) 

        metric_charts_data = get_business_report_charts(user_business)

        context = {'metric_charts_data' : metric_charts_data}




        return render(request, 'businessreport/business_charts_report.html',context)



@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def view_business_metrics_progress(request,business_name):


    user_business = get_user_business(request)

    business_view_metrics = get_business_metrics_progress(user_business)

    if not business_view_metrics:
        messages.add_message(request, messages.WARNING, 'You have no applied loan status to view submitted business metrics!.')
        return HttpResponseRedirect(reverse("loan:business_loans",args=(request.session["business_name"],)))


    context = {'business_view_metrics' : business_view_metrics}

     




    return render(request, 'businessreport/view_business_metrics_progress.html',context)




@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def view_business_month_report_metric_progress_chart(request,business_name,report_metric_id):


    user_business = get_user_business(request)

    report_metric = get_business_report_metric_by_id(report_metric_id)

    data = get_business_month_report_by_report_metric(user_business,report_metric)
    data_sum = get_business_month_report_by_report_metric_total(user_business,report_metric)

    context = {'data' : data,'report_metric' : report_metric,'data_sum':data_sum}


    return render(request, 'businessreport/view_business_month_report_metric_progress_chart.html',context)












 
  
