from django.contrib import admin
from .models import Donor, BloodInventory, BloodRequest

@admin.register(Donor)
class DonorAdmin(admin.ModelAdmin):
    list_display = ('name', 'blood_group', 'units_donated', 'phone', 'last_donation_date', 'created_at')
    search_fields = ('name', 'blood_group', 'phone')



@admin.register(BloodInventory)
class BloodInventoryAdmin(admin.ModelAdmin):
    list_display = ('blood_group', 'units_available', 'last_updated')


@admin.register(BloodRequest)
class BloodRequestAdmin(admin.ModelAdmin):
    list_display = ('patient_name', 'blood_group', 'units_requested', 'status', 'created_at')
    list_filter = ('blood_group', 'status')
    search_fields = ('patient_name', 'hospital_name')
