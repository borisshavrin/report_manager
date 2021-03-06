from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.shortcuts import render, HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.utils.decorators import method_decorator
from django.views.generic import CreateView, UpdateView

from users.forms import UserProfileForm, UserProfileEditForm, UserRegisterForm, UserLoginForm
from users.models import User


class UsersLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'users/login.html'

    def get_context_data(self, **kwargs):
        context = super(UsersLoginView, self).get_context_data(**kwargs)
        context['title'] = 'UWCA_Manager - Авторизация'
        return context


class UsersRegisterView(SuccessMessageMixin, CreateView):
    template_name = 'users/register.html'
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')
    success_message = 'Успешная регистрация!'

    def get_context_data(self, **kwargs):
        context = super(UsersRegisterView, self).get_context_data(**kwargs)
        context['title'] = 'UWCA_Manager - Авторизация'
        return context

    def form_valid(self, form):
        user = form.save()
        verify_link = reverse('users:verify', args=[user.email])
        self.success_url = verify_link
        return super(UsersRegisterView, self).form_valid(form)


def verify(request, email):
    try:
        user = User.objects.get(email=email)
        user.is_active = True
        user.save()
        auth.login(request, user)
        return render(request, 'index')
    except Exception as err:
        print(f'error activation user {err.args}')
        return HttpResponseRedirect(reverse('index'))


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


class UsersProfileView(SuccessMessageMixin, UpdateView):
    template_name = 'users/profile.html'
    success_url = 'users:profile'
    success_message = 'Данные успешно изменены!'
    form_class = UserProfileForm
    model = User
    template_name_suffix = '_update_form'

    def get(self, request, *args, **kwargs):
        return self.render_to_response(
            {'userprofileform': UserProfileForm(prefix='userprofileform_pre',
                                                instance=request.user),
             'userprofileeditform': UserProfileEditForm(prefix='userprofileeditform_pre',
                                                        instance=request.user.userprofile)}
        )

    def get_context_data(self, **kwargs):
        context = super(UsersProfileView, self).get_context_data(**kwargs)
        if self.request.method == 'POST':
            userprofileform = UserProfileForm(self.request.POST,
                                              instance=self.request.user,
                                              prefix='userprofileform_pre')
            userprofileeditform = UserProfileEditForm(self.request.POST,
                                                      instance=self.request.user.userprofile,
                                                      prefix='userprofileeditform_pre')
            if userprofileform.is_valid() and userprofileeditform.is_valid():
                userprofileform.save()
                return context
        else:
            userprofileform = UserProfileForm(instance=self.request.user)
            userprofileeditform = UserProfileEditForm(instance=self.request.user.userprofile)

        context['title'] = 'UWCA_Manager - Личный кабинет'
        context['userprofileform'] = userprofileform
        context['userprofileeditform'] = userprofileeditform
        return context

    def get_success_url(self):
        return reverse_lazy(self.success_url, args=(self.request.user.pk,))

    @method_decorator(login_required())
    def dispatch(self, request, *args, **kwargs):
        return super(UsersProfileView, self).dispatch(request, *args, **kwargs)
