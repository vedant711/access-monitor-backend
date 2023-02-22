from django.urls import path

from . import views
urlpatterns= [
    path('<server>/',views.index),
    path('<server>/show_custom/',views.show_custom),
    path('<server>/show_ipwise/',views.show_ipwise),
    path('<server>/show_blocked/',views.blocked_ips),
    path('<server>/blockip/',views.block_ip),
    path('<server>/unblockip/',views.unblock_ips),
    path('<server>/firewall/',views.firewall),
    path('<server>/show-detailed/',views.show_detailed_codewise),




]