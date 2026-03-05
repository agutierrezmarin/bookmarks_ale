from django.contrib.auth import get_user_model


class EmailAuthBackend:
    # Autentificacion usando cuenta de email Gmail
    def authenticate(self, request, username=None, password=None):
        UserModel = get_user_model()
        try:
            user = UserModel.objects.get(email=username)
            if user.check_password(password):
                return user
            return None
        except (UserModel.DoesNotExist, UserModel.MultipleObjectsReturned):
            return None

    def get_user(self, user_id):
        UserModel = get_user_model()
        try:
            return UserModel.objects.get(pk=user_id)
        except UserModel.DoesNotExist:
            return None
