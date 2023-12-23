from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from .models import News, Ad, LikePage, Category, Response
from .forms import AdForm, ResponseForm, NewsForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from django.urls import reverse

def my_view(request):
    DEFAULT_FROM_EMAIL = settings.DEFAULT_FROM_EMAIL
    # Далее ваш код представления

def index(request):
    return render(request, 'index.html')

class NewsListView(ListView):
    model = News
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-date']


class NewsDetail(DetailView):
    model = News
    template_name = 'news_detail.html'
    context_object_name = 'news_detail'


class Ads(ListView):
    model = Ad
    template_name = 'ads.html'
    context_object_name = 'ads'
    ordering = ['-date_create']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        return context

class AdsDetail(DetailView):
    model = Ad
    template_name = 'ads_detail.html'
    context_object_name = 'ads_detail'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset=queryset)
        # Инкрементируем просмотры каждый раз, когда страница открывается
        obj.views += 1
        obj.save()
        return obj


class AdPrivatePage(ListView):
    model = Ad
    template_name = 'ads_private.html'
    context_object_name = 'ads'
    ordering = ['-date_create']

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Ad.objects.filter(author=self.request.user)
        else:
            return Ad.objects.none()


class AdPrivateDetail(DetailView):
    model = Ad
    template_name = 'ads_private_detail.html'
    context_object_name = 'ads_detail'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.object
        context['responses'] = Response.objects.filter(ad=ad)
        return context


class AdLike(DetailView):
    model = LikePage
    template_name = 'ads_like.html'
    context_object_name = 'ads_like'

    def get_object(self, queryset=None):
        return get_object_or_404(LikePage, ad__id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        ad = self.object.ad
        context['responses'] = Response.objects.filter(ad=ad)
        return context


@login_required
def create_ad(request):
    if request.method == 'POST':
        form = AdForm(request.POST)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.author = request.user
            ad.views = 0
            ad.save()
            return redirect('ads_detail', pk=ad.pk)
    else:
        form = AdForm()

    categories = Category.objects.all()
    return render(request, 'create_ad.html', {'form': form, 'categories': categories})


@login_required
def create_response(request, ad_id):
    ad = get_object_or_404(Ad, id=ad_id)
    if request.method == 'POST':
        form = ResponseForm(request.POST)
        if form.is_valid():
            response = form.save(commit=False)
            response.ad = ad
            response.sender = request.user
            response.save()

            # Отправка уведомления по электронной почте
            send_mail(
                'Новый отклик на ваше объявление',
                f'Пользователь {request.user.username} оставил отклик на ваше объявление "{ad.title}".',
                settings.DEFAULT_FROM_EMAIL,  # Вместо DEFAULT_FROM_EMAIL используйте settings.DEFAULT_FROM_EMAIL
                [ad.author.email],
                fail_silently=False,
            )

            messages.success(request, 'Отклик успешно отправлен.')
            return redirect('ads_detail', pk=ad_id)
    else:
        form = ResponseForm()

    return render(request, 'create_response.html', {'form': form, 'ad': ad, 'DEFAULT_FROM_EMAIL': settings.DEFAULT_FROM_EMAIL})


@login_required
def user_responses(request):
    responses = Response.objects.filter(sender=request.user)
    return render(request, 'user_responses.html', {'responses': responses})


@login_required
def accept_response(request, ad_id, response_id):
    ad = get_object_or_404(Ad, id=ad_id)
    response = get_object_or_404(Response, id=response_id)

    # Изменяем статус на "принят"
    response.status = 'принят'
    response.save()

    messages.success(request, 'Отклик принят.')
    return redirect('ad_private_detail', pk=ad_id)

@login_required
def reject_response(request, ad_id, response_id):
    ad = get_object_or_404(Ad, id=ad_id)
    response = get_object_or_404(Response, id=response_id)

    # Изменяем статус на "отклонен"
    response.status = 'отклонен'
    response.save()

    messages.success(request, 'Отклик отклонен.')
    return redirect('ad_private_detail', pk=ad_id)


@login_required
def ad_private_detail(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    responses = Response.objects.filter(ad=ad)

    if request.method == 'POST':
        # Обработка удаления отклика
        response_id_to_delete = request.POST.get('response_id_to_delete')
        if response_id_to_delete:
            response_to_delete = get_object_or_404(Response, id=response_id_to_delete)
            response_to_delete.delete()
            messages.success(request, 'Отклик успешно удален.')
            return redirect('ad_private_detail', pk=pk)

    return render(request, 'ads_private_detail.html', {'ads_detail': ad, 'responses': responses})


@login_required
def delete_response(request, pk, response_id):
    ad = get_object_or_404(Ad, id=pk)
    response = get_object_or_404(Response, id=response_id, ad=ad)

    if request.method == 'POST':
        response.delete()
        messages.success(request, 'Отклик успешно удален.')

    return redirect('ad_private_detail', pk=pk)


def send_news_notification(request, news_id):
    news = get_object_or_404(News, pk=news_id)

    users = User.objects.all()

    for user in users:
        subject = f'Уведомление: {news.title}'
        message = f'Привет, {user.username}!\n\n' \
                  f'Новая новость: {news.title}\n\n' \
                  f'{news.text}\n\n' \
                  f'С уважением,\nВаш билборд'

        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

    return redirect(reverse('news_detail', args=[news_id]))