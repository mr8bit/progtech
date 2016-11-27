from django.db import models
from ckeditor.fields import RichTextField
from django.contrib.auth.models import User
import datetime
from .mail import send_mail


class Chat(models.Model):
    """
        Сообщение из чата
        Поля:
            Дата создания
            От пользователя
            Сообщение
            Группа пользователя
    """
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)
    message = models.CharField(max_length=200)
    group = models.ForeignKey('Group', default='')

    def __str__(self):
        return self.message


class Group(models.Model):
    """
        Группа
        Поля:
            Факультет
            Номер группы
    """
    departament = models.CharField(max_length=300, verbose_name='Кафедра')
    name = models.CharField(max_length=300, verbose_name="Наименование")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = "Группы"


STATUS_CHOICES = (
    ('Не зачет', 'Не зачет'),
    ('Удволитворительно', 'Удволитворительно'),
    ('Хорошо', 'Хорошо'),
    ('Отлично', 'Отлично'),
)


def make_upload_path(instance,filename):
    """
    Создание загрузочной папки
    :param instance:
    :param filename:
    :return:
    """
    filename = str(datetime.datetime.now()) + "_" + filename
    return u'reports/%s/%s' % (instance.user.user, filename)


class Report(models.Model):
    """
        Отчет по лаборатоной
        Поля:
            Лабораторная - ForeignKey - Laboratory
            Пользователь - ForeignKey
            Отчет - FileField
            Балл - IntegerField
            Оценка - CharField
            Замечания - TextField
            Дата создания - DateTimeField
    """
    laboratory = models.ForeignKey('Laboratory', default='', related_name="reports", verbose_name='Отчеты')
    user = models.ForeignKey('UserGroup', default='', verbose_name="Студенты")
    report = models.FileField(upload_to=make_upload_path, verbose_name="Отчет")
    rating = models.IntegerField(default=1, blank=True, null=True, verbose_name="Баллы")
    price = models.CharField(choices=STATUS_CHOICES, max_length=300, blank=True, null=True, verbose_name="Оценка")
    note = models.TextField(verbose_name="Комментарий", default="", blank=True, null=True)
    date_create = models.DateTimeField(auto_now_add=True,  null=True, blank=True)

    def __str__(self):
        return self.laboratory.name

    class Meta:
        verbose_name = 'Отчет'
        verbose_name_plural = "Отчеты"
        ordering = ['-date_create']

    def save(self, *args, **kwargs):
        """
        :param args:
        :param kwargs:
        :return:
        """
        if self.pk is not None:
            original = Report.objects.get(pk=self.pk)
            if original.report != self.report:
                self.note = ''
                self.date_create = datetime.datetime.now()
            send_mail(self)
        super(Report, self).save(*args, **kwargs)


class Laboratory(models.Model):
    """
        Лабораторная работа
        Поля:
            Название работы
            Описание
            Максимальный бал
            Вариант
            Группа
    """
    name = models.CharField(max_length=300, verbose_name="Название")
    description = RichTextField(verbose_name="Описание")
    max_rating = models.IntegerField(default=1, verbose_name="Максимальный балд")
    variant = models.IntegerField(default=0, verbose_name="Вариант")
    group = models.ForeignKey('Group', default=0, verbose_name="Группа")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Лабораторная работа'
        verbose_name_plural = "Лабораторные работы"


class UserGroup(models.Model):
    """
        Пользователь в группе
        Поля:
            Пользователь
            Группа
            Вариант
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Студенты")
    group = models.ForeignKey('Group', verbose_name="Группа")
    variant = models.IntegerField(default=0, verbose_name="Вариант")

    def __str__(self):
        return self.user.last_name + ' ' + self.user.first_name

    class Meta:
        ordering = ['-variant']
        verbose_name = 'Студент'
        verbose_name_plural = "Студенты"
