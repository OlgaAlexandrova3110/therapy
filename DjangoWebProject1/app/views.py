"""
Definition of views.
"""

from datetime import datetime
from django.shortcuts import render
from django.http import HttpRequest
from django.contrib.auth.forms import UserCreationForm #использование встроенной формы регистрации 
from django.shortcuts import render, redirect #импорта функции render еще и импортом функции redirect

from django.db import models  #для блога
from .models import Blog #блог

from .models import Comment # использование модели комментариев
from .forms import CommentForm # использование формы ввода комментария

from .forms import BlogForm # код импорта формы для ввода статьи блога


def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Главная',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Контакты',
            'message':'Страница с нашими контактами.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'О нас',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )

#для Полезные ресурсы
def links(request):
    return render(request, 'app/links.html')


#для Обратная связь
from .forms import FeedbackForm #Обратная связь

def pool(request):
    assert isinstance(request, HttpRequest)
    data = None
    gender = {'1': 'Женщина', '2': 'Мужчина'}
    coffee = {'1': 'каждый день', '2': 'несколько раз в день',
              '3': 'несколько раз в неделю', '4': 'несколько раз в месяц'}
    rating = {'1': '1', '2': '2', '3': '3', '4': '4', '5': '5' }
    if request.method == 'POST':
        form = FeedbackForm(request.POST)
        if form.is_valid():
            data = dict()
            data['name'] = form.cleaned_data['name']
            data['city'] = form.cleaned_data['city']
            data['coffee'] = coffee[form.cleaned_data['coffee'] ]
            data['gender'] = gender[form.cleaned_data['gender'] ]
            if(form.cleaned_data['notice'] == True):
                data['notice'] = 'Да'
            else:
                data['notice'] = 'Нет'
            data['email'] = form.cleaned_data['email']
            data['rating'] = rating[form.cleaned_data['rating'] ]
            data['suggestions'] = form.cleaned_data['suggestions']
            form = None
    else:
        form = FeedbackForm()
    return render(
        request,
        'app/pool.html',
        {
            'form':form,
            'data': data
         }
    )

#метод действия контроллера registration 
#для обработки данных и передачи данных с сервера 
#для отображения шаблона веб-страницы регистрации

def registration(request):
    """Renders the registration page."""

    if request.method == "POST": # после отправки формы
        regform = UserCreationForm (request.POST)
        if regform.is_valid(): #валидация полей формы
            reg_f = regform.save(commit=False) # не сохраняем автоматически данные формы
            reg_f.is_staff = False # запрещен вход в административный раздел
            reg_f.is_active = True # активный пользователь
            reg_f.is_superuser = False # не является суперпользователем
            reg_f.date_joined = datetime.now() # дата регистрации
            reg_f.last_login = datetime.now() # дата последней авторизации
            reg_f.save() # сохраняем изменения после добавления данных
            return redirect('home') # переадресация на главную страницу после регистрации
    else:
        regform = UserCreationForm() # создание объекта формы для ввода данных нового пользователя
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/registration.html',
        {
            'regform': regform, # передача формы в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )

def blog(request):
    """Renders the blog page."""
    assert isinstance(request, HttpRequest)
    posts = Blog.objects.all() # запрос на выбор всех статей блога из модели
    return render(
        request,
        'app/blog.html',
        {
            'title':'Блог',
            'posts': posts, # передача списка статей в шаблон веб-страницы
            'year':datetime.now().year,
        }
    )


def blogpost(request, parametr):
    """Renders the blogpost page."""
    assert isinstance(request, HttpRequest)
    post_1 = Blog.objects.get(id=parametr) # запрос на выбор конкретной статьи по параметру
    comments = Comment.objects.filter(post=parametr)

    if request.method == "POST": # после отправки данных формы на сервер методом POST
        form = CommentForm(request.POST)
        if form.is_valid():
            comment_f = form.save(commit=False)
            comment_f.author = request.user # добавляем (так как этого поля нет в форме) в модель Комментария (Comment) в поле автор авторизованного пользователя
            comment_f.date = datetime.now() # добавляем в модель Комментария (Comment) текущую дату
            comment_f.post = Blog.objects.get(id=parametr) # добавляем в модель Комментария (Comment) статью, для которой данный комментарий
            comment_f.save() # сохраняем изменения после добавления полей
            return redirect('blogpost', parametr=post_1.id) # переадресация на ту же страницу статьи после отправки комментария
    else:
        form = CommentForm() # создание формы для ввода комментария
    return render(
        request,
        'app/blogpost.html',
        {
            'post_1': post_1, # передача конкретной статьи в шаблон веб-страницы

            'comments': comments, # передача всех комментариев к данной статье в шаблон веб-страницы
            'form': form, # передача формы добавления комментария в шаблон веб-страницы

            'year':datetime.now().year,
        }
    )



# код метода действия контроллера def newpost(request): 
def newpost(request):
    """Renders the newpost page."""
    assert isinstance(request, HttpRequest)

    if request.method == "POST": # после отправки формы
        blogform = BlogForm(request.POST, request.FILES)
        if blogform.is_valid():
            blog_f = blogform.save(commit=False)
            blog_f.posted = datetime.now()
            blog_f.autor = request.user
            blog_f.save()    # сохраняем изменения после добавления полей

            return redirect('blog')    # переадресация на страницу Блог после создания статьи Блога
    else:
        blogform = BlogForm()     # создание объекта формы для ввода данных

    return render(
        request,
        'app/newpost.html',
        {
            
            'blogform': blogform,     # передача формы в шаблон веб-страницы
            'title': 'Добавить статью блога',
            
            'year':datetime.now().year,
        }
    )

def videopost(request):
    """Renders the videopost page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/videopost.html',
        {
            'title':'Видео',
            'message':'Сведения о нас.',
            'year':datetime.now().year,
        }
    )
