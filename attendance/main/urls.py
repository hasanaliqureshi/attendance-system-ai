from django.urls import path, include
from main.views import attendanceView, getImagefromFeed, surveillance, getImageForAttendance
app_name='main'

urlpatterns = [
    path('surveillance/', attendanceView, name='attendance'),
    path('attendance/', surveillance, name='surveillance'),
    path('imagefeed', getImagefromFeed, name='imagefeed'),
    path('attfeed', getImageForAttendance, name='attfeed'),
]