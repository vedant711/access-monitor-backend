from django.urls import path

from . import views

# from rest_framework_simplejwt.views import (
#     TokenRefreshView,
# )
urlpatterns= [
    path('',views.index_home),
    path('login/',views.login_view),
    path('logout/',views.logout_view),

    path('access/<server>/',views.index_server_home),
    path('complete_logs/<server>/',views.complete_logs),
    path('show_custom/<server>/',views.show_custom),
    path('show_ipwise/<server>/',views.show_ipwise),
    # path('access/<server>/show_blocked/',views.blocked_ips),
    path('blockip/<server>/',views.block_ip),
    path('unblockip/<server>/',views.unblock_ips),
    path('firewall/<server>/',views.firewall),
    path('show-detailed/<server>/',views.show_detailed_codewise),
    path('unblockipfw/<server>/',views.unblock_ips_fw),

    # path('api/token/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    # path('api/test/', views.testEndPoint),


    # path('', views.getRoutes)




]

handler404 = 'views.error404'