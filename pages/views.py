from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm
from .webScrape import scrape


# Create your views here.
def home_view(request, *args, **kwargs):
    return render(request, "index.html", {})


def form_view(request, *args, **kwargs):
    form = ProductForm(request.POST or None)
    if form.is_valid():
        form.save()
        scrape(request.POST['url'], request.POST['price'], request.POST['email'])
        form = ProductForm()

    context = {
        'form': form
    }
    return render(request, "form.html", context)
