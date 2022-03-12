from django.http import HttpResponse
from django.views import generic
from django.urls import reverse_lazy
from django.shortcuts import render, redirect

from .forms import ReservationForm
from .models import Reservation
from .forms import ReservationForm
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
