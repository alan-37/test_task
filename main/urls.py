from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views



urlpatterns = [
    path('', views.ads_list, name='ads_list'),
    path('ads/<int:pk>/', views.ads_detail, name='ads_detail'),
    path('ads/create/', views.create_ad, name='create_ad'),
    path('ads/<int:pk>/edit/', views.edit_ad, name='edit_ad'),
    path('ads/<int:pk>/delete/', views.delete_ad, name='delete_ad'),
    path('proposals/send/<int:ad_receiver_id>/', views.send_proposal, name='send_proposal'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('proposal/<int:proposal_id>/accept/', views.accept_proposal, name='accept_proposal'),
    path('proposal/<int:proposal_id>/reject/', views.reject_proposal, name='reject_proposal'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)