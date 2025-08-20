from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_page, name='post_page'),
    path('publish/', views.publish_to_platforms, name='publish_to_platforms'),
    path('publish/twitter/', views.publish_to_twitter, name='publish_to_twitter'),
    path('linkedin/login/', views.linkedin_login, name='linkedin_login'),
    path('linkedin/callback/', views.linkedin_callback, name='linkedin_callback'),  # Ensure this line exists
]