from django.urls import path
from . import views

app_name = "institution"
urlpatterns = [
    path("account/institution/set_up", views.institution_setup_register, name="institution_setup_register"),
    path("account/institution/welcome/home", views.institution_complete, name="institution_complete"),
    path("institution/<str:institutionname>/home", views.institution_dashboard, name="institution_dashboard"),
    path("institution/setting/setup/<str:institutionname>", views.institution_setting, name="institution_setting"),
    path("institution/setting/metrics/create", views.create_institution_metric, name="create_institution_metric"),
    path("institution/loan/view/applications/<str:institutionname>", views.institutions_all_loan_applications, name="institutions_all_loan_applications"),
    path("institution/business/view/reports/<str:institutionname>", views.all_submitted_business_report, name="all_submitted_business_report"),
    path("institution/report/business/view/submitted/records/<int:month_report_summary>", views.view_break_down_summary_monthly_report, name="view_break_down_summary_monthly_report"),
    path("institution/business/view/defaulters/<str:institutionname>", views.all_business_monthly_defaulters, name="all_business_monthly_defaulters"),
     path("institution/business/view/business/metrics/<str:institutionname>", views.institution_metrics, name="institution_metrics"),
]

