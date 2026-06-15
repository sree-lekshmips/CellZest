from django.urls import path
from .import views




urlpatterns = [
    path('',views.home,name="home"),
    path('get-meal-plan/', views.get_meal_plan, name='get_meal_plan'),
    path('index/',views.index,name="index"),
    path('recommend_food/',views.recommend_food,name="recommend_food"),
    path('about/',views.about,name="about"),
    path('blog/',views.blog,name="blog"),
    path('contact/',views.contact,name="contact"),
    path('stories/',views.stories,name="stories"),

]
