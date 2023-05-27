import json
import uuid

from django.contrib.auth import login
from django.db.models import Avg, Count
from django.shortcuts import redirect, render, reverse
from datetime import datetime

from beatycity import settings
from beatycity.settings import API_KEY, SHOP_ID
from users.models import SMSCode, User
from .models import (
    Master,
    Review,
    Salon,
    Service,
    ServiceSignUp,
    ServiceType,
    AvailableDateTime,
)
from yookassa import Configuration, Payment

def show_home(request):
    template = "beautycity/index.html"

    salons = Salon.objects.all()
    services = Service.objects.all()
    masters = Master.objects.annotate(avg_stars=Avg('review__number_of_stars'), reviews_number=Count('review'))
    reviews = Review.objects.all()

    context = {
        'salons': salons,
        'services': services,
        'masters': masters,
        'reviews': reviews
    }

    if request.method == "POST" and "num1" not in request.POST:
        if request.body:
            body_data = json.loads(request.body)
            phone_number = request.session['phone_number'] = body_data["phone_number"]
            try:
                user, _ = User.objects.get_or_create(username=phone_number,
                                                     phone_number=phone_number)
                SMSCode.objects.filter(client=user).delete()
                SMSCode.objects.create(number='1234', client=user)
            except:
                print('Неправильный номер телефона')

    if request.method == "POST" and "num1" in request.POST:
        user = User.objects.get(
            phone_number=request.session['phone_number'])
        code = SMSCode.objects.get(client=user)

        code_text = (
                request.POST.get('num1')
                + request.POST.get('num2')
                + request.POST.get('num3')
                + request.POST.get('num4')
        )

        if code.number == code_text:
            login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])
            code.delete()
            if user.is_manager:
                return redirect("beauty:manager")
            return redirect("beauty:notes")
        else:
            print("wrong_code")
    return render(request, template, context)


def show_notes(request):
    template = "beautycity/notes.html"

    signups_and_dates = {}
    paid_sum = 0
    for signup in ServiceSignUp.objects.select_related('service', 'master', 'salon').filter(user=request.user):
        month_number = int(str(signup.datetime.datetime)[5:7])
        if month_number == 1:
            month = 'января'
        elif month_number == 2:
            month = 'февраля'
        elif month_number == 3:
            month = 'марта'
        elif month_number == 4:
            month = 'апреля'
        elif month_number == 5:
            month = 'мая'
        elif month_number == 6:
            month = 'июня'
        elif month_number == 7:
            month = 'июля'
        elif month_number == 8:
            month = 'августа'
        elif month_number == 9:
            month = 'сентября'
        elif month_number == 10:
            month = 'октября'
        elif month_number == 11:
            month = 'ноября'
        elif month_number == 12:
            month = 'декабря'
        else:
            month = ''

        formatted_date = str(signup.datetime.datetime)[8:10] + ' ' + month + ' - ' + str(signup.datetime.datetime)[
                                                                                     11:16]
        signups_and_dates[signup] = formatted_date
        if not signup.paid:
            paid_sum += signup.service.price

    context = {
        'signups_and_dates': signups_and_dates,
        'paid_sum': paid_sum,
    }

    return render(request, template, context)


def show_service(request):
    template = "beautycity/service.html"

    service_types = ServiceType.objects.all()
    salons = Salon.objects.all()
    masters = Master.objects.all()
    dates = AvailableDateTime.objects.all()

    service_types = [
        {
            'name': service_type.name,
            'services': [
                {
                    'name': service.name,
                    'price': service.price,
                } for service in service_type.services.all()
            ],
        } for service_type in service_types
    ]

    context = {
        'salons': salons,
        'masters': masters,
        'service_types': service_types,
        'dates': dates,
    }

    return render(request, template, context)


def show_service_finally(request):
    #template = "beautycity/serviceFinally.html"
    salon = request.GET['salon']
    service = request.GET['service']
    master = request.GET['master'].split(":")
    year = request.GET['year']
    month = request.GET['month']
    day = request.GET['day']
    time = request.GET['time'].split(":")
    name = request.GET['name']
    phone = request.GET['phone']
    text = request.GET['text']

    user, is_new_user = User.objects.get_or_create(
        phone_number=phone,
        username=phone
    )
    if is_new_user:
        user.first_name = name
        user.save()
    login(request, user, backend=settings.AUTHENTICATION_BACKENDS[0])


    service = Service.objects.get(name=service)
    master = Master.objects.get(
        first_name=master[0],
        last_name=master[1],
    )
    salon = Salon.objects.get(name=salon)
    date_time = datetime(
        int(year),
        int(month),
        int(day),
        int(time[0])+3,
        int(time[1]),
    )

    date_time = AvailableDateTime.objects.create(
        datetime=date_time
    )

    ServiceSignUp.objects.create(
        service=service,
        master=master,
        datetime=date_time,
        salon=salon,
        tips=0,
        user=user,
        question=text,
    )

    #return render(request, template)
    return redirect("beauty:notes")


def show_manager_page(request):
    template = "beautycity/admin.html"
    context = {}
    return render(request, template, {"context": context})


def update_paid_status(payment_id):
    orders = ServiceSignUp.objects.filter(payment_id=payment_id).all()
    for order in orders:
        order.paid = True
    ServiceSignUp.objects.bulk_update(orders, ['paid'])

def make_payment_by_id(request, order_id):
    if request.method == "GET":
        Configuration.account_id = SHOP_ID
        Configuration.secret_key = API_KEY

        price = ServiceSignUp.objects.get(id=order_id).service.price
        payment = Payment.create({
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                "return_url": settings.RETURN_URL
            },
            "capture": True,
            "description": f'Оплата по заказу {order_id}'
        }, uuid.uuid4())

        signup = ServiceSignUp.objects.get(id=order_id)
        signup.payment_id = payment.id
        signup.save()

        confirmation_url = payment.confirmation.confirmation_url

        update_paid_status(payment.id)
        return redirect(confirmation_url)

def make_payment(request):
    if request.method == "GET":
        Configuration.account_id = SHOP_ID
        Configuration.secret_key = API_KEY
        price = 0
        for unpaid_signup in ServiceSignUp.objects.filter(paid=False).select_related('service'):
            price += unpaid_signup.service.price

        payment = Payment.create({
            "amount": {
                "value": price,
                "currency": "RUB"
            },
            "confirmation": {
                "type": "redirect",
                 "return_url": settings.RETURN_URL
            },
            "capture": True,
            "description": f'Оплата по заказам'
        }, uuid.uuid4())
        unpaids_signups =ServiceSignUp.objects.filter(paid=False).all()
        for unpaids_signup in unpaids_signups:
            unpaids_signup.payment_id = payment.id

        ServiceSignUp.objects.bulk_update(unpaids_signups, ['payment_id'])
        confirmation_url = payment.confirmation.confirmation_url

        update_paid_status(payment.id)

        return redirect(confirmation_url)
