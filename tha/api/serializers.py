import re

from rest_framework import serializers


class QuestionSerializer(serializers.Serializer):
    expression = serializers.CharField(
        initial='Write your expression, for example: lg(5*a+2*b)'
    )
    varies = serializers.DictField(
        initial='{Write your variables in dict format}'
    )

    def validate_varies(self, value):
        if not all(map(lambda x: x.isalpha(), list(value.keys()))):
            raise serializers.ValidationError("Variables keys must be alpha!")
        if not all(map(lambda x: len(x) == 1, list(value.keys()))):
            raise serializers.ValidationError(
                "Variables keys must be 1 symb length!"
            )
        if not all(map(lambda x: x.isdigit(), list(value.values()))):
            raise serializers.ValidationError(
                "Variables values must be digits!"
            )
        return value

    def validate(self, data):
        varies_in_expression = set()
        for v in data['expression']:
            if v.isalpha():
                if re.search(
                    r'(\W|^)%s(\W|$)' % (v, ), data['expression']
                ) is not None:
                    varies_in_expression.add(v)
        for v in varies_in_expression:
            if v not in data['varies']:
                raise serializers.ValidationError(
                    "You forgot to send all variables!"
                )
        return data


class AnswerSerializer(serializers.Serializer):
    result = serializers.CharField()
    error = serializers.ErrorDetail(string='seems like error')
