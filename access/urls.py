from django.urls import path

from . import views

from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
urlpatterns= [
    path('access/<server>/',views.index),
    path('access/<server>/show_custom/',views.show_custom),
    path('access/<server>/show_ipwise/',views.show_ipwise),
    path('access/<server>/show_blocked/',views.blocked_ips),
    path('access/<server>/blockip/',views.block_ip),
    path('access/<server>/unblockip/',views.unblock_ips),
    path('access/<server>/firewall/',views.firewall),
    path('access/<server>/show-detailed/',views.show_detailed_codewise),
    path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/test/', views.testEndPoint),


    path('', views.getRoutes)




]