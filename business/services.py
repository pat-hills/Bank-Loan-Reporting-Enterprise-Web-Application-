from .models import Business
from institution.models import Institution


def get_user_business(request):
    try:
        users_business = Business.objects.select_related("user").get(is_deleted=False,user=request.user)
        return users_business
    except Business.DoesNotExist:
            return None


 


def validate_user_business_by_contact(request):
    business_validation = Business.objects.filter(is_deleted=False,contact=request)
    return business_validation

#def get_banks_in_users_region(region):
 #   banks_in_region = Institution.objects.filter(is_deleted=False,region=region)
  #  return banks_in_region