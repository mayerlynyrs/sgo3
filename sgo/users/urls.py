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
    # Crea el usuario
    path(
        route='create',
        view=views.create_user,
        name="create"
    ),
    path(
        route='<int:user_id>/create/', 
        view=views.UsersIdView.as_view(),
        name='create'
        ),
    path(
        route='<int:pk>/detail/',
        view=views.TrabajadorDetailView.as_view(),
        name='detail'
    ),
    path(
        route='<int:user_id>/update/',
        view=views.update_user,
        name="update"
    ),
    path(
        route='<int:user_id>/profile/',		
        view=views.update_profile,		
        name="profile"		
    ),
    # Crea el trabajador
    path(
        route='list-trabajador',
        view=views.TrabajadorListView.as_view(),
        name='list_trabajador'
     ),
    path(
        route='create-trabajador',
        view=views.create_trabajador,
        name="create_trabajador"
    ),
    path(
        route='<int:user_id>/create_trabajador/', 
        view=views.TrabajadoresIdView.as_view(),
        name='create_trabajador'
        ),
    path(
        route='<int:trabajador_id>/update_trabajador/',
        view=views.update_trabajador,
        name="update_trabajador"
    ),
    path(
        route='<int:user_id>/contactos/',
        view=views.ContactoView.as_view(),
        name='contactos'
     ),
    path(
        route='<int:user_id>/profesion_trabajadores/',
        view=views.ProfesionTrabajadorView.as_view(),
        name='profesion_trabajadores'
     ),
    path(
        route='<int:user_id>/archivo_trabajadores/',
        view=views.ArchivoTrabajadorView.as_view(),
        name='archivo_trabajadores'
     ),
    path(
        route='<int:user_id>/evaluacion_trabajadores/',
        view=views.EvaluacionUserView.as_view(),
        name='evaluacion_trabajadores'
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
        route='lista-negra',
        view=views.ListaNegraView.as_view(),
        name='lista_negra'
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
    
    
    path('ajax/load-plantas/', views.load_plantas, name='ajax_load_plantas'), # AJAX
]
