from django.urls import path
from blog import views
urlpatterns = [
    path('blog/<int:id>/',views.DetailBlogView.as_view(),name='detail'),
    path('category/<str:category_url>/',views.CategoryView.as_view(),name='category'),
    path('',views.IndexView.as_view(),name='index'),
]
