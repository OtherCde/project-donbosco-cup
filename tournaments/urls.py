from django.urls import path
from . import views

app_name = 'tournaments'

urlpatterns = [
    path('', views.index, name='index'),
    # Aquí se agregarán las rutas específicas de tournaments
    # path('list/', views.tournament_list, name='tournament_list'),
    # path('<int:tournament_id>/', views.tournament_detail, name='tournament_detail'),
]
