
from django.urls import path
from .views import *
urlpatterns = [
    path('home/',home_page),    
    path('profile/',profile_page),
    path('create_poll/',create_poll),
    path('get_poll/<str:id>',get_poll),
    path('handle_ans/<str:id>/<int:ans>',handle_ans),
    path('del_poll/<str:id>',del_pol),
    path('del_24/',del_24hrs_poll),
]
