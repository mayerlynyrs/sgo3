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
    path(
        route='<int:pk>/detail/',
        view=views.UserDetailView.as_view(),
        name='detail'
    ),
    path(
        route='list_profesion',
        view=views.ProfesionListView.as_view(),
        name='list_profesion'
     ),
    path(
        route='create_profesion',
        view=views.create_profesion,
        name="create_profesion"
    ),
    path(
        route='<int:profesion_id>/update_profesion/',
        view=views.update_profesion,
        name="update_profesion"
    ),
    path(
        route='list_especialidad',
        view=views.EspecialidadListView.as_view(),
        name='list_especialidad'
     ),
    path(
        route='create_especialidad',
        view=views.create_especialidad,
        name="create_especialidad"
    ),
    # path(
    #     route='<int:user_id>/add_contacto/',
    #     view=views.add_contacto_user,
    #     name="add_contacto"
    # ),
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
