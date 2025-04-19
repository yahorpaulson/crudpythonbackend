from django.shortcuts import render
from django.shortcuts import redirect
from .models import Note
from django.http import HttpResponse, JsonResponse
from .models import UserTokenPair
from .forms import NoteForm, UserForm
from django.contrib import messages
from django.shortcuts import render, redirect
from myapp.auth import auth
from myapp.tokens import refresh_access_token, create_token_pair, get_user_by_token, delete_token_pair
from myapp.register import register_user


# Create your views here.

def register(request):
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                register_user(form.cleaned_data)
                messages.success(request, 'User registered successfully')
                return redirect('login')
            except ValueError as e:
                form.add_error(None, str(e))
    else:
        form = UserForm()

    return render(request, 'register.html', {'form': form})

def login(request):
    if request.method == 'POST':
        username= request.POST.get('username')
        password= request.POST.get('password')

        user = auth(username, password)

        if user:
            UserTokenPair.objects.filter(user=user).delete()

            token = create_token_pair(user)
            response = redirect('main')
            response.set_cookie('access_token', token['access'])
            response.set_cookie('refresh_token', token['refresh'])
            return response
        
        return JsonResponse({'error': 'Invalid credentials'}, status=401)
    return render(request, 'login.html')



def main_view(request):
    access_token = request.COOKIES.get('access_token')
    if not access_token:
        messages.error(request, 'Login first!')
        return redirect('login')
    
    user = get_user_by_token(access_token)
    if not user:
        messages.error(request, 'Session expired! Please login again.')
        return redirect('login')

    return render(request, 'main.html', {'user': user})

def refresh_token(request):
    refresh_token = request.COOKIES.get('refresh_token')


    if not refresh_token:
        return JsonResponse({'error': 'No refresh token'})
    
    try:
        data = refresh_access_token(refresh_token)
        response = JsonResponse({'message':'Access token refreshed'})
        response.set_cookie('access_token', data['access'])
        return response
    except Exception as e:
        return JsonResponse({'error', str(e)}, status=401)


def logout(request):
    access_token = request.COOKIES.get('access_token')
    if access_token:
        user = get_user_by_token(access_token)
        delete_token_pair(user.id)


    response = redirect('login') 
    response.delete_cookie('access_token') #delete from users browser
    response.delete_cookie('refresh_token') 
    return response



        


def note_list_create(request):
    if request.method == 'POST':
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        color = request.POST.get('color')

        owner_id = request.POST.get('owner_id')
        
        Note.objects.create(
            title=title,
            content=content,
            color=color,
            owner_id=owner_id
        )

        return redirect('note_list')
    

    notes = Note.objects.all()

    return HttpResponse("Note list create view")


def notes_get(request, user_id):
    if request.method == 'GET':
        notes = Note.objects.filter(owner_id=user_id)
        return render(request, 'notes_get.html', {'notes': notes})
    else:
        return HttpResponse("Method not allowed", status=405)
    
def notes_get_by_id(request, user_id, note_id):
    if request.method == 'GET':
        try:
            note = Note.objects.get(owner_id=user_id, id=note_id)
            return render(request, 'notes_get_by_id.html', {'note': note})
        except Note.DoesNotExist:
            return HttpResponse("Note not found", status=404)
    else:
        return HttpResponse("Method not allowed", status=405)
    

def main_view(request):
    access_token = request.COOKIES.get('access_token')
    print("ACCESS_TOKEN:", access_token)

    user = get_user_by_token(access_token)
    print("USER:", user)

    if not user:
        messages.error(request, 'Session expired!')
        return redirect('login')

    return render(request, 'main.html', {'user': user})

    




def notes_delete(request, user_id, note_id):
    if request.method == 'POST':
        try:
            note = Note.objects.get(owner_id=user_id, id=note_id)
            note.delete()
            return redirect('note_list')
        except Note.DoesNotExist:
            return HttpResponse("Note not found", status=404)
    else:
        return HttpResponse("Method not allowed", status=405)
    

    def refresh_token(request):
        if request.method == 'POST':
            refresh = request.POST.get('refresh')
            try:
               result = refresh_access_token(refresh)
               return JsonResponse(result, status=200)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=401)
            

