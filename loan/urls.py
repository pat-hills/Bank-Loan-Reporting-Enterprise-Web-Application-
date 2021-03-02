from django.urls import path
from . import views


app_name = "loan"
urlpatterns = [
    path("loans/business/<str:bank_name>/institution/<int:bank_id>/apply", views.business_loan_application, name="business_loan_application"), 
    path("loans/business/<str:bank_slug>/institution/<int:bank_id>/apply/begin/application", views.business_loan_application_begin, name="business_loan_application_begin"), 
    path("loans/<str:business_name>/business", views.business_loans, name="business_loans"),
    path("loans/view/business/application/<str:transaction_code>/loan/<int:id>", views.business_loan_view, name="business_loan_view"),
    #path("loans/business/apply/<str:bank_name>/<int:bank_id>", views.business_loan_application, name="business_loan_application"), 
]