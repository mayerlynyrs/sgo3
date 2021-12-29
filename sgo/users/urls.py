"""Users urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from users import views


urlpatterns = [
    # Management
    path(
        route='signin/',
        view=views.SignInView.as_view(),
        name='signin'
    ),
    path(
        route='logout/',
        view=auth_views.LogoutView.as_view(next_page='/users/signin/'),
        name='logout'
    ),
    path(
        route='',
        view=views.UserListView.as_view(),
        name='list'
     ),
    path(
        route='<int:planta_id>/',
        view=views.UserListView.as_view(),
        name='list'
    ),
    path(
        route='<int:user_id>/update/',
        view=views.update_user,
        name="update"
    ),
    path(
        route='<int:user_id>/attribute/',
        view=views.update_a_user,
        name="attribute"
    ),
    # Crea el usuario
    path(
        route='create',
        view=views.create_user,
        name="create"
    ),
    # Crea el contacto/profesion/documentos del usuario
    path(
        route='<int:user_id>/create/',
        view=views.users_create,
        name="create"
    ),
    # user
    path(
        route='<int:user_id>/user/', 
        view=views.UsersIdView.as_view(),
        name='user'
        ),
    path(
        route='<int:user_id>/profesion_users/',
        view=views.ProfesionUserView.as_view(),
        name='profesion_users'
     ),
    path(
        route='<int:user_id>/archivo_users/',
        view=views.ArchivoUserView.as_view(),
        name='archivo_users'
     ),
    path(
        route='<int:pk>/detail/',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    path(
        route='profesion',
        view=views.ProfesionView.as_view(),
        name='profesion'
     ),
    # especialidad
    path(
        route='especialidad',
        view=views.EspecialidadView.as_view(),
        name='especialidad'
     ),
    path(
        route='change_password/',
        view=views.PasswordChangeView.as_view(),
        name='change_password'
    ),
    path(
        route='admin/<int:user_id>/change_password/',
        view=views.admin_change_password,
        name='admin_change_password'
    ),
    path(
        route='<int:user_id>/contrato/',
        view=views.generar_contrato_usuario,
        name='generar_contrato'
    ),
    
    
    path('ajax/load-provincias/', views.load_provincias, name='ajax_load_provincias'), # AJAX
    
    
    path('ajax/load-ciudades/', views.load_ciudades, name='ajax_load_ciudades'), # AJAX
    
    
    path('ajax/load-negocios/', views.load_negocios, name='ajax_load_negocios'), # AJAX
]
