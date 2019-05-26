from django.urls import path, include
from main.views import attendanceView, getImagefromFeed
app_name='main'

urlpatterns = [
    path('attendance/', attendanceView, name='attendance'),
    path('imagefeed', getImagefromFeed, name='imagefeed'),
]