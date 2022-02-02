from email import message
import json
from operator import contains
from django.http import request
import requests

from django.shortcuts import redirect, render
from .models import Stock
from .forms import StockForm
from django.contrib import messages
# Create your views here.


def home(request):
    # sandbox_c7grba2ad3ibsjtt23pg
    token = "sandbox_c7grba2ad3ibsjtt23pg"
    if request.method == 'POST':
        ticker = request.POST['ticker']
        ticker = ticker.upper()

        url = "https://finnhub.io/api/v1/quote?symbol=" + ticker + "&token=" + token
        
   
        try:
            api_request = requests.get(url)
            api = json.loads(api_request.content)
        except Exception as e:
          
            api = "Error..."
        
       
        return render(request, "home.html", {'api': api})
    else:
        return render(request, 'home.html', {'ticker': "Enter a stock symbol !"})


def about(request):
    return render(request, 'about.html', {})


def add_stock(request):

    if request.method == 'POST':
        form =  StockForm(request.POST or None)

        if form.is_valid():
           form.save()
           messages.success(request, ("Stock has been added"))
        
        return redirect('add_stock')
    else:
        ticker  = Stock.objects.all()
        return render(request, 'add_stock.html', {'ticker': ticker})


def delete(request, stock_id ,):
    item = Stock.objects.get(pk=stock_id)
    item.delete()
    messages.success(request , ("Stock has been deleted!"))
    return redirect('add_stock')

