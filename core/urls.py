from django.urls import path
from core import views
urlpatterns = [
    path("", views.TaskList.as_view(), name="tasks"),
    path("task/<int:pk>/", views.TaskDetail.as_view(), name="task"),
    path("task-create/", views.TaskCreate.as_view(), name="task-create"),
    path("task-update/<int:pk>/", views.TaskUpdate.as_view(), name="task-update"),
    path("task-delete/<int:pk>/", views.TaskDelete.as_view(), name="task-delete"),
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", views.CustomLogoutView.as_view(), name="logout"),
    path("signup/", views.CustomUserCreate.as_view(), name="signup"),
]
