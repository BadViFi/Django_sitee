from django.shortcuts import render, redirect
from apps.chat.models import Room, Message
from django.http import HttpResponse, JsonResponse
from apps.members.models import Profile
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404

from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
# Create your views here.
def home(request):
    recent_chat_rooms = Room.objects.order_by('-id')[:10]  
    return render(request, 'home.html', {'recent_chat_rooms': recent_chat_rooms})

def room(request, room):
    if request.user.is_authenticated:
        username = request.user.username
        profile = Profile.objects.get(user=request.user)
        avatar_url = profile.get_avatar()
    else:
        username = 'Anonymous'
        avatar_url = '/media/avatars/default.png' 

    room_details = Room.objects.get(name=room)
    return render(request, 'room.html', {
        'username': username,
        'room': room,
        'room_details': room_details,
        'avatar_url': avatar_url,
    })


def checkview(request):
    room = request.POST['room_name']
    username = request.POST['username']
    
    if Room.objects.filter(name=room).exists():
        return redirect('/' + 'chat/' + room + '/?username=' + username)
    else:
        new_room = Room.objects.create(name=room)
        new_room.save()
        return redirect('/' + 'chat/' + room + '/?username=' + username)
    
def send(request):
    message = request.POST['message']
    username = request.POST['username']
    room_id = request.POST['room_id']

    new_message = Message.objects.create(value=message, user=username, room=room_id)
    new_message.save()
    return HttpResponse('Message sent successfully')

def getMessages(request, room):
    room_details = Room.objects.get(name=room)
    messages = Message.objects.filter(room=room_details.id)
    serialized_messages = []
    for message in messages:
        try:
            user = User.objects.get(username=message.user)
            profile = Profile.objects.get(user=user)
            avatar_url = profile.get_avatar()
        except (User.DoesNotExist, Profile.DoesNotExist):
            avatar_url = '/media/avatars/default.png'
        
        serialized_message = {
            'id': message.id,
            'value': message.value,
            'user': message.user,
            'date': message.date,
            'avatar_url': avatar_url
        }
        serialized_messages.append(serialized_message)
    return JsonResponse({"messages": serialized_messages})


@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.user == request.user.username:
        if request.method == 'POST':
            new_message_value = request.POST['message']
            message.value = new_message_value
            message.save()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'You are not allowed to edit this message.'})

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id)
    if message.user == request.user.username:
        if request.method == 'POST':
            message.delete()
            return JsonResponse({'success': True})
    return JsonResponse({'success': False, 'error': 'You are not allowed to delete this message.'})





