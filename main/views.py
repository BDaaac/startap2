from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Teacher, Profile, ShopItem, ChatMessage, Transaction
from .forms import BecomeTeacherForm, ProfileForm, ShopItemForm, DepositForm
from django.contrib.auth.decorators import login_required
from .models import ChatMessage
from django.db.models import Q


def main_view(request):
    return render(request, 'main/main.html')


def home(request):
    query = request.GET.get("q", "")
    teachers = Teacher.objects.all()
    if query:
        teachers = teachers.filter(
            Q(name__icontains=query) | Q(directions__icontains=query)
        )
    return render(request, "main/menu.html", {"teachers": teachers})

@login_required
def become_teacher(request):
    if request.method == "POST":
        form = BecomeTeacherForm(request.POST, request.FILES)
        if form.is_valid():
            teacher = form.save(commit=False)
            teacher.user = request.user
            teacher.save()
            return redirect('menu')
    else:
        form = BecomeTeacherForm()

    return render(request, 'main/profile.html', {'form': form})


def menu(request):
    teachers = Teacher.objects.all()

    q = request.GET.get('q', '').strip()
    if q:
        teachers = teachers.filter(
            Q(name__icontains=q) | Q(directions__icontains=q)
        )

    directions_param = request.GET.get('directions', '').strip()
    if directions_param:
        direction_list = [d.strip() for d in directions_param.split(',') if d.strip()]
        q_direction = Q()
        for d in direction_list:
            q_direction |= Q(directions__icontains=d)
        teachers = teachers.filter(q_direction)

    price_param = request.GET.get('price', '').strip()
    if price_param:
        try:
            price_limit = float(price_param)
            teachers = teachers.filter(price__lte=price_limit)
        except ValueError:
            pass

    return render(request, "main/menu.html", {"teachers": teachers})


def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, "main/teacher_detail.html", {"teacher": teacher})
@login_required
def profile_view(request):

    return render(request, 'main/my_profile.html', {'user': request.user})



@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('my_profile')
    else:
        form = ProfileForm(instance=profile)

    return render(request, 'main/edit_profile.html', {'form': form})


