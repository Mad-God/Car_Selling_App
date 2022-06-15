from celery import shared_task
from .models import User
from django.core.mail import send_mail

@shared_task(bind=True)
def test_func(self):
    print(self)
    print(type(self))
    print(dir(self))
    print(self.__dir__)
    for i in range(10):
        print(i)
    return "Done"



@shared_task(bind=True)
def send_promoitonal_mails(self, a, b):
    all_users = User.objects.all()
    all_user_emails = [x.email for x in all_users]
    print(all_user_emails, f"a={a}; b={b}")
    for i in all_users:
        print(f"send_mail to {i.email}")
    # send mail here
    send_mail(
        subject = f'Visit Car Selling . com for car related business.',
        message = f'''
        Hello {i.username}, 
        Please visit our site Car_Selling to buy cars at greate prices or to sell your old car easily and without hassle.
        Regards,
        Karan, 
        Sheikh Brothers Agency.
        ''',
        from_email = 'satansin2001@gmail.com',
        recipient_list = all_user_emails,
        fail_silently=False,
        )
    return "Done"

