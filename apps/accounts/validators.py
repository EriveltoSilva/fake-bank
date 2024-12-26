""" validator account module"""

import re


def is_email_valid(email):
    """
    Função para validar um endereço de email.
    Args:
      email: O endereço de email a ser validado.
    Returns:
      True se o email for válido, False caso contrário.
    """
    regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-z]{2,7}$"  # Expressão regular para um email válido
    return re.match(regex, email)


def is_password_equal(password, confirmation_password):
    """return true if password is equal to confirmation"""
    return password == confirmation_password
