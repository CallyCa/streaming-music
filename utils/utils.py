def format_password(password):
    # Mostrar apenas a parte após pbkdf2:sha256:
    return ':'.join(password.split(':')[2:])