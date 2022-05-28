from django.urls import path, include

from reports.views import reports, choose

app_name = 'reports'

urlpatterns = [
    path('', reports, name='index'),
    path('choose', choose, name='choose'),
]
