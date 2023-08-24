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
    """ Обрабатываем тригонометрию """
    for oper in trigon:
        if oper in expression:
            expression = expression.replace(oper, f'math.{oper}')
            break
    return expression


def check_logs(expression):
    """ Обрабатываем логарифмы """
    for oper in logs:
        if oper in expression:
            expression = expression.replace(oper, f'math.{logs[oper]}')
            break
    return expression


def check_pow(expression):
    """ Обрабатываем возведение в степень """
    if '^' in expression:
        expression = expression.replace('^', '**')
    return expression


def replace_varies(expression, varies):
    """ Подставляем переменные """
    exp = list(expression)

    for var in varies:
        for i, symb in enumerate(exp):
            if symb == var:
                if i == 0:
                    if not exp[i+1].isalpha():
                        exp[i] = str(varies[var])
                elif 0 < i < len(exp)-1:
                    if not exp[i+1].isalpha() and not exp[i-1].isalpha():
                        exp[i] = str(varies[var])
                else:
                    if not exp[i-1].isalpha():
                        exp[i] = str(varies[var])
    expression = ''.join(exp)
    return expression


def calculation(expression, varies):
    """ Вычисляем ответ """
    expression = check_trigonometry(expression)
    expression = check_logs(expression)
    expression = check_pow(expression)
    expression = replace_varies(expression, varies)

    return {"result": eval(expression)}


def validate_vars(data):
    """ Проверяем наличие всех пременных """
    varies_in_expression = set()
    for v in data['expression']:
        if v.isalpha():
            s = re.search(
                r'(\W|^)%s(\W|$)' % (v, ), data['expression']
            )
            if s is not None:
                varies_in_expression.add(v)

    lost_vars = [v for v in varies_in_expression if v not in data['varies']]

    return lost_vars if lost_vars else False


@api_view(['GET', 'POST'])
def api_compute(request):
    """Обработка Гет и Пост запроса"""

    if request.method == 'POST':

        serializer = QuestionSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            lost_vars = validate_vars(serializer.data)
            if not lost_vars:

                try:
                    answer = calculation(
                        serializer.data['expression'],
                        serializer.data['varies']
                    )

                    serializer = AnswerSerializer(answer)
                    return Response(serializer.data, status=status.HTTP_200_OK)

                except ZeroDivisionError:
                    return Response(
                        AnswerSerializer(
                            {"error": ['Деление на 0']}
                        ).data,
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except NameError:
                    return Response(
                        AnswerSerializer(
                            {"error": ['Некорректное указание '
                                       'перемнных в выражении']}
                        ).data,
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except ValueError:
                    return Response(
                        AnswerSerializer(
                            {"error": ['Некорректное использование '
                                       'операций в выражении']}
                        ).data,
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except AttributeError:
                    return Response(
                        AnswerSerializer(
                            {"error": ['Некорректное наименование '
                                       'операций в выражении']}
                        ).data,
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except SyntaxError:
                    return Response(
                        AnswerSerializer(
                            {"error": ['Некорректный синтаксис']}
                        ).data,
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except TypeError:
                    return Response(
                        AnswerSerializer(
                            {"error": ['Некорректный тип данных']}
                        ).data,
                        status=status.HTTP_400_BAD_REQUEST
                    )
                except Exception:
                    return Response(
                        AnswerSerializer(
                            {"error": ['Неизвестная ошибка']}
                        ).data,
                        status=status.HTTP_400_BAD_REQUEST
                    )

            serializer = AnswerSerializer(
                {
                    "error": [f"Вы не указали переменную {lv}!"
                              for lv in lost_vars]
                }
            )
            return Response(
                serializer.data,
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            AnswerSerializer(
                {"error": [serializer.errors]}
            ).data,
            status=status.HTTP_400_BAD_REQUEST
        )
    return Response(QuestionSerializer().data)
