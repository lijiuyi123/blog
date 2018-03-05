from django.urls import path
from blog import views
urlpatterns = [

    path('index/',views.IndexView.as_view()),
    #path('test/',views.get_name),
]
