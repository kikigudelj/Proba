from django.urls import path

from . import views
from .views import home,new_drive,list_of_drives, singup_view,user_dashboard, profile, driver_dashboard, detail, set_status,accept_drive_and_change_seats

urlpatterns = [
   path("", home, name="home"),
   path("new_drive/", new_drive, name="new_drive"),
   path("list_of_drives/", list_of_drives, name="list_of_drives"),
   path('<int:drive_id>/', detail, name="detail"),
   path("singup/", singup_view, name="singup"),
   path("dashboard/", user_dashboard, name="user_dashboard"),
   path("driver_dashboard/", driver_dashboard, name="driver_dashboard"),
   path('accept_drive/<int:application_id>/', views.accept_drive_and_change_seats, name='accept_drive_and_change_seats'),
   path('set_status/<int:drive_id>/', views.set_status, name='set_status'),
   path("profile/", profile, name="profile"),
]