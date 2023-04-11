import math
import re

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .serializers import AnswerSerializer, QuestionSerializer

trigon = ('asin', 'acos', 'atan', 'sin', 'cos', 'tan')
logs = {
    'ln': 'log',
    "lg": 'log10'
}


def check_trigonometry(expression):
    """Обрабатываем тригонометрию"""
    for oper in trigon:
        if oper in expression:
            expression = expression.replace(oper, f'math.{oper}')
            break
    return expression


def check_logs(expression):
    """Обрабатываем логарифмы"""
    for oper in logs:
        if oper in expression:
            expression = expression.replace(oper, f'math.{logs[oper]}')
            break
    return expression


def check_pow(expression):
    """Обрабатываем возведение в степень"""
    if '^' in expression:
        expression = expression.replace('^', '**')
    return expression


def replace_varies(expression, varies):
    """Подставляем переменные"""
    for v, x in varies.items():
        area = re.search(r'(\W|^){}(\W|$)'.format(v), expression)
        if area:
            area_left, area_right = area.span()[0], area.span()[1] + 1
            expression = expression[:area_left] \
                + expression[area_left: area_right].replace(v, x) \
                + expression[area_right:]
    return expression


def calculation(expression, varies):
    """Вычисляем ответ"""
    expression = check_trigonometry(expression)
    expression = check_logs(expression)
    expression = check_pow(expression)
    expression = replace_varies(expression, varies)
    return {"result": eval(expression)}


@api_view(['GET', 'POST'])
def api_compute(request):
    """Обработка Гет и Пост запроса"""
    if request.method == 'POST':
        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            answer = calculation(
                serializer.data['expression'],
                serializer.data['varies']
            )
            serializer = AnswerSerializer(answer)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    return Response(QuestionSerializer().data)
