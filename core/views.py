from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from core.models import Task
from django.shortcuts import redirect
from django import forms
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin


class CustomLoginView(LoginView):
    template_name = "core/login.html"
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy("tasks")


class CustomUserCreate(CreateView):
    form_class = UserCreationForm
    template_name = "core/new_user.html"
    success_url = "/"

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect("tasks")
        return super().get(*args, **kwargs)


class CustomLogoutView(LogoutView):
    next_page = "/"


class TaskList(LoginRequiredMixin, ListView):
    template_name = 'core/task_list.html'
    model = Task
    context_object_name = "tasks"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tasks'] = context['tasks'].filter(user=self.request.user)
        context['count'] = context['tasks'].filter(complete=False).count()
        search_input = self.request.GET.get("search") or ""
        if search_input:
            context['tasks'] = context['tasks'].filter(
                title__icontains=search_input)
        context['search_input'] = search_input
        return context


class TaskDetail(LoginRequiredMixin, DetailView):
    model = Task
    template_name = "core/task.html"
    context_object_name = 'task'


class TaskCreate(LoginRequiredMixin, CreateView):
    template_name = "core/task_create.html"
    fields = ['title', 'description']
    model = Task
    success_url = reverse_lazy('tasks')

    def form_valid(self, form):
        # it is to make sure that the user is logged in user that create the task
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self):
        form = super().get_form()
        form.fields['title'].widget = forms.TextInput(
            attrs={"required": True})
        form.fields['description'].widget = forms.Textarea(
            attrs={"required": True})
        return form


class TaskUpdate(LoginRequiredMixin, UpdateView):
    template_name = "core/update.html"
    fields = "__all__"
    model = Task

    success_url = reverse_lazy("tasks")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class TaskDelete(LoginRequiredMixin, DeleteView):
    model = Task
    context_object_name = "task"
    success_url = reverse_lazy("tasks")
