from django.core.management.base import BaseCommand

from user.models import User
from backend.customs.generators import generate_password


class Command(BaseCommand):
    help = "creates new admin(enter: name username password)"

    def add_arguments(self, parser):
        parser.add_argument("name", type=str)
        parser.add_argument("username", type=str)
        parser.add_argument("password", type=str)

    def handle(self, name: str, username: str, password: str = None, *args, **kwargs):
        if User.objects.filter(username__iexact=username).exists():
            return self.stdout.write(self.style.ERROR("user already exists"))
        if password is None:
            password = generate_password()
        user = User.objects.create(name=name, username=username)
        user.password = user.set_password(password=password)
        self.stdout.write(self.style.SUCCESS("new user created"))
