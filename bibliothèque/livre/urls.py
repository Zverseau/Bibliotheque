from django.urls import path
from . import views


urlpatterns = [
    path('home', views.home, name='home'),
    path('ajouter',views.ajouterLivre, name='ajouter'),
    path('modifier/<int:livre_id>/', views.modifierInfoLivre, name='modifier_livre'), 
    path('LeLivre/<int:livre_id>/', views.livre_detail, name='livre_detail'),
    path('supprimer/<int:livre_id>/', views.supprimer_livre, name='supprimer_livre'),
    path('emprunter/<int:livre_id>/', views.emprunter_livre, name='emprunter_livre'),
    path('emprunteurs/', views.liste_emprunteurs, name='liste_emprunteurs'),
    path('modifierEmprunt/<int:emprunt_id>/', views.modifier_emprunt, name='modifierEmprunt'),
    path('register/', views.register, name='register'),
    path('', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
]

