from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from .forms import ReservationForm
from .models import Reservation
from .forms import ReservationForm, CreateUserForm
from .utils import download_csv


class ReservationHomeView(generic.TemplateView):
    template_name = "rsvp/base.html"


class ReservationListView(generic.ListView):
    model = Reservation
    paginate_by = 25


class ReservationAddView(generic.CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservation_list")


class ReservationEditView(generic.UpdateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservation_list")


class ReservationDeleteView(generic.DeleteView):
    model = Reservation
    success_url = reverse_lazy("reservation_list")


def reservation_search(request):
    if request.method == "POST":
        searched = str(request.POST.get("searched"))
        if searched:
            reservations = Reservation.objects.filter(full_name__icontains=searched)
            return render(
                request,
                "rsvp/reservation_search.html",
                {"searched": searched, "reservations": reservations},
            )
        else:
            return redirect("reservation_list")
    else:
        return redirect("reservation_list")


def export_csv(request):
    data = download_csv(request, Reservation.objects.all())
    response = HttpResponse(data, content_type="text/csv")
    return response


def register_page(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            print('new user is being saved')
            form.save()
            messages.success(request, f"Account was created for {request.POST.get('username')}")
            return redirect('login')

    context = {'form': form}
    return render(request, 'rsvp/register.html', context)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return render(request, 'rsvp/reservation_list.html', {'user':user})
        else:
            messages.info('Username or password is incorrect...')

    context = {}
    return render(request, 'rsvp/login.html', context)

def user_logout(request):
    pass