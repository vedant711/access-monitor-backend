from django.urls import path

from . import views
urlpatterns= [
    path('',views.index),
    path('show_custom',views.show_custom),
    path('show_ipwise',views.show_ipwise),
    path('show_blocked',views.blocked_ips),
    path('blockip',views.block_ip),
    path('unblockip',views.unblock_ips),
    path('firewall',views.firewall),



]