import csv

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required

from .models import Contact, ContactGroup
from .forms import ContactForm, ContactGroupForm, CSVUploadForm


@login_required
def contact_list(request):

    contacts = Contact.objects.filter(
        user=request.user
    )

    return render(request, 'contacts/list.html', {
        'contacts': contacts
    })


@login_required
def create_contact(request):

    form = ContactForm(request.POST or None)

    if form.is_valid():

        contact = form.save(commit=False)
        contact.user = request.user
        contact.save()

        return redirect('contact_list')

    return render(request, 'contacts/create.html', {
        'form': form
    })


@login_required
def contact_groups(request):

    groups = ContactGroup.objects.filter(
        user=request.user
    )

    return render(request, 'contacts/groups.html', {
        'groups': groups
    })


@login_required
def create_group(request):

    form = ContactGroupForm(request.POST or None)

    if form.is_valid():

        group = form.save(commit=False)
        group.user = request.user
        group.save()

        return redirect('contact_groups')

    return render(request, 'contacts/create_group.html', {
        'form': form
    })


@login_required
def upload_contacts(request, group_id):

    group = get_object_or_404(
        ContactGroup,
        id=group_id,
        user=request.user
    )

    form = CSVUploadForm(
        request.POST or None,
        request.FILES or None
    )

    if form.is_valid():

        csv_file = request.FILES['csv_file']

        decoded_file = csv_file.read().decode(
            'utf-8'
        ).splitlines()

        reader = csv.DictReader(decoded_file)

        for row in reader:

            Contact.objects.create(
                user=request.user,
                group=group,
                name=row.get('name', ''),
                phone=row.get('phone', ''),
                email=row.get('email', '')
            )

        return redirect('contact_groups')

    return render(request, 'contacts/upload.html', {
        'form': form,
        'group': group
    })