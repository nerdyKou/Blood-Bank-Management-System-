from django.db import models
from django.db.models import Sum


class Donor(models.Model):
    BLOOD_GROUP_CHOICES = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
        ('O+', 'O+'), ('O-', 'O-'),
    ]

    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]

    name = models.CharField(max_length=100)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUP_CHOICES)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    last_donation_date = models.DateField(blank=True, null=True)

    # how many units this donor donated (for this record)
    units_donated = models.PositiveIntegerField(default=0)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.blood_group})"

    def save(self, *args, **kwargs):
        """
        Every time a donor is created or edited, recalculate the
        BloodInventory for the relevant blood groups by summing
        all donors' units_donated.
        """
        # Remember old blood group (if editing)
        old_blood_group = None
        if self.pk:
            old = Donor.objects.get(pk=self.pk)
            old_blood_group = old.blood_group

        # Save donor first
        super().save(*args, **kwargs)

        # Old group (if changed) + new group
        groups_to_update = set()
        if old_blood_group:
            groups_to_update.add(old_blood_group)
        groups_to_update.add(self.blood_group)

        for group in groups_to_update:
            # Sum all units_donated for this group
            total_units = (
                Donor.objects
                .filter(blood_group=group)
                .aggregate(total=Sum('units_donated'))
                ['total'] or 0
            )

            inv, created = BloodInventory.objects.get_or_create(
                blood_group=group,
                defaults={'units_available': 0},
            )
            inv.units_available = total_units
            inv.save()


class BloodInventory(models.Model):
    BLOOD_GROUP_CHOICES = Donor.BLOOD_GROUP_CHOICES

    blood_group = models.CharField(
        max_length=3,
        choices=BLOOD_GROUP_CHOICES,
        unique=True
    )
    units_available = models.PositiveIntegerField(default=0)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.blood_group} - {self.units_available} units"


class BloodRequest(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('REJECTED', 'Rejected'),
        ('FULFILLED', 'Fulfilled'),
    ]

    patient_name = models.CharField(max_length=100)
    hospital_name = models.CharField(max_length=150, blank=True, null=True)
    blood_group = models.CharField(max_length=3, choices=Donor.BLOOD_GROUP_CHOICES)
    units_requested = models.PositiveIntegerField()
    reason = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Request: {self.patient_name} ({self.blood_group})"
