from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Institution, InstitutionCustomMetric
from .services import *
from .utils import greetings
from django.contrib import messages
from loan.services import *
from businessreport.services import * 
from appusers.models import User
#from appusers import models

# Create your views here.

# @login_required
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# def institution_setup(request):
#     request.session['fullname'] = request.user.first_name
#     return render(request, "institution/institution_setup.html",{
#     })

@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def institution_setup_register(request):

    if request.method == "POST":
        
        name = request.POST["name"]
        branch = request.POST["branch"]
        tagline = request.POST["tagline"]
        country = request.POST["country"]
        region = request.POST["region"]
        district = request.POST["district"]
        institutionLogo = request.FILES["institutionLogo"]
        

        # Ensure password matches confirmation  
        # if password != confirmpassword:
        #     return render(request, "account/institution_sign_up.html", {
        #         "message": "Passwords must match!"
        #     })

        save_user_institution = Institution.objects.create(name=name,tagline = tagline,location = branch,country=country,
        district = district,region=region,logo = institutionLogo,user=request.user)
        save_user_institution.save()
        User.complete_institution_setup(User,request.user)
        request.session["institution_name"] = save_user_institution.name
        request.session["institution_id"] = save_user_institution.id
        request.session["institution_slug_name"] = save_user_institution.slug
        request.session["institution_location"] = save_user_institution.location
        
        return HttpResponseRedirect(reverse("institution:institution_complete"))
    else:
        return render(request, "institution/institution_setup.html", {
           

    })



@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def institution_complete(request):
    #users_institution = Institution.objects.get(is_deleted=False,user=request.user)
    users_institution = get_user_institution(request)
    return render(request, "institution/institution_welcome_home.html",{
         "greetings" : greetings,
         "users_institution" : users_institution
     })


@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def institution_dashboard(request,institutionname):
    #request.session['institutionname'] = institutionname
    return render(request, "institution/institution_dashboard.html",{
         "greetings" : greetings
     })

@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def institution_setting(request,institutionname):
    user_institution_details = get_user_institution(request)
    user_customer_metrics = get_user_institution_custom_metrics(request)
    context = {'user_customer_metrics' : user_customer_metrics,'user_insti_details' : user_institution_details}
    return render(request, 'institution/institution_setting.html',context)


@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def create_institution_metric(request):
    if request.method == "POST":
        
        metricfullname = request.POST["metricfullname"]
        metricshortname = request.POST["metricshortname"]
        cleanmetricshortname = metricshortname.replace(" ","_")
        #mystring.replace(" ", "_")
        metricunitofmeasure = request.POST["metricunitofmeasure"]
        preferredcharttype = request.POST["preferredcharttype"]
        metricdescription = request.POST["metricdescription"] 
        

        # Ensure password matches confirmation
        # if password != confirmpassword:
        #     return render(request, "account/institution_sign_up.html", {
        #         "message": "Passwords must match!"
        #     })

        #user_institution_by_id = get_user_institution_by_id(request.session["institution_id"])

        save_institution_metric = InstitutionCustomMetric.objects.create(metric_name=metricfullname,metric_short_name = cleanmetricshortname,
        unit_measurement = metricunitofmeasure,preferred_chart=preferredcharttype,description = metricdescription,institution=get_user_institution(request),created_by=request.user)
        save_institution_metric.save()

       
        
        #return reverse('institution:institution',args=(request.session["institution_name"]))
        messages.add_message(request, messages.SUCCESS, 'Successfully saved institution metrics!.')
        return HttpResponseRedirect(reverse("institution:institution_setting",args=( request.session["institution_slug_name"],)))
    else:
         #user_customer_metrics = get_user_institution_custom_metrics(request)
         return render(request, "institution/institution_setting.html",{
     })


@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def institutions_all_loan_applications(request,institutionname):
    users_institution = get_user_institution(request)
    users_business_loans = get_loans_for_institutions(users_institution)

    return render(request, "institution/institution_all_loan_applications.html",{
        "users_business_loans" :users_business_loans, 
     })



@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def all_submitted_business_report(request,institutionname):
 
    user_institution = get_user_institution(request)
    is_Business = None
    business_submitted_report = get_summary_submitted_monthly_business_report(is_Business,user_institution) 
   
    return render(request, "institution/all_submitted_business_report.html",{ 

        "business_submitted_report" : business_submitted_report
        
     })





@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def all_business_monthly_defaulters(request,institutionname):


    user_institution = get_user_institution(request)

    all_defaulters_month = get_all_business_monthly_defaulters(user_institution)


    context = {'all_defaulters_month' : all_defaulters_month,}


    return render(request, 'institution/all_defaulters_businesses_monthly.html',context)




@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def institution_metrics(request,institutionname):


    if request.method == "POST":


        user_institution = get_user_institution(request)

 
    else:

        user_institution = get_user_institution(request)
        loan_sum = get_total_amount_loan_applied_current_year(user_institution) 
        total_loans_applied = get_total_loans_applied(user_institution)
        total_authorized_loans = get_total_authorized_loans(user_institution)
        total_rejected_loans = get_total_denied_loans(user_institution)
        loan_auth_sum = get_total_amount_loan_applied_current_year_authorized(user_institution)
        loan_denied_sum = get_total_amount_loan_applied_current_year_denied(user_institution)
        total_report_submitted = get_total_report_submissions(user_institution)
        total_report_submitted_published = get_total_published_report_submissions(user_institution)
        total_pending_report = get_total_pending_report_submissions(user_institution)

         

        context = {'loan_sum' : loan_sum,'total_loans_applied' : total_loans_applied,
        'total_authorized_loans':total_authorized_loans,'total_rejected_loans':total_rejected_loans,'loan_auth_sum':loan_auth_sum,
        'loan_denied_sum':loan_denied_sum,'total_report_submitted' : total_report_submitted,'total_report_submitted_published':total_report_submitted_published,
        'total_pending_report':total_pending_report}




        return render(request, 'institution/institution_metrics.html',context)



     

