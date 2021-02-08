from django.apps import AppConfig


class AccountsConfig(AppConfig):
    '''Configurations for accounts app'''
    name = 'accounts'

    def ready(self):
        '''using signals to create dependencies'''
        import accounts.signals # noqa
