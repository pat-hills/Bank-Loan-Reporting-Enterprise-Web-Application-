from institution.models import Institution,InstitutionCustomMetric



def get_banks_in_users_region(region):
    banks_in_region = Institution.objects.filter(is_deleted=False,region=region)
    return banks_in_region

def get_institution_by_slug(slug):
    Institution_by_slug = Institution.objects.get(is_deleted=False,slug=slug)
    return Institution_by_slug


def get_institution_by_id_slug(id,slug):
    Institution_by_id = Institution.objects.get(is_deleted=False,pk=id,slug=slug)
    return Institution_by_id



def get_user_institution(request):
    try:
        user_institution = Institution.objects.get(is_deleted=False,user=request.user)
        return user_institution
    except Institution.DoesNotExist:
        return None

 


#def get_user_institution(request):
#    users_institution = Institution.objects.get(is_deleted=False,user=request.user)
#    return users_institution

def get_user_institution_custom_metrics(request):
    users_institution_custom_metric = InstitutionCustomMetric.objects.filter(is_deleted=False,created_by=request.user)
    return users_institution_custom_metric


def get_user_institution_by_id(id):
    users_institution = Institution.objects.get(pk=id)
    return users_institution


 