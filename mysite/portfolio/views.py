from django.shortcuts import render

# Create your views here.
def getMainPorfolioView(request):
    return render(request, 'portfolio/index.html')