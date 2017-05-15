from django.shortcuts import render


def index(request):
    context = {
        'sent_things': ['a', 'test', 'list']
    }
    return render(request, 'index.html', context=context)