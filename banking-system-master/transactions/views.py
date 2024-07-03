from dateutil.relativedelta import relativedelta

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.generic import CreateView, ListView
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import UploadFileForm
from .models import UploadStatistics
import csv


from transactions.models import Transaction

from io import TextIOWrapper
import csv
from django.shortcuts import render, redirect
from django.utils import timezone
from .forms import UploadFileForm
from .models import UploadStatistics

from django.shortcuts import redirect

from django.shortcuts import redirect

def list_management(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            if form.cleaned_data['ofac_file']:
                process_file(form.cleaned_data['ofac_file'], 'ofac')
            if form.cleaned_data['un_file']:
                process_file(form.cleaned_data['un_file'], 'un')
            if form.cleaned_data['eu_file']:
                process_file(form.cleaned_data['eu_file'], 'eu')
            return redirect('transactions:list_management')  # Namespaced URL pattern
    else:
        form = UploadFileForm()

    statistics = UploadStatistics.objects.all()
    context = {
        'form': form,
        'statistics': statistics
    }
    return render(request, 'transactions/list_management.html', context)




def process_file(file, list_name):
    start_time = timezone.now()
    
    # Read CSV file in text mode
    file_wrapper = TextIOWrapper(file, encoding='utf-8')
    reader = csv.DictReader(file_wrapper)
    
    records_added = 0
    records_updated = 0
    records_deleted = 0

    existing_records = set()
    new_records = set()
    
    # Track all UIDs for debugging
    all_uids = set()
    
    for row in reader:
        uid = row.get('ID_original')
        if uid:
            all_uids.add(uid)  # Track all UIDs encountered
            if uid not in existing_records:
                new_records.add(uid)
            existing_records.add(uid)

    # Debugging output
    print(f"Total UIDs read: {len(all_uids)}")
    print(f"Unique UIDs processed: {len(existing_records)}")
    print(f"New UIDs added: {len(new_records)}")

    # Placeholder logic for record handling
    records_added = len(new_records)  # Update this based on your actual logic

    # Update statistics
    end_time = timezone.now()
    stats, created = UploadStatistics.objects.update_or_create(
        list_name=list_name,
        defaults={
            'last_import_date': end_time.date(),
            'records_added': records_added,
            'records_updated': records_updated,
            'records_deleted': records_deleted,
            'total_active_records': len(existing_records),  # Update as needed
            'start_time': start_time,
            'end_time': end_time,
        }
    )
