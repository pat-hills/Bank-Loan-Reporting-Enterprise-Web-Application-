from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Business
from .utils import greetings
from .services import *
from institution.services import *
from loan.services import *
import datetime
from django.contrib import messages
from appusers.models import User
from repurta.securityuser import SecurityUserBusiness

# Create your views here.


@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def business_setup_register(request):

    if request.method == "POST":
        
        #date_of_founding
        name = request.POST["name"]
        location = request.POST["location"] 
        contact = request.POST["contact"]
        tagline = request.POST["tagline"]
        country = request.POST["country"]
        region = request.POST["region"]
        industry = request.POST["industry"]
        #date_of_founding = request.POST["date_of_founding"]
        businessLogo = request.FILES["businessLogo"]
        date_of_founding = datetime.datetime.now().date()


        #Testing if contact of business exist

        business_contact_qs = validate_user_business_by_contact(contact).count()

        if business_contact_qs > 0 :

            return render(request, "business/business_setup.html", {
               "message": "Business contact account already exist!"
           })
        

        save_user_business = Business.objects.create(name=name,tagline = tagline,location = location,country=country,
        region = region,contact=contact,industry=industry,logo = businessLogo,date_of_coperation=date_of_founding,user=request.user)
        save_user_business.save()
        User.complete_institution_setup(User,request.user)
        request.session["business_name"] = save_user_business.name
        request.session['business_slug_name'] = save_user_business.slug
        #request.session["institution_id"] = save_user_business.id
        
        return HttpResponseRedirect(reverse("business:business_complete"))
    else:
        return render(request, "business/business_setup.html", {
           

    })

@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def business_complete(request):
    #users_institution = Institution.objects.get(is_deleted=False,user=request.user)
    users_business = get_user_business(request)
    return render(request, "business/business_welcome_home.html",{
         "greetings" : greetings,
         "users_business" : users_business, 
     })


@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def business_dashboard(request,business_name):
    #request.session['business_slug_name'] = business_name
    #we checking if user is valid to submit a report

    user_business = get_user_business(request)

    user_status_loan = get_user_business_active_institution_on_loan(request)
    users_latest_loan_status = get_users_latest_loan_application(user_business)

    return render(request, "business/business_dashboard.html",{
         "greetings" : greetings,
         "user_status_loan" : user_status_loan,
          "users_latest_loan_status" : users_latest_loan_status
     })


##@login_required
#@cache_control(no_cache=True, must_revalidate=True,no_store=True)
#def business_loans(request,business_name):
    #users_business_loans = get_users_business_loans(request)
    #user_latest_application = get_users_latest_loan_application(request)

     
       #return HttpResponseRedirect(reverse("business:business_loans",args=( request.session["business_name"],)))

    
    #return render(request, "business/business_loans.html",{
        #"users_business_loans" :users_business_loans,
       # "user_latest_application" :user_latest_application,
     #})


@login_required(login_url="appusers:login_business")
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def business_bank_listing(request):

    users_business_region = get_user_business(request)
    users_banks_in_region = get_banks_in_users_region(users_business_region.region)
    return render(request, "business/business_bank_list.html",{
        "users_banks_in_region" : users_banks_in_region,
     })
