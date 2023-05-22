import json

from django.contrib.auth import login
from django.shortcuts import redirect, render

from beatycity import settings
from users.models import SMSCode, User


def show_home(request):
    template = "beautycity/index.html"

    if request.method == "POST" and not "num1" in request.POST:
        if request.body:
            body_data = json.loads(request.body)
            phone_number = request.session['phone_number'] = body_data["phone_number"]
            try:
                user, _ = User.objects.get_or_create(phone_number=phone_number)
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
            return redirect("beauty:notes")
        else:
            print("wrong_code")
    return render(request, template)

def show_notes(request):
    template = "beautycity/notes.html"
    context = {}
    return render(request, template, {"context": context})
