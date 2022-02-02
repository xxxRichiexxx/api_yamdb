from django.core.exceptions import ValidationError
import re


def validate_user(value):
    if value == 'me':
        raise ValidationError(
            f'Использовать имя {value} в качестве username запрещено.'
        )
    elif re.findall(r'[^\w.@+-]+', value):
        raise ValidationError(
            'Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.'
        )