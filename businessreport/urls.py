from django.urls import path
from . import views


 
app_name = "businessreport"
urlpatterns = [
    path("report/business/new/submit", views.submit_business_report, name="submit_business_report"),
    path("report/business/submitted/records", views.all_submitted_business_report, name="all_submitted_business_report"),
    #path("report/business/view/records/month_report_summary", views.view_break_down_summary_monthly_report, name="view_break_down_summary_monthly_report"),
    path("report/business/view/records/<int:month_report_summary>", views.view_break_down_summary_monthly_report, name="view_break_down_summary_monthly_report"),
    path("report/business/edit/records/<int:month_report_summary>", views.edit_break_down_summary_monthly_report, name="edit_break_down_summary_monthly_report"),
    path("report/business/delete/records/<int:month_report_summary>", views.delete_monthly_report, name="delete_monthly_report"),
    path("report/business/charts/data/insights/<str:business_name>", views.view_business_charts_graphs_reports, name="charts_graphs_metrics"),
    path("report/business/view/metrics/<str:business_name>", views.view_business_metrics_progress, name="view_business_metrics_progress"),
    path("report/business/view/metric/name/<str:business_name>/<int:report_metric_id>", views.view_business_month_report_metric_progress_chart, name="view_business_month_report_metric_progress_chart"),

]