from django.shortcuts import render, get_object_or_404

def index(request):
    context = {
        'header' : 'Maintenance'
    }
    return render(request, 'index.html', context)
