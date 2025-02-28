from django.urls import path
from .views import (
    main_view, home, become_teacher, menu, teacher_detail, profile_view,
    edit_profile, chat_with_teacher, toggle_favorite, my_teacher_profile,
    my_teacher_ads, edit_teacher_ad, delete_teacher_ad, chat_list
)
from .views import deposit_balance
from .views import shop_view, buy_item, purchase_history
from .views import shop_view, add_shop_item
from .views import customize_profile


urlpatterns = [
    path('', main_view, name='main'),
    path('home/', home, name='home'),
    path('my_profile/', profile_view, name='my_profile'),
    path('become-teacher/', become_teacher, name='profile'),
    path('menu/', menu, name='menu'),
    path('teacher/<int:teacher_id>/', teacher_detail, name='teacher_detail'),
    path('edit-profile/', edit_profile, name='edit_profile'),
    path('chat/<int:teacher_id>/', chat_with_teacher, name='chat_with_teacher'),
    path('toggle-favorite/<int:teacher_id>/', toggle_favorite, name='toggle_favorite'),
    path('teacher/profile/', my_teacher_profile, name='my_teacher_profile'),
    path('teacher/ads/', my_teacher_ads, name='my_teacher_ads'),
    path('teacher/ads/edit/<int:teacher_id>/', edit_teacher_ad, name='edit_teacher_ad'),
    path('teacher/ads/delete/<int:teacher_id>/', delete_teacher_ad, name='delete_teacher_ad'),  # ✅ Новый маршрут
    path('chats/', chat_list, name='chat_list'),
    path('deposit/', deposit_balance, name='deposit'),
    path('shop/', shop_view, name='shop'),
    path('shop/buy/<int:item_id>/', buy_item, name='buy_item'),
    path('shop/history/', purchase_history, name='purchase_history'),
path('shop/add/', add_shop_item, name='add_shop_item'),
    path('customize_profile/', customize_profile, name='customize_profile'),

]
