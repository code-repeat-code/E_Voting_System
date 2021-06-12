from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path,include
from django.conf import settings
from . import views
urlpatterns = [
    path('',views.home,name="home"),
    path('register',views.register,name="register"),
    path('login',views.view_login,name="view_login"),
    path('logout',views.view_logout,name="view_logout"),
    path('candidate/<int:pos>/',views.candidate_view,name="candidate_view"),
    path('positions',views.position_view,name="position_view"),
    path('result',views.result,name="result"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)