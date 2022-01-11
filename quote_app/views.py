from django.shortcuts import render
from django.shortcuts import render, redirect
import bcrypt
from . models import *
from django.contrib import messages



def index(request):
    return render(request, 'index.html')
def register(request): 
    if request.method == 'POST':
        errors = User.objects.basic_validator(request.POST)
        if User.objects.filter(email_address = request.POST['email_address']):
            messages.error(request, 'Email is alreay registered. Please use login!')
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/')
        else:
            password = request.POST['password']
            pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode() 
            new_user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email_address = request.POST['email_address'], 
            password = pw_hash,
            ) 
            request.session['userid']= new_user.id
            return redirect('/login')
    return redirect( '/')

def login(request):
    if 'userid' in request.session:
        user = User.objects.filter(id = request.session['userid'])
        if user:
            context = {
                'user': user[0],
            }
            return render(request, 'success.html', context)
    return redirect('/')

def validate_login(request):
    user = User.objects.filter(email_address = request.POST['email_address']) 
    if user:
        login_user = user[0]
        if bcrypt.checkpw(request.POST['password'].encode(), login_user.password.encode()):
            request.session['userid'] = login_user.id
            return redirect('/quotes')
    else:
        return redirect('/')
def quotes(request):
    if 'userid' in request.session:
        user = User.objects.filter(id = request.session['userid'])
        if user:
            context = {
                'user': user[0],
                'display_quotes' : Quote.objects.all(),
            }
            return render(request, 'quotes.html', context)
    return redirect('/')

def add_quote(request):
    if request.method == 'POST':
        errors = Quote.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/quotes')
        else:
            user_quote = User.objects.get(id = request.session['userid'])
            Quote.objects.create(
                user_quote = user_quote,
                author = request.POST['author'],
                desc = request.POST['desc'],
            )
    return redirect('/quotes')
def edit_page(request, quote_id):
    context = {
        'quote': Quote.objects.get(id=quote_id),
        'user_quote' : User.objects.get(id = request.session['userid'])
    }
    return render(request, 'edit.html', context)

def edit(request, quote_id):
    if request.method == 'POST':
        errors = Quote.objects.basic_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/edit/{quote_id}')
        else:
            quote = Quote.objects.get(id=quote_id)
            quote.user_quote = User.objects.get(id = request.session['userid'])
            quote.desc = request.POST['desc']
            quote.author = request.POST['author']
            quote.save()
    return redirect('/quotes')

def delete_quote(request, quote_id):
    delete_quote = Quote.objects.get(id=quote_id)
    delete_quote.delete()
    return redirect('/quotes')

def user_page(request, user_id):
    user = User.objects.get(id=user_id)
    quotes_by_user = Quote.objects.filter(user_quote = user_id)
    context = {
                'user': user,
                'quotes' : quotes_by_user,
            }
    return render(request, "user.html", context)

def logout(request):
    request.session.flush()
    return redirect('/')