from django.urls import include,path
from django.contrib import admin
from .views import SignUpView
from . import views

urlpatterns = [
    path('', views.BgamesList,name='index'),
    path('search/',views.Search, name = 'search'),
    path('detail/<int:id>/',views.Detail),
    path('', include('django.contrib.auth.urls')), 
    path('signup/', SignUpView.as_view(), name='signup'),
    path('personal/', views.ShowFavoured, name='personal'),
    path('fav_game/<int:id>/',views.AddDelFavoured,name='fav_game'),
    path('rate_game/<int:id>/',views.AddUpdRate,name='rate_game'),
    path('admin/', admin.site.urls),
]