from django.shortcuts import render, redirect
from django.db import connection
from django.urls import reverse
from django.views.generic import TemplateView
from django.contrib.auth.models import User,auth
from django.contrib import messages
from web_scraping import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from datetime import datetime
from django.http import JsonResponse




@login_required(login_url='login_user')  # Redirige vers la page 'login_user' si non connecté
def index(request):
    url = request.POST.get('url')
    return render(request, 'index.html', {'url': url})

# @login_required
# def index(request):
#     url = request.POST.get('url')
#     return render(request, 'acces.html', {'url': url})





def list_and_display_tables(request):
# Récupérer la liste des noms de tables de la base de données
    with connection.cursor() as cursor:
        cursor.execute("SHOW TABLES")
        all_table_names = [row[0] for row in cursor.fetchall()]

    # Filtrer les noms de tables pour inclure uniquement 'solar_data' et 'scraping_data'
    table_names = [table_name for table_name in all_table_names if table_name in ['solar_data', 'scraping_data']]

    return render(request, 'list_and_display_tables.html', {'table_names': table_names})


# def display_table(request, table_name):
#     with connection.cursor() as cursor:
#         sort_column = request.GET.get('sort', 'date_ajout')
#         sort_order = request.GET.get('order', 'desc')

#         order_symbol = '-' if sort_order == 'desc' else ''

#         query = f"SELECT * FROM {table_name} ORDER BY {order_symbol}{sort_column}"
        
#         search_date = request.GET.get('search_date')
#         if search_date:
#             query = f"SELECT * FROM {table_name} WHERE date_ajout = '{search_date}' ORDER BY {order_symbol}{sort_column}"
        
#         cursor.execute(query)

#         columns = [col[0] for col in cursor.description]
#         data = cursor.fetchall()

#     return render(request, 'display_table.html', {'table_name': table_name, 'columns': columns, 'data': data})


def display_table(request, table_name):
    with connection.cursor() as cursor:
        sort_column = request.GET.get('sort', 'date_ajout')
        sort_order = request.GET.get('order', 'desc')

        order_symbol = '-' if sort_order == 'desc' else ''

        query = f"SELECT * FROM {table_name} ORDER BY {order_symbol}{sort_column}"
        
        search_date_start = request.GET.get('search_date_start')
        search_date_end = request.GET.get('search_date_end')
        
        if search_date_start and search_date_end:
            start_date = datetime.strptime(search_date_start, '%Y-%m-%d')
            end_date = datetime.strptime(search_date_end, '%Y-%m-%d')
            
            query = f"SELECT * FROM {table_name} WHERE date_ajout BETWEEN '{start_date.date()}' AND '{end_date.date()}' ORDER BY {order_symbol}{sort_column}"
        
        cursor.execute(query)

        columns = [col[0] for col in cursor.description]
        data = cursor.fetchall()

        paginator = Paginator(data, 7)  # Change 10 to the number of items per page you want
        page_number = request.GET.get('page')
        page_data = paginator.get_page(page_number)

    return render(request, 'display_table.html', {
        'table_name': table_name,
        'columns': columns,
        'data': page_data,
    })


# def login_user(request):
#     if request.user.is_authenticated:  # Vérifie si l'utilisateur est déjà connecté
#         return redirect('index')  # Redirige vers la page d'accueil

#     if request.method == 'POST':
#         username = request.POST['username']
#         password = request.POST['password']

#         user = auth.authenticate(username=username, password=password)

#         if user is not None:
#             auth.login(request, user)
#             return redirect('index')
#         else:
#             messages.info(request, 'Invalid Username or password')
#             return redirect('login_user') 
#     else:
#         return render(request, "login.html")




def login_user(request):
    if request.user.is_authenticated:
        if request.user.is_staff:
            return redirect('admin:index')  # Redirect to admin dashboard
        else:
            return redirect('index')  # Redirect to the index page

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            if user.is_staff:
                return redirect('admin:index')  # Redirect to admin dashboard
            else:
                return redirect('index')  # Redirect to the index page
        else:
            messages.info(request, 'Invalid Username or password')
            return redirect('login_user')
    else:
        return render(request, "login.html")




def logout_user(request):
    auth.logout(request)
    return redirect('login_user')

 

def return_hello(request):
    if request.method == 'POST':
        try:
            username = request.POST.get('username')
            return JsonResponse({"error": False, "message": f"Hello {username}!"})
        except Exception as e:
            return JsonResponse({"error": True, "message": str(e)})
    else:
        return JsonResponse({"error": True, "message": "Invalid request method."})






# def handler_404(request):
#     return render(request, '404.html', status=404)