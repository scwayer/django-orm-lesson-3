import random

from django.core.exceptions import MultipleObjectsReturned
from django.core.exceptions import ObjectDoesNotExist

from datacenter.models import Schoolkid
from datacenter.models import Mark
from datacenter.models import Lesson
from datacenter.models import Chastisement
from datacenter.models import Commendation


commendations = [
    'Молодец!',
    'Отлично!',
    'Хорошо!',
    'Великолепно!',
    'Прекрасно!',
    'Очень хороший ответ!',
    'Так держать!']


def fix_marks(schollkid):
    Mark.objects.filter(schoolkid=schollkid, points__lte=3).update(points=5)


def remove_chastisements(schoolkid):
    Chastisement.objects.filter(schoolkid=schoolkid).delete()


def create_commendation(schoolkid, subject):
    try:
        child = Schoolkid.objects.get(full_name__contains=schoolkid)
    except MultipleObjectsReturned:
        print(f'Найдено несколько учеников с именем "{schoolkid}"')
    except ObjectDoesNotExist:
        print(f'Ученик с именем "{schoolkid}" не найден')

    lesson = Lesson.objects.filter(
        year_of_study=child.year_of_study,
        group_letter=child.group_letter,
        subject__title__contains=subject).order_by('-date').first()

    Commendation.objects.create(
        text=random.choice(commendations),
        created=lesson.date,
        schoolkid=child,
        subject=lesson.subject,
        teacher=lesson.teacher
    )


