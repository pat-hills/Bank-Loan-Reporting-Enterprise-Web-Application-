from django.urls import path
from . import views


app_name = "business"
urlpatterns = [
    path("account/business/set_up", views.business_setup_register, name="business_setup_register"),
    path("account/business/welcome/home", views.business_complete, name="business_complete"),
    path("business/<str:business_name>/home", views.business_dashboard, name="business_dashboard"),
    #path("business/<str:business_name>/loans", views.business_loans, name="business_loans"),
    path("business/loan/view/banks", views.business_bank_listing, name="business_bank_listing"),
    #path("institution/setting/setup/<str:institutionname>", views.institution_setting, name="institution_setting"),
    #path("institution/setting/metrics/create", views.create_institution_metric, name="create_institution_metric"),
]