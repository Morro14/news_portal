from django.apps import AppConfig


class NewsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'news'

    def ready(self):
        import news.signals
#        from .tasks import send_mails
#        from .scheduler import mail_schedular
#        print('started')
#
#        mail_schedular.add_job(
#            id='send_mails',
#            func=send_mails,
#            trigger='interval',
#            seconds=10,
#
#        )
#        mail_schedular.start()
