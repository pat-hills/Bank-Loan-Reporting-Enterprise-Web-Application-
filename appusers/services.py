# from django.contrib.auth.models import AbstractUser, UserManager

from repurta.securityuser import SecurityUserBusiness
from business.services import *
from institution.services import *
from appusers.models import User


# class UserAccountManager(UserManager):
    
#     def find_by_username(self, username):
#         queryset = self.get_queryset()
#         return queryset.filter(username=username)


#     def find_user_by_email(self, email):
#         queryset = self.get_queryset()
#         return queryset.filter(email=email)


#     def get_user_details_by_email(self, email):
#         queryset = self.get_queryset()
#         return queryset   



# class UserAccount(AbstractUser):
#     objects = UserAccountManager()

def loadSecurityUserBusiness(request):
    
    user_business = get_user_business(request)
    #user_institution = get_user_institution(request)
    #request.session['user'] = request.user
    #request.session['user_id'] = request.user.id
    #request.session['user_email'] = request.user.email
    #request.session['user_account_type'] = request.user.account_type
    #request.session['user_role']= request.user.user_role
    #request.session['user_first_name'] = request.user.first_name
    #request.session['user_last_name'] = request.user.last_name
    request.session['user_business_name'] = user_business.name
    request.session['user_business_slug']= user_business.slug
    request.session['user_business_id'] = user_business.id 
    #request.session['user_business'] = user_business
    security_data = SecurityUserBusiness(request.session['user_business_name'],request.session['user_business_slug'],request.session['user_business_id'])
    return security_data

