from django.urls import path

from . import views

urlpatterns=[

    path("",views.home,name="home"),
    path("calendar/",views.calendar_view,name="calendar"),
    path("clients/",views.client_view,name="clients")
]