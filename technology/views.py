from django.contrib.auth import authenticate, logout, login
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from .forms import DocumentForm, ReportForm
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.core.exceptions import ObjectDoesNotExist

from .models import *


# Create your views here.

def Login(request):
    """
    Авторизация пользователя
    :param request:
    :return: admin
    :return: main
    :return: Аккаунт не существует
    """
    next_page = request.GET.get('next', '/main/')
    admin = request.GET.get('admin', '/groups')
    if request.user.is_authenticated():
        if request.user.is_staff:
            return HttpResponseRedirect(admin)
        return HttpResponseRedirect(next_page)
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                if user.is_staff:
                    return HttpResponseRedirect(admin)
                return HttpResponseRedirect(next_page)
            else:
                return HttpResponse("Аккаунт не существует.")
        else:
            return HttpResponseRedirect('/')
    return TemplateResponse(request, 'login.html', {'next': next_page, 'admin': admin})


def Logout(request):
    """
    Выход из системы
    :param request:
    :return:
    """
    logout(request)
    return HttpResponseRedirect('/')


def home(request):
    """
    Страница чата и отправки лаб
    :param request:
    :return:
    """
    context = {'u': request.user}
    context['g'] = UserGroup.objects.get(user=context['u'])
    context['c'] = Chat.objects.filter(group=context['g'].group)
    context['labs'] = Laboratory.objects.filter(group=context['g'].group, variant=context['g'].variant)
    context['reports'] = Report.objects.filter(user=context['g'])
    if request.method == 'POST':
        form = DocumentForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                change = Report.objects.get(user=context['g'], laboratory_id=request.POST.get('id'))
                change.report = request.FILES['docfile']
                change.save()
            except ObjectDoesNotExist:
                newdoc = Report(report=request.FILES['docfile'], user=context['g'],
                                laboratory_id=request.POST.get('id'))
                newdoc.save()
            return redirect(home)
    else:
        form = DocumentForm()
    return TemplateResponse(request, 'student/main.html', context)


def chat(request, id):
    """
        Чат преподавателя c студентами
    :param request:
    :param id: id группы
    :return:
    """
    context = {'g': Group.objects.get(id=id)}
    context['c'] = Chat.objects.filter(group=context['g'])
    return TemplateResponse(request, 'teacher/chat.html', context)


def post(request):
    """
    Отправка сообщений на сервер
    :param request:
    :return:
    """
    if request.method == "POST":
        msg = request.POST.get('msgbox', None)
        group = request.POST.get('group', None)
        g = Group(id=group)
        c = Chat(user=request.user, message=msg, group=g)
        if msg != '':
            c.save()
        return JsonResponse({'msg': msg, 'user': c.user.username})
    else:
        return HttpResponse('Request must be POST.')


def messages(request):
    """
        Метод получения изображений
        :param request:
        :return:
    """
    context = {'u': request.user}
    context['g'] = UserGroup.objects.get(user=context['u'])
    context['chat'] = Chat.objects.filter(group=context['g'].group)
    return TemplateResponse(request, 'student/messages.html', context)


def groups(request):
    """
        Учительская админка.
            Выдает список групп.
        :param request:
        :return:  404
        :return:  шаблон teacher/students.html
    """
    if request.user.is_staff:
        context = {'userGroup': Group.objects.all()}
        return TemplateResponse(request, 'teacher/groups.html', context)
    else:
        return Http404('<h1>Page not found</h1>')


def students(request, id):
    """
        Список студетов выбранной группы.
        :param request:
        :param id: id группы
        :return:  404
    """
    if request.user.is_staff:
        context = {'students': UserGroup.objects.filter(group_id=id).order_by('variant'),
                   'group': Group.objects.get(id=id)}
        return TemplateResponse(request, 'teacher/students.html', context)
    else:
        return Http404('<h1>Page not found</h1>')


def student(request, id, id_group):
    """
        Список лабораторных работы студента
        :param id_group: id группы
        :param request:
        :param id: id студента
        :return:
    """
    if request.user.is_staff:
        context = {'report': Report.objects.filter(user__id=id), 'user': UserGroup.objects.get(user__chat=id),
                   'group': Group.objects.get(id=id_group)}
        return TemplateResponse(request, 'teacher/student.html', context)
    else:
        return Http404('<h1>Page not found</h1>')


def laboratory(request, id, id_group, id_student):
    """
        Лабараторная работа студента
        :param id: id отчета
        :param id_student: id студента
        :param id_group:  id группы
        :param request:
        :return:
    """
    if request.user.is_staff:
        context = {'laboratory': Report.objects.get(id=id)}
        context['form'] = ReportForm(instance=context['laboratory'])
        context['choices'] = STATUS_CHOICES
        if request.POST:
            forms = ReportForm(request.POST, instance=context['laboratory'])
            forms.save()
            return redirect(student, id_group, id_student)
        return TemplateResponse(request, 'teacher/laboratory.html', context)
    else:
        return Http404('<h1>Page not found</h1>')
