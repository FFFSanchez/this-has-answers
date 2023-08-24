from rest_framework import serializers


def check_var_alpha(vars):
    ers = [var for var in vars if not var.isalpha()]
    return ers if ers else False


def check_var_len(vars):
    ers = [var for var in vars if not len(var) == 1]
    return ers if ers else False


class QuestionSerializer(serializers.Serializer):
    expression = serializers.CharField(
        initial='Напишите выражение, например: lg(5*a+2*b)',
        error_messages={
            'blank': 'Выражение не должно быть пустым',
            'required': 'Поле обязательно к отправке'
        }
    )
    varies = serializers.DictField(
        child=serializers.FloatField(
            error_messages={'invalid': 'Допустимы только float числа'}
        ),
        initial='Напишите переменные в формате словаря',
        error_messages={'required': 'Поле обязательно к отправке'}
    )

    def validate_varies(self, value):

        check_alpha = check_var_alpha(value.keys())
        if check_alpha:
            raise serializers.ValidationError(
                {v: "Переменная должна быть буквой!" for v in check_alpha}
            )

        check_len = check_var_len(value.keys())
        if check_len:
            raise serializers.ValidationError(
                {v: "Переменная должна быть 1 буквой!" for v in check_len}
            )

        return value


class AnswerSerializer(serializers.Serializer):
    result = serializers.CharField(default=None)
    error = serializers.ListField(required=False)
