from django.urls import path

from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("calendar/", views.calendar_view, name="calendar"),
    path("clients/", views.client_view, name="clients"),
    path("jobs/", views.jobs, name="jobs"),
    path("jobs/<str:job_id>", views.job_detail),
    path("tasks/", views.tasks, name="tasks"),
    path("tasks/<str:task_id>", views.task_detail),
]
