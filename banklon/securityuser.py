from django.contrib.auth.backends import ModelBackend
from appusers.models import User


class EmailAuthBackend(ModelBackend):
    """
    Email Authentication Backend

    Allows a user to sign in using an email/password pair, then check
    a username/password pair if email failed
    """

    def authenticate(self, email=None, password=None):
        """ Authenticate a user based on email address as the user name. """
        try:
            user = User.objects.get(email=email)
            if user.check_password(password):
                return user
        except User.DoesNotExist:
                return None

    

class SecurityUserBusiness:
    #User = None
    #UserId = 0
    #UserEmail = ""
    #UserAccountType = ""
    #UserRole = ""
    #UserFirstname = ""
    #UserLastname = ""
    UserBusinessName = ""
    UserBusinessSlug = "" 
    UserBusinessId = 0 
    #UserBusiness = None 


    def __init__(self,_UserBusinessName,_UserBusinessSlug,_UserBusinessId): 
        self.UserBusinessName = _UserBusinessName
        self.UserBusinessSlug = _UserBusinessSlug
        self.UserBusinessId = _UserBusinessId




class SecurityUserInstitution:
    User = None
    UserId = 0
    UserEmail = ""
    UserAccountType = ""
    UserRole = ""
    UserFirstname = ""
    UserLastname = ""
    UserBusinessName = ""
    UserBusinessSlug = ""
    UserInstitutionName = ""
    UserInstitutionSlug = ""
    UserBusinessId = 0
    UserInstitutionId = 0
    UserBusiness = None
    UserInstitution = None


    def __init__(self, _User ,_UserId,_UserEmail,_UserAccountType,_UserRole,_UserFirstname,_UserLastname,
        _UserBusinessName,_UserBusinessSlug,_UserInstitutionName,_UserInstitutionSlug,_UserBusinessId,_UserInstitutionId,_UserBusiness,_UserInstitution): 
        self.User = _User
        self.UserId = _UserId 
        self.UserEmail = _UserEmail 
        self.UserAccountType = _UserAccountType
        self.UserRole = _UserRole
        self.UserFirstname = _UserFirstname
        self.UserLastname = _UserLastname
        self.UserBusinessName = _UserBusinessName
        self.UserBusinessSlug = _UserBusinessSlug
        self.UserInstitutionName = _UserInstitutionName
        self.UserInstitutionSlug = _UserInstitutionSlug
        self.UserBusinessId = _UserBusinessId
        self.UserInstitutionId = _UserInstitutionId
        self.UserBusiness = _UserBusiness
        self.UserInstitution = _UserInstitution

    
