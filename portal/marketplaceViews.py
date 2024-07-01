from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Product, User
from .forms import ProductForm

def marketPlace(request):
    products = Product.objects.all()
    return render(request, "marketplace/marketplace.html", {"products": products, "user": request.user})

@login_required(login_url="signin")
def add_product(request):
    if request.method == "POST":
        form = ProductForm(request.POST, request.FILES)
        # Validate the form
        if form.is_valid():
            product = form.save(request.user)
            messages.success(request, "Product added successfully!")
            # Redirect to the marketplace or product detail page
            return redirect("market-place")
        # If the form is not valid, show an error message or handle it accordingly
        else:
            print(form.errors)
            messages.error(request, "Error adding the product. Please check the form.")
    # If the request method is not POST, redirect to the marketplace
    return redirect("market-place")



@login_required(login_url="signin")
def delete_product(request, id=None):
    try:
        product = Product.objects.get(id=id)
        product.delete()
        messages.success(request, "Product deleted successfully!")
    except Exception as e:
        print(e)
        messages.error(request, "Product couldnot be deleted!")
    return redirect("market-place")


@login_required(login_url="signin")
def buyProduct(request):
    if request.method == "POST":
        try:
            product = Product.objects.get(id=request.POST.get("productId"))
            product.buyer = request.user
            product.save()
            messages.success(request, "Product bought successfully!")
        except Exception as e:
            print(e)
            messages.error(request, "Product couldnot be bought!")
    return HttpResponseRedirect(reverse("market-place"))
