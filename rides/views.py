from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    DeleteView,
    UpdateView,
)
from .models import Ride, Request, Payment


class RideListView(LoginRequiredMixin, ListView):
    '''View to list all rides'''
    model = Ride
    template_name = "rides/home.html"  # <app>/<model>_<viewtype>.html
    context_object_name = "rides"
    ordering = ["-ride_created_time"]
    paginate_by = 5

    def get_queryset(self):
        '''method to return all active rides'''
        return Ride.objects.filter(is_active=True)


class UserRideListView(LoginRequiredMixin, ListView):
    '''View to return all rides of a user'''
    model = Ride
    template_name = "rides/user_rides.html"
    context_object_name = "rides"
    ordering = ["-ride_created_time"]
    paginate_by = 5

    def get_context_data(self, **kwargs):
        '''method to get the custom context data to be used by template'''
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["profile_user"] = get_object_or_404(
            User, username=self.kwargs.get("username")
        )
        context["rides_of_this_user"] = Ride.objects.filter(
            driver=context["profile_user"].id,
        )
        return context

    def get_queryset(self):
        '''method to return query set to return all rides of a user'''
        user = get_object_or_404(User, username=self.kwargs.get("username"))
        return Ride.objects.filter(driver=user).order_by("-ride_created_time")


class RideDetailView(LoginRequiredMixin, DetailView):
    '''View for Ride details'''
    model = Ride
    context_object_name = "ride"

    def get_context_data(self, **kwargs):
        '''method to get the custom context data to be used by template'''
        # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        context["already_requested"] = (
            Request.objects.filter(ride=self.kwargs.get("pk"))
            .filter(user_requested=self.request.user)
            .count()
            >= 1
        )
        return context


class RideCreateView(LoginRequiredMixin, CreateView):
    '''View to create New Ride'''
    model = Ride
    success_url = "/"

    fields = [
        "source_location",
        "destination_location",
        "start_time",
        "end_time",
        "price_per_km",
        "distance",
    ]

    def form_valid(self, form):
        '''Validation of form to set driver to the request user'''
        form.instance.driver = self.request.user
        return super().form_valid(form)


class RideUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    '''View to update a ride'''
    model = Ride
    success_url = "/"
    fields = [
        "source_location",
        "destination_location",
        "start_time",
        "end_time",
        "price_per_km",
    ]

    def form_valid(self, form):
        '''validation of form to set driver to the request user'''
        form.instance.driver = self.request.user
        return super().form_valid(form)

    def test_func(self):
        '''
        Custom test function to verify if
        the user is the owner(driver) of the ride
        '''
        ride = self.get_object()
        if self.request.user == ride.driver:
            return True
        return False


class RideDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    '''View to delete ride'''
    model = Ride
    success_url = "/"

    def test_func(self):
        '''
        Custom test to check if the user
        is the owner(driver) of the ride object
        '''
        ride = self.get_object()
        if self.request.user == ride.driver:
            return True
        return False


class UserRequestsListView(LoginRequiredMixin, ListView):
    '''View to get all the requests for rides of a user'''
    model = Request
    template_name = "requests/user_requests.html"
    context_object_name = "requests"
    ordering = ["-request_created_time"]
    paginate_by = 5

    def get_queryset(self):
        '''custom query set to return all the requests for rides of a user'''
        requests_list = Request.objects.filter(
            ride__driver=self.request.user
        ).order_by("-request_created_time")
        return requests_list


class UserRequestedListView(LoginRequiredMixin, ListView):
    '''View to get all the requests made by a user for rides'''
    model = Request
    template_name = "requests/user_requests.html"
    context_object_name = "requests"
    ordering = ["-request_created_time"]
    paginate_by = 5

    def get_queryset(self):
        '''Queryset to return all ride requests made by user'''
        requests_list = Request.objects.filter(
            user_requested=self.request.user
        ).order_by("-request_created_time")
        return requests_list


class UserPaymentListView(LoginRequiredMixin, ListView):
    '''View to list all the payments of a user'''
    model = Payment
    template_name = "payments/user_payments.html"
    context_object_name = "payments"
    ordering = ["-generated_time"]
    paginate_by = 5

    def get_queryset(self):
        '''queryset to list all the payments of a user'''
        payments_list = Payment.objects.filter(
            rider=self.request.user
        ).order_by("-generated_time")
        return payments_list

class UserPaymentRecievedListView(LoginRequiredMixin, ListView):
    '''View to list all the payments recieved by a user'''
    model = Payment
    template_name = "payments/user_payments.html"
    context_object_name = "payments"
    ordering = ["-generated_time"]
    paginate_by = 5

    def get_queryset(self):
        '''queryset to list all the payments recieved by a user'''
        payments_list = Payment.objects.filter(
            ride__driver=self.request.user
        ).order_by("-generated_time")
        return payments_list


@login_required
def approve_request_view(request, req):
    '''function based view to approve a ride request'''
    if request.method == "POST":
        req_to_approve = get_object_or_404(Request, id=req)
        req_to_approve.approve()
        return redirect("user-requests")
    else:
        return redirect("home")


@login_required
def reject_request_view(request, req):
    '''function based view to reject a ride request'''
    if request.method == "POST":
        req_to_reject = get_object_or_404(Request, id=req)
        req_to_reject.reject()
        return redirect("user-requests")
    else:
        return redirect("home")


@login_required
def create_request_view(request, ride):
    '''function based view to create a ride request'''
    if request.method == "POST":
        ride = get_object_or_404(Ride, id=ride)
        req = Request.objects.create(ride=ride, user_requested=request.user)
        req.save()
        return redirect("user-requested")
    else:
        return redirect("home")


@login_required
def ride_finish_view(request, ride):
    '''function based view to finish a ride'''
    ride = get_object_or_404(Ride, id=ride)
    ride.finish()
    return redirect("ride-detail", pk=ride.id)


@login_required
def payment_pay_view(request, payment):
    '''function based view to pay a bill'''
    if request.method == "POST":
        payment = get_object_or_404(Payment, id=payment)
        payment.pay()
        return redirect("user-payments")
    else:
        return redirect("home")
