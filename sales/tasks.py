from celery import shared_task
from .models import User
from django.core.mail import send_mail

@shared_task(bind=True)
def test_func(self):
    print("\n\n\n\n\Test_task1:\n")
    print(self)
    print(type(self))
    print(dir(self))
    print(self.__dir__)
    for i in range(10):
        print(i)
    return 3



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

@shared_task(bind=True)
def schedule_mails(self, a, b):
    all_users = User.objects.all()
    all_user_emails = [x.email for x in all_users]
    print(all_user_emails, f"a={a}; b={b}")
    for i in all_users:
        print(f"send_mail to {i.email}")
    # send mail here
    send_mail(
        subject = f'{str(a)}',
        message = f'''
        Hello {i.username}, 
        {b}
        Regards,
        Karan, 
        Sheikh Brothers Agency.
        ''',
        from_email = 'satansin2001@gmail.com',
        recipient_list = all_user_emails,
        fail_silently=False,
        )
    return "Done"



@shared_task(bind=True)
def test_func2(self, a,b):
    print("\n\n\n\n\Test_task2:\n")
    for i in range (a+b):
        print(i)
    return a+b


# subasks in a task
@shared_task(bind=True)
def test_func3(self, a,b):
    print("\n\n\n\n\Test_task3:\n")
    
    # manually calling; not allowed to call .get() for a task inside another task
    # res1 = test_func.delay().get()
    # res2 = test_func2.delay(a=4,b=5).get()
    # return f"res1:{res1}, res2:{res2}"

    # 2 chained tasks
    # chain = test_func.s() | test_func2.s(4)
    
    # single sub-task
    chain = test_func2.s(2,3)
    
    x = chain()
    return x

