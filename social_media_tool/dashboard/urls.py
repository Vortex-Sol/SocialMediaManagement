from django.urls import path

from . import views

urlpatterns = [
    path('', views.post_page, name='post_page'),
    path('publish/twitter/', views.publish_to_twitter, name='publish_to_twitter'),

]
