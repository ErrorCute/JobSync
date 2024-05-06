from django.shortcuts import render

# Create your views here.
def login(request):
    return render(request,'login.html')

def sobre_nosotros(request):
    return render(request, 'sobrenosotros.html')