@login_required
def toggle_favorite(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    profile = request.user.profile
    if teacher in profile.favorite_teachers.all():
        profile.favorite_teachers.remove(teacher)
    else:
        profile.favorite_teachers.add(teacher)
    return redirect('menu')
@login_required
def my_profile(request):
    profile = request.user.profile
    chat_data = (
        ChatMessage.objects.filter(Q(sender=request.user) | Q(receiver__in=Teacher.objects.all()))
        .values('receiver_id')
        .annotate(last_message_time=Max('timestamp'))
        .order_by('-last_message_time')
    )

    chats = []
    for data in chat_data:
        teacher = get_object_or_404(Teacher, id=data['receiver_id'])
        last_message = ChatMessage.objects.filter(
            Q(sender=request.user, receiver=teacher) | Q(sender=teacher, receiver=request.user)
        ).order_by('-timestamp').first()
        chats.append({
            'teacher': teacher,
            'last_message': last_message.message if last_message else '',
            'timestamp': last_message.timestamp if last_message else None,
        })

    return render(request, 'main/my_profile.html', {'profile': profile, 'chats': chats})



@login_required
def chat_with_teacher(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    teacher_user = teacher.user  # Это экземпляр User
    if request.method == "POST":
        message_text = request.POST.get('message')
        if message_text:
            ChatMessage.objects.create(
                sender=request.user,
                receiver=teacher_user,  # Теперь receiver — объект User
                message=message_text
            )
        return redirect('chat_with_teacher', teacher_id=teacher.id)

    messages = ChatMessage.objects.filter(
        Q(sender=request.user, receiver=teacher_user) | Q(sender=teacher_user, receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'main/chat.html', {'teacher': teacher, 'messages': messages})


@login_required
def profile_view(request):
    profile = Profile.objects.get(user=request.user)

    chats = ChatMessage.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).values('sender', 'receiver').distinct()

    chat_users = set()
    for chat in chats:
        if chat['sender'] == request.user.id:
            chat_users.add(chat['receiver'])
        else:
            chat_users.add(chat['sender'])

    chat_teachers = Teacher.objects.filter(user__id__in=chat_users)

    return render(request, 'main/my_profile.html', {
        'chats': chat_teachers,
        'balance': profile.balance
    })

@login_required
def my_teacher_profile(request):
    teacher = Teacher.objects.filter(user=request.user).first()

    if not teacher:
        return redirect('profile')

    teacher_ads = []

    if request.method == 'POST':
        form = TeacherProfileForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('my_teacher_profile')
    else:
        form = TeacherProfileForm(instance=teacher)

    return render(request, 'main/my_teacher_profile.html', {'form': form, 'teacher_ads': teacher_ads})


def teacher_detail(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id)
    return render(request, 'main/teacher_detail.html', {'teacher': teacher})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import TeacherProfileForm
from .models import Teacher  # Убедись, что модель Teacher импортируется
@login_required
def my_teacher_ads(request):
    """ Отображает список всех преподавателей (как объявления) текущего пользователя """
    teachers = Teacher.objects.filter(user=request.user)  # Теперь это твои "объявления"

    return render(request, 'main/my_teacher_ads.html', {'teacher_ads': teachers})


@login_required
def edit_teacher_ad(request, teacher_id):
    """ Позволяет редактировать данные преподавателя """
    teacher = get_object_or_404(Teacher, id=teacher_id, user=request.user)

    if request.method == 'POST':
        form = BecomeTeacherForm(request.POST, request.FILES, instance=teacher)
        if form.is_valid():
            form.save()
            return redirect('my_teacher_ads')
    else:
        form = BecomeTeacherForm(instance=teacher)

    return render(request, 'main/edit_teacher_ad.html', {'form': form, 'teacher': teacher})


@login_required
def chat_list(request):
    chats = (
        ChatMessage.objects.filter(Q(sender=request.user) | Q(receiver=request.user))
        .values('receiver_id')
        .distinct()
    )

    chat_teachers = Teacher.objects.filter(user__id__in=[chat['receiver_id'] for chat in chats])

    return render(request, 'main/chat_list.html', {'chats': chat_teachers})

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Teacher

@login_required
def delete_teacher_ad(request, teacher_id):
    teacher = get_object_or_404(Teacher, id=teacher_id, user=request.user)

    if request.method == 'POST':
        teacher.delete()
        return redirect('my_teacher_ads')

    return render(request, 'main/delete_teacher_ad.html', {'teacher': teacher})


@login_required
def deposit_balance(request):
    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            amount = form.cleaned_data['amount']
            profile = request.user.profile
            profile.balance += amount
            profile.save()

            Transaction.objects.create(user=request.user, amount=amount, transaction_type='deposit')

            return redirect('menu')
    else:
        form = DepositForm()

    return render(request, 'main/deposit.html', {'form': form})
from django.shortcuts import render
from .models import ShopItem

@login_required
def shop_view(request):
    items = ShopItem.objects.filter(available=True)
    return render(request, 'main/shop.html', {'items': items})


@login_required
def buy_item(request, item_id):
    item = get_object_or_404(ShopItem, id=item_id)
    profile = request.user.profile

    if profile.balance < item.price:
        messages.error(request, "Недостаточно средств!")
        return redirect('shop')

    profile.balance -= item.price
    profile.owned_items.add(item)
    profile.save()

    messages.success(request, f"Вы купили {item.name}!")
    return redirect('shop')

@login_required
def purchase_history(request):
    purchases = Purchase.objects.filter(user=request.user).order_by('-purchased_at')
    return render(request, 'main/purchase_history.html', {'purchases': purchases})



@login_required
def add_shop_item(request):
    if request.method == "POST":
        form = ShopItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('shop')
    else:
        form = ShopItemForm()

    return render(request, 'main/add_shop_item.html', {'form': form})
@login_required
def customize_profile(request):
    profile = request.user.profile
    backgrounds = profile.owned_items.filter(category="background")
    frames = profile.owned_items.filter(category="frame")
    icons = profile.owned_items.filter(category="icon")

    if request.method == "POST":
        bg_id = request.POST.get("background")
        frame_id = request.POST.get("frame")
        icon_id = request.POST.get("icon")

        if bg_id:
            profile.selected_background = ShopItem.objects.get(id=bg_id)
        if frame_id:
            profile.selected_frame = ShopItem.objects.get(id=frame_id)
        if icon_id:
            profile.selected_icon = ShopItem.objects.get(id=icon_id)

        profile.save()
        messages.success(request, "Профиль обновлен!")
        return redirect('my_profile')

    return render(request, 'main/customize_profile.html', {
        "backgrounds": backgrounds,
        "frames": frames,
        "icons": icons,
        "profile": profile
    })
