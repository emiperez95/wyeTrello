from django.shortcuts import render

from trellofy.models import userForm, miniUser


def index(request):
    if request.method == "POST":
        form = userForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = userForm()

    entries = miniUser.objects.all()
    context = {
        'form': form,
        'entries': entries,
    }
    return render(request, 'home.html', context)
