from django.shortcuts import render, redirect
from django.db.models import Q
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import User, UserMessages
from .forms import RegistrationForm, CustomAuthenticationForm, SendMessaggesForm
from django.contrib import auth

# Create your views here.

@login_required
def index(request):
    # Получите список чатов или пользователей с которыми была переписка
    users_with_messages_list = UserMessages.objects.filter(Q(sender=request.user) | Q(reciever=request.user)).values_list('sender', 'reciever')
    users = User.objects.filter(Q(id__in=[user[0] for user in users_with_messages_list]) | Q(id__in=[user[1] for user in users_with_messages_list])).exclude(id=request.user.id)
    return render(request, 'index.html', {'users':users})


def login(request):
    login_form = CustomAuthenticationForm()
    registration_form = RegistrationForm()
    context = {'login_form': login_form, 'registration_form': registration_form}
    

    if request.method == 'POST':
        
        if 'login' in request.POST:
            global error_login 
            login_form = CustomAuthenticationForm(request, request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = auth.authenticate(request, username=username, password=password)
                if user:
                    auth.login(request, user)
                    return redirect('index')
        elif 'registration' in request.POST:
            registration_form = RegistrationForm(request.POST)
            if registration_form.is_valid():
                user = registration_form.save()
                auth.login(request, user)
                return redirect('index')
    
    print(context)
    return render(request, 'login.html', context)


# def registration(request):
#     if request.method != 'POST':
#         form = RegistrationForm()
#     else:
#         form = RegistrationForm(request.POST)
#         if form.is_valid():
#             user = form.save()
#             auth.login(request, user)
#             return redirect('index')
#     return render(request, 'registration.html', {'form': form})


@login_required
def logout(request):
    auth.logout(request)
    return redirect('login')


@login_required
def user_search(request):
    query = request.GET.get('q')
    users_search = User.objects.filter(username__icontains=query) if query else []
    context = {'query': query, 'users_search': users_search}
    return render(request, 'index.html', context)


@login_required
def user_chat(request, sender_id, reciever_id):
    sender = User.objects.get(id=sender_id)
    reciever = User.objects.get(id=reciever_id)

    # Фильтрация сообщений отправителя. Это дает нам сообщения, которые отправлены от отправителя к получателю.
    sender_messages = UserMessages.objects.filter(sender=sender, reciever=reciever)
    # Фильтрация сообщений получателя
    reciever_messages = UserMessages.objects.filter(sender=reciever, reciever=sender)
    # Объединение результатов в один список. Это дает нам сообщения, которые отправлены от получателя к отправителю.
    messages = sender_messages.order_by('time_stamp') | reciever_messages.order_by('time_stamp')

    # Получите список пользователей с которыми была переписка
    # users_with_messages_list = UserMessages.objects.filter(Q(sender=sender) | Q(sender=reciever)).values_list('reciever', flat=True)

    users_with_messages_list = UserMessages.objects.filter(Q(sender=request.user) | Q(reciever=request.user)).values_list('sender', 'reciever')
    users_with_messages = User.objects.filter(Q(id__in=[user[0] for user in users_with_messages_list]) | Q(id__in=[user[1] for user in users_with_messages_list])).exclude(id=request.user.id)

    # Убираем из списка юзеров, текущего юзера
    # users_with_messages = User.objects.filter(id__in=users_with_messages_list).exclude(id=request.user.id)

    if request.method != 'POST':
        form = SendMessaggesForm()
    else:
        form = SendMessaggesForm(request.POST)

        if form.is_valid():
            message_text = form.cleaned_data['message']
            new_message = UserMessages(sender=sender, reciever=reciever, message=message_text)
            new_message.save()
        
            return redirect(request.META.get('HTTP_REFERER'))
    
    context = {'form': form, 
               'sender': sender, 
               'reciever':reciever,
               'messages': messages,
               'users': users_with_messages}
    return render(request, 'user_chat.html', context)

    

