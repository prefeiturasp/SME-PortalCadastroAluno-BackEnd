from django.core import validators


phone_validation = validators.RegexValidator(
    regex=r"^\d{9}$",
    message="Necessário 9 digitos",
)

cpf_validation = validators.RegexValidator(
    regex=r"^\d{11}$",
    message="Necessário 11 digitos",
)
