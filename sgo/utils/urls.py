"""Utils urls."""

# Django
from django.urls import path
from django.contrib.auth import views as auth_views
from utils import views


urlpatterns = [
    # # Management
    # path(
    #     route='',
    #     view=views.ProfesionListView.as_view(),
    #     name='list_profesion'
    #  ),
    # path(
    #     route='<int:planta_id>/',
    #     view=views.ProfesionListView.as_view(),
    #     name='list_profesion'
    # ),
    # path(
    #     route='<int:profesion_id>/update/',
    #     view=views.update_profesion,
    #     name="update"
    # ),
    # path(
    #     route='create_profesion',
    #     view=views.create_profesion,
    #     name="create_profesion"
    # ),
    # path(
    #     route='<int:profesion_id>/detail/',
    #     view=views.detail_profesion,
    #     name="detail"
    # ),
    # path(
    #     route='<int:object_id>/delete/',
    #     view=views.delete_profesion,
    #     name="delete"
    # ),
]
