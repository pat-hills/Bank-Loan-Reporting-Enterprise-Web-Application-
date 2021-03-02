from loan.models import Loan

from django.db.models import Sum
import datetime
from django.db.models import Count
from repurta.utils import *



def get_users_business_loans(business):
    users_business_loans = Loan.objects.filter(is_deleted=False,business=business).select_related("institution","user")
    return users_business_loans


def get_users_latest_loan_application(business):
    users_latest_loan = Loan.objects.filter(is_deleted=False,business=business,loan_status="UNPAID").last()
    return users_latest_loan


def get_loans_for_institutions(institution):
    loans_institutions = Loan.objects.filter(is_deleted=False,institution=institution).select_related("business","user")
    return loans_institutions




def authorize_business_loan_status(transaction_code,id,category_data,request):
    authorize_business_loan_status = Loan.objects.filter(is_deleted=False,transaction_code=transaction_code,id=id).update(loan_category=category_data,institution_action_by=request.user.first_name)
    return authorize_business_loan_status



#def get_user_business_active_institution_on_loan(request):
#    user_business_active_institution_on_loan = Loan.objects.select_related("institution","user").get(is_deleted=False,loan_status="UNPAID",loan_category="AUTHORIZE",user=request.user)
#   return user_business_active_institution_on_loan




def get_user_business_active_institution_on_loan(request):
    try:
        user_business_active_institution_on_loan = Loan.objects.prefetch_related("institution","user").get(is_deleted=False,loan_status="UNPAID",loan_category="AUTHORIZE",user=request.user)
        #user_business_active_institution_on_loan = Loan.objects.prefetch_related("institution","user").get(is_deleted=False,loan_status="UNPAID",loan_category="AUTHORIZE",user=request.user)
        return user_business_active_institution_on_loan
    except Loan.DoesNotExist:
        return False


# BEGIN LOANS METRICS START

def get_total_amount_loan_applied_current_year(institution):

    try:
          today = datetime.datetime.now()
          current_year = today.year
          #current_month = today.month
          total_loan = Loan.objects.filter(is_deleted=False,institution=institution,date_created__year = current_year).aggregate(loan_sum=Sum('amount'))
    
    except Loan.DoesNotExist:
        total_loan = None
    return total_loan


def get_total_loans_applied(institution):

    try:
          today = datetime.datetime.now()
          current_year = today.year
          #current_month = today.month
          total_loans_applied = Loan.objects.filter(is_deleted=False,institution=institution,date_created__year = current_year).count()
    
    except Loan.DoesNotExist:
        total_loans_applied = None
    return total_loans_applied



def get_total_authorized_loans(institution):

    try:
          today = datetime.datetime.now()
          current_year = today.year
          #current_month = today.month
          total_loans_applied = Loan.objects.filter(is_deleted=False,institution=institution,date_created__year = current_year,loan_category=loan_authorized_value).count()
    
    except Loan.DoesNotExist:
        total_loans_applied = None
    return total_loans_applied


def get_total_denied_loans(institution):

    try:
          today = datetime.datetime.now()
          current_year = today.year
          #current_month = today.month
          total_loans_rejected = Loan.objects.filter(is_deleted=False,institution=institution,date_created__year = current_year,loan_category=loan_denied_value).count()
    
    except Loan.DoesNotExist:
        total_loans_rejected = None
    return total_loans_rejected


def get_total_amount_loan_applied_current_year_authorized(institution):

    try:
          today = datetime.datetime.now()
          current_year = today.year
          #current_month = today.month
          total_loan_authorized = Loan.objects.filter(is_deleted=False,institution=institution,date_created__year = current_year,loan_category=loan_authorized_value).aggregate(loan_auth_sum=Sum('amount'))
    
    except Loan.DoesNotExist:
        total_loan_authorized = None
    return total_loan_authorized


def get_total_amount_loan_applied_current_year_denied(institution):

    try:
          today = datetime.datetime.now()
          current_year = today.year
          #current_month = today.month
          total_loan_authorized = Loan.objects.filter(is_deleted=False,institution=institution,date_created__year = current_year,loan_category=loan_denied_value).aggregate(loan_denied_sum=Sum('amount'))
    
    except Loan.DoesNotExist:
        total_loan_authorized = None
    return total_loan_authorized






# END

 


