from django.urls import path
from .views import (
    RideListView,
    RideCreateView,
    RideUpdateView,
    RideDetailView,
    RideDeleteView,
    UserRideListView,
    UserRequestsListView,
    UserRequestedListView,
    UserPaymentListView,
    UserPaymentRecievedListView,
)
from .views import (
    approve_request_view,
    reject_request_view,
    create_request_view,
    ride_finish_view,
    payment_pay_view,
)

urlpatterns = [
    # url pattern for homepage
    path(
        "",
        RideListView.as_view(),
        name="home"
    ),

    # url pattern for rides of user
    path(
        "user/<str:username>",
        UserRideListView.as_view(),
        name="user-rides"
    ),

    # url pattern for ride details
    path(
        "ride/<int:pk>/",
        RideDetailView.as_view(),
        name="ride-detail"
    ),

    # url pattern to create ride
    path(
        "ride/new/",
        RideCreateView.as_view(),
        name="ride-create"
    ),

    # url pattern to update ride
    path(
        "ride/<int:pk>/update/",
        RideUpdateView.as_view(),
        name="ride-update"
    ),

    # url pattern to delete ride
    path(
        "ride/<int:pk>/delete/",
        RideDeleteView.as_view(),
        name="ride-delete"
    ),

    # url pattern to list requests of user
    path(
        "requests/",
        UserRequestsListView.as_view(),
        name="user-requests"
        ),

    # url pattern to list requests by user
    path(
        "requested_list/",
        UserRequestedListView.as_view(),
        name="user-requested"
    ),

    # url pattern to list payments of user
    path(
        "payment_list/",
        UserPaymentListView.as_view(),
        name="user-payments"
    ),

    # url pattern to list payments recieved by a user
    path(
        "payment_recieved/",
        UserPaymentRecievedListView.as_view(),
        name="user-payment-recieved"
    ),

    # url pattern to approve ride request
    path(
        "approve/request/<int:req>",
        approve_request_view,
        name="approve-request"
    ),

    # url pattern to reject ride request
    path(
        "reject/request/<int:req>",
        reject_request_view,
        name="reject-request"
    ),

    # url pattern to create request for ride
    path(
        "create/request/<int:ride>",
        create_request_view,
        name="create-request"
    ),

    # url pattern to finish a ride
    path(
        "finish/ride/<int:ride>",
        ride_finish_view,
        name="ride-finish"
    ),

    # url pattern to pay payment bill
    path(
        "payment/<int:payment>",
        payment_pay_view,
        name="payment-pay"
    ),
]
