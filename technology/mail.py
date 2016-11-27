from django.conf import settings
from django.core.mail import EmailMessage


def send_mail(report):
    """
    :param report: отчет
    :return: отправка сообщения
    """
    msg = EmailMessage('Преподаватель проверил ' + str(report.laboratory),
                       '<div><p>Вас приведствует сайт Технологии Программирования</p>'
                       + "<p>Недавно преподователь просмотрел вашу работу " + str(report.laboratory) + '</p>'
                       + "<p><b>Итоги</b></p>"
                       + "<p><b>Оценка: </b>"+ str(report.price)+"</p>"
                       + "<p><b>Балл: </b>"+ str(report.rating)+"</p>"
                       + "<p><b>Комментарий: </b>"+str(report.note)+"</p>"
                       + '<p>Для просмотра прейдите по ссылке <a href=''>Посмотреть</a></p></div>',
                       settings.EMAIL_HOST_USER,
                       [report.user.user.email])
    msg.content_subtype = "html"
    msg.send()
