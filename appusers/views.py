from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.urls import reverse
from django.db import IntegrityError
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
#from .managers import UserAccount
from django.contrib import messages 
#from repurta import securityuser
from repurta.securityuser import EmailAuthBackend,SecurityUserBusiness
from .services import *
from business.services import *

# Create your views here.


# user = None
# def current_user(request):
#     global user
#     user = request.user


def index(request):
    return render(request, "pages/index.html", {

    })


# @login_required
# @cache_control(no_cache=True, must_revalidate=True,no_store=True)
# def institution_setup(request):
#     return render(request, "institution/institution_setup.html", {

#     })


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("appusers:index"))


def institution_app_user_sign_up(request):

    if request.method == "POST":
        
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        confirmpassword = request.POST["confirmpassword"]
        account_type = "Bank"
        user_role = "FinancialAdmin"
        is_institution_setup = False
        username = email+"_"+firstname+"_"+lastname

        # Ensure password matches confirmation
        if password != confirmpassword:
            return render(request, "account/institution_user_sign_up.html", {
                "message": "Passwords must match!"
            })

        #user = User()

        user_email_qs = User.objects.filter(is_deleted=False, email=email).count()

        #user_email_qs = User.if_email_exist(email,email)

        if user_email_qs > 0 :

            return render(request, "account/institution_user_sign_up.html", {
               "message": "User account email already exist!"
           })
         
        
        #user_email_qs = UserAccount.objects.find_user_by_email(email)
        #if user_email_qs.exists():
            #return render(request, "account/institution_sign_up.html", {
               #"message": "User account email already exist!"
           # })

        
        user_save = User.objects.create_user(email=email,first_name = firstname,last_name = lastname,password=password,
        account_type = account_type,user_role = user_role,is_institution_setup = is_institution_setup,username=username)
        user_save.save()
          
       

        #request.session["user_id"] = user_save.id
        request.session["fullname"] = user_save.first_name +" "+ user_save.last_name  
        login(request, user_save)
        return HttpResponseRedirect(reverse('institution:institution_setup_register'))
    else:
        return render(request, "account/institution_user_sign_up.html", {

    })




def business_app_user_sign_up(request):

    if request.method == "POST":
        
        email = request.POST["email"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        password = request.POST["password"]
        confirmpassword = request.POST["confirmpassword"]
        account_type = "Business"
        user_role = "Business-Owner"
        is_institution_setup = False
        username = email+"_"+firstname+"_"+lastname

        # Ensure password matches confirmation
        if password != confirmpassword:
            return render(request, "account/business_user_sign_up.html", {
                "message": "Passwords must match!"
            })


        user_email_qs = User.objects.filter(is_deleted=False, email=email).count()

        #user_email_qs = User.if_email_exist(email,email)

        if user_email_qs > 0 :

            return render(request, "account/business_user_sign_up.html", {
               "message": "User account email already exist!"
           })
         
        
        #user_email_qs = UserAccount.objects.find_user_by_email(email)
        #if user_email_qs.exists():
            #return render(request, "account/institution_sign_up.html", {
               #"message": "User account email already exist!"
           # })

        
        user_save = User.objects.create_user(email=email,first_name = firstname,last_name = lastname,password=password,
        account_type = account_type,user_role = user_role,is_institution_setup = is_institution_setup,username=username)
        user_save.save()
          
       

        #request.session["user_id"] = user_save.id
        request.session["fullname"] = user_save.first_name +" "+ user_save.last_name  
        login(request, user_save)
        return HttpResponseRedirect(reverse('business:business_setup_register'))
    else:
        return render(request, "account/business_user_sign_up.html", {

    })




def login_business(request):

    if request.method == "POST":
        
        # Attempt to sign user in
        email = request.POST["email"]
        password = request.POST["password"]

        user_auth = securityuser.EmailAuthBackend.authenticate(securityuser.EmailAuthBackend,email=email,password=password)
       

        # Check if authentication successful
        if user_auth is not None:
            
            #We get the account type
            if user_auth.account_type == "Bank":
                if user_auth.is_institution:
                    login(request,user_auth)
                    user_institution = get_user_institution(request)
                    request.session['institution_slug_name'] = user_institution.slug
                    request.session['institution_name'] = user_institution.name
                    request.session['institution_location'] = user_institution.location
                    request.session['institution_tagline'] = user_institution.tagline
                    #request.session['institution_logo'] = user_institution.logo
                    request.session['institution_id'] = user_institution.id

                    #request.session["SecurityUser"] = loadSecurityUserFromUsr(request)
                    return HttpResponseRedirect(reverse("institution:institution_complete"))
                else:
                    login(request,user_auth)
                    #request.session["SecurityUser"] = loadSecurityUserFromUsr(request)
                    return HttpResponseRedirect(reverse("institution:institution_setup_register"))
            else:
                if user_auth.is_institution:
                    login(request,user_auth) 
                    #getting user business
                    user_business = get_user_business(request)
                    request.session['business_slug_name'] = user_business.slug
                    request.session['business_name'] = user_business.name
                    return HttpResponseRedirect(reverse("business:business_complete",))
                else:
                    login(request,user_auth)
                    loadSecurityUserBusiness(request)
                    return HttpResponseRedirect(reverse("business:business_setup_register"))
        else:
            return render(request, "account/login_business.html", {
                "message": "Invalid email or password."
            })
        
          

    else:
        title = "Repurta - User Login"
        return render(request, "account/login_business.html", {
            "title" :  title

    })

def password_reset_business(request):

    if request.method == "POST":
        
        email = request.POST["email"] 

       


         
          
       

        #request.session["user_id"] = user_save.id
        #request.session["fullname"] = user_save.first_name +" "+ user_save.last_name  
        #login(request, user_save)
        #return HttpResponseRedirect(reverse('business:business_setup_register'))
    else:

        page_title = 'Password Reset'
        return render(request, "account/password_reset_business.html", {

        'page_title':page_title 

         

    })
