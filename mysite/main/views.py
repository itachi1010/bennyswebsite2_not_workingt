from .models import Book, Product
from django.core.paginator import Paginator  # import Paginator

from django.shortcuts import render, redirect
from .forms import ContactForm
from django.core.mail import send_mail, BadHeaderError
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from .forms import NewUserForm, UserForm, ProfileForm
from django.core.files.storage import FileSystemStorage
from .forms import MovieForm
from .models import Movie


# Create your views here.


def homepage(request):
    if request.method == "POST":
        product_id = request.POST.get('product_pk')
        product = Product.objects.get(id=product_id)
        request.user.profile.products.add(product)
        messages.success(request, (f'{product} added to wishlist.'))
        return redirect('main:homepage')
    product = Product.objects.all()[:4]
    return render(request=request, template_name="main/home.html",
                  context={'product': product})


# "<p>This is a test website that was made by benny</p>"

# Create your views here.
def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            subject = "Website Inquiry"
            body = {
                'first_name': form.cleaned_data['first_name'],
                'last_name': form.cleaned_data['last_name'],
                'email': form.cleaned_data['email_address'],
                'message': form.cleaned_data['message'],
            }
            message = "\n".join(body.values())

            try:
                send_mail(subject, message, 'admin@example.com', ['admin@example.com'])
            except BadHeaderError:
                return HttpResponse('Invalid header found.')
            messages.success(request, "Message sent.")
            return redirect("main:homepage")
        messages.error(request, "Error. Message not sent.")

    form = ContactForm()
    return render(request, "main/contact.html", {'form': form})


def register(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("main:homepage")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm
    return render(request=request, template_name="main/register.html", context={"form": form})


def login_request(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect("main:homepage")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request=request, template_name="main/login.html", context={"form": form})


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("main:homepage")


def products(request):
    if request.method == "POST":
        product_id = request.POST.get("product_pk")
        product = Product.objects.get(id=product_id)
        request.user.profile.products.add(product)
        messages.success(request, (f'{product} added to wishlist.'))
        return redirect('main:products')
    products = Product.objects.all()
    paginator = Paginator(products, 18)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request=request, template_name="main/products.html", context={"page_obj": page_obj})


def aboutus(request):
    return render(request=request, template_name='main/aboutus.html')


def userpage(request):
    if request.method == "POST":
        user_form = UserForm(request.POST, instance=request.user)
        profile_form = ProfileForm(request.POST, instance=request.user.profile)
        if user_form.is_valid():
            user_form.save()
            messages.success(request, ('Your profile was successfully updated!'))
        elif profile_form.is_valid():
            profile_form.save()
            messages.success(request, ('Your wishlist was successfully updated!'))
        else:
            messages.error(request, ('Unable to complete request'))
        return redirect("main:userpage")
    user_form = UserForm(instance=request.user)
    profile_form = ProfileForm(instance=request.user.profile)
    return render(request=request, template_name="main/user.html", context={"user": request.user,"user_form": user_form,"profile_form": profile_form})


def upload(request):
    if request.method == "POST":
        form = MovieForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
        return redirect("main:upload")
    form = MovieForm()
    movies = Movie.objects.all()
    return render(request=request, template_name="main/upload.html", context={'form': form, 'movies': movies})
