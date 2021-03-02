from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from .models import Loan
from businessreport.models import *
from business.services import *
from institution.services import * 
from loan.services import *
import hashlib

from django.contrib import messages


# Create your views here.

@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def business_loan_application(request,bank_name,bank_id):

    #if request.method == "POST":

         
    #    loanamount = request.POST["loanamount"]
    #    bank_name = request.POST["bank_name"]
    #    bank_id = request.POST["bank_id"]
    #    termofloan = request.POST["termofloan"]
    #    business_number = request.POST["business_number"]
    #    Reason = request.POST["Reason"]
    #    businessCertificate = request.FILES["businessCertificate"]

    #    mystring = request.user.username
    #    hash_obj = hashlib.md5(mystring.encode())
    #    transaction_code= hash_obj.hexdigest()



    #    users_business = get_user_business(request)
    #    applied_institution = get_institution_by_id_slug(bank_id,bank_name)

        
    #    business_loan = Loan.objects.create(amount=loanamount,reason = Reason,transaction_code = transaction_code,business_number=business_number,
    #    term_of_loan=termofloan,business_certificate=businessCertificate,user = request.user, business=users_business,institution = applied_institution)
    #    business_loan.save()

    #    messages.add_message(request, messages.SUCCESS, 'Successfully applied for business loan!.')
    #    return HttpResponseRedirect(reverse("loan:business_loans",args=(users_business.slug,)))
        
 
    #else:
        context = {'bank_name' : bank_name,'bank_id' : bank_id,}
        return render(request, 'loan/business_loan_application.html',context)



@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def business_loan_application_begin(request,bank_slug,bank_id):

    if request.method == "POST":

         
        loanamount = request.POST["loanamount"]
        bank_name = request.POST["bank_name"]
        bank_id = request.POST["bank_id"]
        termofloan = request.POST["termofloan"]
        business_number = request.POST["business_number"]
        Reason = request.POST["Reason"]
        businessCertificate = request.FILES["businessCertificate"]

        mystring = request.user.username
        hash_obj = hashlib.md5(mystring.encode())
        transaction_code= hash_obj.hexdigest()



        users_business = get_user_business(request)
        applied_institution = get_institution_by_id_slug(bank_id,bank_name)

        
        business_loan = Loan.objects.create(amount=loanamount,reason = Reason,transaction_code = transaction_code,business_number=business_number,
        term_of_loan=termofloan,business_certificate=businessCertificate,user = request.user, business=users_business,institution = applied_institution)
        business_loan.save()

        messages.add_message(request, messages.SUCCESS, 'Successfully applied for business loan!.')
        return HttpResponseRedirect(reverse("loan:business_loans",args=(users_business.slug,)))
        
 
    else:
        context = {'bank_slug' : bank_slug,'bank_id' : bank_id,}
        return render(request, 'loan/business_loan_application_begin.html',context)



@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def business_loans(request,business_name):
    user_business = get_user_business(request)
    users_business_loans = get_users_business_loans(user_business)
    user_latest_application = get_users_latest_loan_application(user_business)

     
       #return HttpResponseRedirect(reverse("business:business_loans",args=( request.session["business_name"],)))

    
    return render(request, "loan/business_loans.html",{
        "users_business_loans" :users_business_loans,
        "user_latest_application" :user_latest_application,
     })



@login_required
@cache_control(no_cache=True, must_revalidate=True,no_store=True)
def business_loan_view(request,transaction_code,id):
    if request.method == "POST":

        loan_action = request.POST["loan_action"]
        id = request.POST["id"]
        transaction_code = request.POST["transaction_code"]

        user_institution = get_user_institution(request)
        user_institution_custom_metric = get_user_institution_custom_metrics(request)
        user_business = get_loans_by_transaction_code_id(transaction_code,id) #we need to check if this is valid before we proceed to anything
        

        if not user_business:
            messages.add_message(request, messages.ERROR, 'Failed performing action on loan application!')
            return HttpResponseRedirect(reverse("institution:institutions_all_loan_applications",args=(user_institution.slug,)))
        else:

            authorized_deny_application = authorize_business_loan_status(transaction_code,id,loan_action,request)

            if authorized_deny_application:
                for data in user_institution_custom_metric:
                    ReportMetric.objects.create(business=user_business.business,institution=user_institution,institution_custom_metric=data)
                     
            messages.add_message(request, messages.SUCCESS, 'Successfully applied action on loan!.')
            return HttpResponseRedirect(reverse("institution:institutions_all_loan_applications",args=(user_institution.slug,)))
        
 
    else:
        loans_transactions = get_loans_by_transaction_code_id(transaction_code,id)
        context = {'loans_transactions' : loans_transactions}
        return render(request, 'institution/institution_business_loan_view.html',context)
    





           

