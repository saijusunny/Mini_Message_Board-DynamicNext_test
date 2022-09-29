from django.http import HttpResponseForbidden
from django.shortcuts import redirect, render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView, FormMixin
from django.urls import reverse_lazy, reverse
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from . import models
# Create your views here.
from .forms import ChatForm


class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('chatusers')


class SignupPage(FormView):
    template_name = 'base/signup.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('chatusers')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(SignupPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('chatusers')
        return super(SignupPage, self).get(*args, **kwargs)




class ChatUsers(FormMixin, ListView):
    model = models.Chat
    form_class = ChatForm
    template_name = 'base/user_chats.html'

    def get_success_url(self):
        return reverse('chatusers')

    def get(self,request,*args,**kwargs):
        context={"Chat":models.Chat.objects.all().filter(user=request.user)}
        print("1111")
        context["form"] = ChatForm()
        return render(request,"base/user_chats.html",context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.method=="POST":
            message=self.request.POST["message"]
            print(message)
            obj = models.Chat(user=self.request.user, message=message)
            obj.save()
            return redirect("chatusers")
        print("2222")
        return super().form_valid(form)

class ChatAllUsers(FormMixin, ListView):
    model = models.Chat
    form_class = ChatForm
    template_name = 'base/user_all_chats.html'

    def get_success_url(self):
        return reverse('chatusers')

    def get(self, request, *args, **kwargs):
        context = {"Chat": models.Chat.objects.all().filter()}
        context["form"]=ChatForm()
        print("1111")
        return render(request, "base/user_all_chats.html", context)

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return HttpResponseForbidden()

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        if self.request.method=="POST":
            message=self.request.POST["message"]
            obj=models.Chat(user=self.request.user,message=message)
            obj.save()
            return redirect("chatusers")
        return super().form_valid(form)

