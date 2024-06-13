from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q

class EmailBackend(ModelBackend):
    def authenticate(self, request, username=None, password=None, **kwargs):
        UserModel = get_user_model()
        user = None

        if username:
            query = Q(username=username) | Q(email=username) | Q(phone=username)
        else:
            email = kwargs.get('email')
            phone = kwargs.get('phone')
            if email:
                query = Q(email=email)
            elif phone:
                query = Q(phone=phone)
            else:
                return None

        try:
            user = UserModel.objects.get(query)
        except UserModel.MultipleObjectsReturned:
            return None
        except UserModel.DoesNotExist:
            return None

        if user and user.check_password(password):
            return user
        return None
