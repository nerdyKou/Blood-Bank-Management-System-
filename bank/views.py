from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from .models import Donor, BloodInventory, BloodRequest
from .forms import DonorForm, BloodRequestForm

def staff_required(view_func):
    decorated_view = login_required(
        user_passes_test(lambda u: u.is_staff)(view_func)
    )
    return decorated_view


@staff_required
def dashboard(request):
    total_donors = Donor.objects.count()
    total_requests = BloodRequest.objects.count()
    pending_requests = BloodRequest.objects.filter(status='PENDING').count()
    inventory = BloodInventory.objects.all().order_by('blood_group')

    context = {
        'total_donors': total_donors,
        'total_requests': total_requests,
        'pending_requests': pending_requests,
        'inventory': inventory,
    }
    return render(request, 'bank/dashboard.html', context)


@staff_required
def donor_list(request):
    donors = Donor.objects.all().order_by('-created_at')
    return render(request, 'bank/donor_list.html', {'donors': donors})


@staff_required
def donor_create(request):
    if request.method == 'POST':
        form = DonorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('donor_list')
    else:
        form = DonorForm()
    return render(request, 'bank/donor_form.html', {'form': form, 'title': 'Add Donor'})


@staff_required
def donor_update(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        form = DonorForm(request.POST, instance=donor)
        if form.is_valid():
            form.save()
            return redirect('donor_list')
    else:
        form = DonorForm(instance=donor)
    return render(request, 'bank/donor_form.html', {'form': form, 'title': 'Edit Donor'})


@staff_required
def donor_delete(request, pk):
    donor = get_object_or_404(Donor, pk=pk)
    if request.method == 'POST':
        donor.delete()
        return redirect('donor_list')
    return render(request, 'bank/confirm_delete.html', {'object': donor, 'type': 'Donor'})


@staff_required
def request_list(request):
    requests_qs = BloodRequest.objects.all().order_by('-created_at')
    return render(request, 'bank/request_list.html', {'requests': requests_qs})


@staff_required
@staff_required
def request_create(request):
    if request.method == 'POST':
        form = BloodRequestForm(request.POST)
        if form.is_valid():
            req = form.save(commit=False)
            req.status = 'PENDING'      # 👈 force default
            req.save()
            return redirect('request_list')
    else:
        form = BloodRequestForm()
    return render(request, 'bank/request_form.html', {'form': form, 'title': 'Create Blood Request'})


@staff_required
def request_update(request, pk):
    req = get_object_or_404(BloodRequest, pk=pk)
    if request.method == 'POST':
        form = BloodRequestForm(request.POST, instance=req)
        if form.is_valid():
            form.save()
            return redirect('request_list')
    else:
        form = BloodRequestForm(instance=req)
    return render(request, 'bank/request_form.html', {'form': form, 'title': 'Update Blood Request'})


@staff_required
def inventory_list(request):
    inventory = BloodInventory.objects.all().order_by('blood_group')
    return render(request, 'bank/inventory_list.html', {'inventory': inventory})
