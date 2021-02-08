from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.exceptions import ValidationError


class Ride(models.Model):
    """Model for rides"""
    title = models.CharField(max_length=255, null=False, blank=True)
    source_location = models.CharField(
        max_length=50,
        null=False,
        blank=False
    )
    destination_location = models.CharField(
        max_length=50,
        null=False,
        blank=False
        )
    start_time = models.DateTimeField(
        auto_now=False,
        default=timezone.now
    )
    distance = models.DecimalField(
        default=10,
        max_digits=5,
        decimal_places=1
    )
    end_time = models.DateTimeField(
        auto_now=False,
        default=timezone.now
    )
    ride_created_time = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    driver = models.ForeignKey(
        User,
        related_name='driving',
        on_delete=models.CASCADE
    )
    number_of_seats = models.IntegerField(default=3)
    car_name = models.CharField(max_length=100, null=True, blank=True)
    status = models.CharField(max_length=20, default='Pending')
    car_number = models.CharField(max_length=100, null=True, blank=True)
    price_per_km = models.IntegerField(default=10)
    description = models.CharField(
        max_length=500,
        null=True,
        blank=True
    )

    def finish(self, *args, **kwargs):
        '''
            Method to finish Ride.
            This will create payments for all riders
            and then set the status of ride to Finished.
        '''
        for trip in self.trips.all():
            payment = Payment.objects.create(
                ride=self,
                rider=trip.rider,
                amount=self.price_per_km * self.distance,
                status="Pending"
            )
            payment.save()
        self.status = 'Finished'
        self.save()

    def save(self, *args, **kwargs):
        '''
        Method to override save method,
        this will set title for the ride
        to be used by __str__ Method
        '''
        self.title = (
            f"{self.driver} from \
            {self.source_location} to \
            {self.destination_location}"
        )
        super(Ride, self).save(*args, **kwargs)

    def __str__(self):
        '''Method for string representation'''
        return (
            f"{self.driver} from \
            {self.source_location} \
            to {self.destination_location}"
        )


class Request(models.Model):
    """Model for requesting for rides"""
    ride = models.ForeignKey(
        Ride,
        related_name='requests',
        on_delete=models.CASCADE
    )
    user_requested = models.ForeignKey(
        User,
        related_name='ride_requested',
        on_delete=models.CASCADE
    )
    request_created_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50, default='Pending')
    comments = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        '''Meta class for the model'''
        unique_together = ('ride', 'user_requested')

    def approve(self):
        '''Method to approve request'''
        trip = Trip.objects.create(ride=self.ride,
                                   rider=self.user_requested)
        trip.save()
        self.status = 'Approved'
        self.save()

    def reject(self):
        '''Method to reject request'''
        self.status = 'Rejected'
        self.save()

    def __str__(self):
        '''Method for string representation'''
        return f"Ride: {self.ride}  <-- \
         Requested by: {self.user_requested}, \
         Status {self.status}"


class Trip(models.Model):
    """Model for Trips"""
    ride = models.ForeignKey(
        Ride,
        related_name="trips",
        on_delete=models.CASCADE
    )
    rider = models.ForeignKey(
        User,
        related_name="riding",
        on_delete=models.CASCADE
    )

    class Meta:
        '''Meta class for Trip Model'''
        unique_together = (
            "ride",
            "rider",
        )

    def clean(self):
        '''method to check if seats are full'''
        if Trip.objects.filter(
            ride=self.ride
        ).count() >= self.ride.number_of_seats:
            raise ValidationError(
                f"Only {self.ride.number_of_seats} riders allowed"
            )

    def __str__(self):
        '''Method for string representation'''
        return str(f"{self.ride} -- > {self.rider}")


class Payment(models.Model):
    """Model for payments"""
    ride = models.ForeignKey(
        Ride,
        related_name="payments",
        on_delete=models.CASCADE
    )
    rider = models.ForeignKey(
        User,
        related_name="payments",
        on_delete=models.CASCADE
    )
    amount = models.IntegerField(default=100)
    generated_time = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default="pending")

    class Meta:
        '''Meta class for Payment model'''
        unique_together = ("ride", "rider")

    def pay(self):
        '''Method to pay the generated payment bill'''
        self.status = "Paid"
        self.save()

    def __str__(self):
        '''Method for string representation'''
        return f"{self.ride} <-- {self.rider} {self.amount}"
