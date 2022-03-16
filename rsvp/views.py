from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


from .forms import ReservationForm
from .models import Reservation
from .forms import ReservationForm, CreateUserForm
from .utils import download_csv

def testing(request):
    return render(request, 'rsvp/testing.html', {})

class ReservationHomeView(LoginRequiredMixin, generic.TemplateView):
    template_name = "rsvp/base.html"
    login_url = '/login/'

class ReservationListView(LoginRequiredMixin, generic.ListView):
    model = Reservation
    paginate_by = 25
    login_url = '/login/'

class ReservationAddView(LoginRequiredMixin, generic.CreateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservation_list")
    login_url = '/login/'

class ReservationEditView(LoginRequiredMixin, generic.UpdateView):
    model = Reservation
    form_class = ReservationForm
    success_url = reverse_lazy("reservation_list")
    login_url = '/login/'

class ReservationDeleteView(LoginRequiredMixin, generic.DeleteView):
    model = Reservation
    success_url = reverse_lazy("reservation_list")
    login_url = '/login/'

@login_required(login_url='login')
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

@login_required(login_url='login')
def export_csv(request):
    data = download_csv(request, Reservation.objects.all())
    response = HttpResponse(data, content_type="text/csv")
    return response


def register_page(request):
    if request.user.is_authenticated:
        return redirect('reservation_list')
    else:
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

def login_page(request):
    if request.user.is_authenticated:
        return redirect('reservation_list')
    else:
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

@login_required(login_url='login')
def logout_user(request):
    logout(request)
    return redirect('login')