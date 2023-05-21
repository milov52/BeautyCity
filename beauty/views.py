from django.shortcuts import render

# Create your views here.
def show_home(request):
    context = {}
    template = "beautycity/index.html"
    return render(request, template, context=context)
