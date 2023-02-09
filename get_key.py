from django.core.management.utils import get_random_secret_key


if __name__ == '__main__':
    with open('.env', 'w') as env:
        env.write(F'SECRET_KEY=\'{get_random_secret_key()}\'')
