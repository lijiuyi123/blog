from django.urls import path
from blog import views
urlpatterns = [
    path('blog/<int:blogid>/',views.detailblogview,name='detail'),
    path('learn/',views.LearnView.as_view(),name = 'learn'),
    path('life/',views.LifeView.as_view(),name = 'life'),
    path('',views.IndexView.as_view(),name='index'),

]
