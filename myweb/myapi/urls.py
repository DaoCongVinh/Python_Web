from django.urls import re_path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [
    # 2 URLs: 1 cái cho đăng nhập (lấy token, gửi username/password lên)
    # Trả về tới 2 token: access (dùng truy cập) và refresh (dùng để gia hạn khi access bị expired)
    # URL dùng để lấy access token mới từ refresh

    re_path(r"^token$", jwt_views.TokenObtainPairView.as_view(), name='get_token'),
    re_path(r"^token/refresh$",jwt_views.TokenRefreshView.as_view(), name='get_refresh_token'),
    re_path(r'^pets$', views.api_list_pets, name = 'api_list_pets'),
    re_path(r"^pet/detail/(?P<pet_id>[\w]+)$", views.api_detail_pets, name='api_detail_pets'),
    re_path(r'^pet/add$', views.api_add_pet, name = 'api_add_pet'),
    re_path(r"^pet/update/(?P<pet_id>[\w]+)$", views.api_update_pet, name='api_update_pet'),
    re_path(r"^pet/delete/(?P<pet_id>[\w]+)$", views.api_delete_pet, name='api_delete_pet'),

]