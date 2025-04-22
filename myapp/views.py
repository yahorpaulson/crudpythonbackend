
from .models import Note
from django.http import  JsonResponse
from .models import UserTokenPair
from .forms import UserForm
from django.shortcuts import render, redirect
from myapp.auth import auth
from myapp.tokens import refresh_access_token, create_token_pair, get_user_by_token, delete_token_pair
from myapp.register import register_user
from myapp.services import get_all_notes, validate_user





def register(request):
    
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            try:
                register_user(form.cleaned_data)
                print('User registered successfully')
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
    validate_user(request)

    return render(request, 'main.html')



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


def create_note(request):
    return redirect('add_note')



        


def add_note(request):
    if request.method == 'POST':
        
        title = request.POST.get('title')
        content = request.POST.get('content')
        color = request.POST.get('color')

        user = validate_user(request)

        owner_id = user.id
        
        Note.objects.create(
            title=title,
            content=content,
            color=color,
            owner_id=owner_id
        )

        return redirect('notes')
    

    return render(request, 'add_note.html')




def deleteNoteByTitle(request):
    user = validate_user(request)
    
    if request.method == 'POST':
        if request.POST.get('title') == "":
            print('Empty title field')
            return redirect('notes')

        
        notes = get_all_notes(user.id)

        target_note = None

        for note in notes:
            if note.title == request.POST.get('title'):
                target_note = note
                note.delete()
                return redirect('notes')
        
        if target_note == None:
            print('Not found')

            return redirect('notes')
    

       



def show_notes(request):
    access_token = request.COOKIES.get('access_token')
    user = get_user_by_token(access_token)

    if not user:
        return redirect('login')
    
    notes = get_all_notes(user.id)
    return render(request, 'note_list.html', {'notes': notes})



    

def main_view(request):
    if not validate_user(request):
        return redirect('login')

    return render(request, 'main.html')


def change_note(request):
    if request.method == 'POST':

        user = validate_user(request)

        input_title = request.POST.get('title')

        notes = get_all_notes(user.id)

        for note in notes:
            if note.title == input_title:
                param = request.POST.get('note_params')
                print(param)
                if param == "":
                    print("Empty")
                    param = request.POST.get('note_params_color')
                    print(param + " with color")


                
                
                radio_value = request.POST.getlist('note_params')[0]

                print(radio_value)
            
                if radio_value == "title":
                    note.title = param
                    print(note.title + " is a new Title")
                elif radio_value == "content":
                    note.content = param
                    print(note.content + " is a new Content")
                elif radio_value == "color":
                    note.color = param

                note.save()
           
        
        return redirect('notes')


        
        

    
def refresh_token(request):
    if request.method == 'POST':
        refresh = request.POST.get('refresh')
        try:
            result = refresh_access_token(refresh)
            return JsonResponse(result, status=200)
        except ValueError as e:
            return JsonResponse({'error': str(e)}, status=401)
            

