from django.contrib.auth.base_user import BaseUserManager

class UserManager(BaseUserManager):
    use_in_migrations = True


    def create_user(self, netid, password=None, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not netid:
            raise ValueError('The given netid must be set')

        user = self.model(netid=(netid), **extra_fields)
        user.set_password(password)
        user.is_staff = False
        user.is_active = True
        user.is_superuser = False
        user.save(using=self._db)
        return user


    def create_superuser(self, netid, password, **extra_fields):
     """
     Creates and saves a superuser with the given netid, date of
     birth and password.
     """
     user = self.create_user(
        netid,
        password=password,
     )
     user.is_staff = True
     user.is_active = True
     user.is_superuser = True
     user.save(using=self._db)
     return user
