from django.urls import path
from blog import views
urlpatterns = [
    path('blog/<int:blogid>/',views.detailblogview,name='detail'),
    path('',views.IndexView.as_view(),name='index'),
]
