
from django.contrib.auth.decorators import login_required

from .forms import ContactForm, ContactGroupForm
from django.shortcuts import (
    render,
    redirect,
    get_object_or_404
)

from .models import Contact,ContactGroup

@login_required
def contact_list(request):

    contacts = Contact.objects.all()

    return render(
        request,
        'contacts/contact_list.html',
        {
            'contacts': contacts
        }
    )
@login_required
def contact_create(request):

    if request.method == 'POST':

        form = ContactForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect(
                'contacts:contact_list'
            )

    else:

        form = ContactForm()

    return render(
        request,
        'contacts/contact_form.html',
        {
            'form': form
        }
    )
@login_required
def contact_update(request, pk):

    contact = get_object_or_404(
        Contact,
        pk=pk
    )

    if request.method == 'POST':

        form = ContactForm(
            request.POST,
            instance=contact
        )

        if form.is_valid():

            form.save()

            return redirect(
                'contacts:contact_list'
            )

    else:

        form = ContactForm(
            instance=contact
        )

    return render(
        request,
        'contacts/contact_form.html',
        {
            'form': form
        }
    )
@login_required
def contact_delete(request, pk):

    contact = get_object_or_404(
        Contact,
        pk=pk
    )

    if request.method == 'POST':

        contact.delete()

        return redirect(
            'contacts:contact_list'
        )

    return render(
        request,
        'contacts/contact_confirm_delete.html',
        {
            'contact': contact
        }
    )
@login_required
def group_list(request):

    groups = ContactGroup.objects.all()

    return render(
        request,
        'contacts/group_list.html',
        {
            'groups': groups
        }
    )


@login_required
def group_create(request):

    if request.method == 'POST':

        form = ContactGroupForm(
            request.POST
        )

        if form.is_valid():

            form.save()

            return redirect(
                'contacts:group_list'
            )

    else:

        form = ContactGroupForm()

    return render(
        request,
        'contacts/group_form.html',
        {
            'form': form
        }
    )


@login_required
def group_update(request, pk):

    group = get_object_or_404(
        ContactGroup,
        pk=pk
    )

    if request.method == 'POST':

        form = ContactGroupForm(
            request.POST,
            instance=group
        )

        if form.is_valid():

            form.save()

            return redirect(
                'contacts:group_list'
            )

    else:

        form = ContactGroupForm(
            instance=group
        )

    return render(
        request,
        'contacts/group_form.html',
        {
            'form': form
        }
    )


@login_required
def group_delete(request, pk):

    group = get_object_or_404(
        ContactGroup,
        pk=pk
    )

    if request.method == 'POST':

        group.delete()

        return redirect(
            'contacts:group_list'
        )

    return render(
        request,
        'contacts/group_confirm_delete.html',
        {
            'group': group
        }
    )