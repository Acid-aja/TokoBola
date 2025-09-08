from django.shortcuts import render

def show_main(request):
    context = {
        'npm' : '2406495786',
        'name' : 'Rasyid',
        'class' : 'PBP D'
    }

    return render(request, "main.html", context)