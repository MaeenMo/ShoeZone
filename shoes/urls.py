from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name='shoes-home'),
    path('men/', views.men, name='men'),
    path('women/', views.women, name='women'),
    path('search_shoes/', views.search_shoes, name='search_shoes'),
    path('register/', views.registration, name='register'),
    path('profile/', views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='shoes/sign_in.html', extra_context={'page_name': 'Sign In'}), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='shoes/sign_out.html'), name='logout'),
    path('cart/', views.cart, name='cart'),
    path('add_product/<int:xid>', views.add_To_Cart, name='add_product'),
    path('add_quantity/<int:hid>/<int:jid>', views.additional_size, name='add_quantity'),
    path('remove_product/<int:xid>', views.remove_From_Cart, name='remove_product'),
    path('remove_quantity/<int:xid>', views.remove_quantity, name='remove_quantity'),
    path('checkout/', views.checkout, name='checkout'),
    path('item/<int:myid>', views.item_page, name='item-page'),
    # Password Reset
    path('password-reset/', auth_views.PasswordResetView.as_view(template_name='shoes/forget_password.html'), name='password_reset'),
    path('password-reset/done/', auth_views.PasswordResetDoneView.as_view(template_name='shoes/pass_reset_done.html'), name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(success_url='/login/', template_name='shoes/pass_reset_confirm.html'), name='password_reset_confirm'),
    path('password-reset-complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Password Change
    path('password_change/', views.PasswordChange.as_view(template_name='shoes/password_change.html',  extra_context={'nav': True}), name='password_change'),

] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
