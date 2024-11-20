"""
Definition of urls for DjangoWebProject1.
"""

from datetime import datetime
from django.urls import path
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from app import forms, views

from django.conf.urls.static import static #импорт функций для настройки доступа к загруженным файлам
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings

urlpatterns = [
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('about/', views.about, name='about'),
    path('login/',
         LoginView.as_view
         (
             template_name='app/login.html',
             authentication_form=forms.BootstrapAuthenticationForm,
             extra_context=
             {
                 'title': 'Авторизация',
                 'year' : datetime.now().year,
             }
         ),
         name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('admin/', admin.site.urls),
    path('links/', views.links, name='links'),  #для Полезные ссылки
    path('pool/', views.pool, name='pool'),  #для Обратная связь
    path('registration/', views. registration, name= 'registration'), #регистрация
    path('blog/', views.blog, name='blog'), #для веб-страницы со списком постов
    path('blogpost/<int:parametr>/', views.blogpost, name='blogpost'), #добавить на веб-сайт страницу поста
    path('newpost/', views.newpost, name='newpost'), # для страницы добавления статьи блога
    path('videopost/', views.videopost, name='videopost'), # для видео
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #строки шаблонов URL для загрузки файлов в папку media, вложенной в папку проекта
urlpatterns += staticfiles_urlpatterns()