from django.shortcuts import render


def index(request):
    context = {
        'title': 'UWCA_Manager',
        'heading_name': 'report manager',
    }
    return render(request, 'reports/index.html', context)


def reports(request):
    context = {
        'title': 'UWCA_Manager',
    }

    return render(request, 'reports/reports.html', context)


def choose(request):
    context = {
        'title': 'Choose',
    }

    return render(request, 'reports/choose.html', context)
