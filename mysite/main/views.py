import datetime
from hashlib import md5
import random

from django.shortcuts import render, redirect
from main.models import *
import requests
import json
from django.http import HttpResponse
from django.db.models import Q


def get_random_number(random_len):
    random_len = int(random_len)
    a = pow(10, random_len)
    b = pow(10, random_len-1)
    n = random.randint(b, a)
    return n


def send_message(phone, sms):
    sms_domain = 'https://smsc.kz/sys/send.php'
    sms_params = {
        'login': 'sanzharirissaliyev',
        'psw': '$anko.Sanko',
        'mes': sms,
        'fmt': 3,
        'phones': phone,
    }
    r = requests.post(sms_domain, data=sms_params)
    print(r.status_code)
    print(r.json())
    print(phone)
    print(sms)


def mainHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    search_value = request.GET.get('q', '')
    if user_id:
        active_user = Siteuser.objects.get(id=int(user_id))

    if request.POST:
        to_user_id = request.POST.get('to_user_id', 0)
        group_id = request.POST.get('group_id', 0)
        date_time = datetime.datetime.now()
        sms = request.POST.get('sms', '')
        status = 0
        sms_item = Sms()
        sms_item.from_user_id = int(user_id)
        sms_item.to_user_id = int(to_user_id)
        sms_item.group_id = int(group_id)
        sms_item.sms = sms
        sms_item.status = status
        sms_item.date_time = date_time
        sms_item.save()

        send_data = {"success": True, "_success": True}
        json_data = json.dumps(send_data)
        return HttpResponse(json_data, content_type="application/json")

#    sm.from_user_id == active_user.id or sm.to_user_id == active_user.id
    users_list = Siteuser.objects.all()
    user_list_obj = {}
    for us in users_list:
        new_us = {
            "last_name": us.last_name,
            "first_name": us.first_name,
            "id": us.id,
            "avatar": us.avatar,
            "phone": us.phone,
            "unread_sms_count": 0
        }
        user_list_obj[us.id] = new_us

    sms_list = Sms.objects.filter(Q(from_user_id=user_id)|Q(to_user_id=user_id)).order_by('date_time')
    pop = Sms.objects.filter(Q(from_user_id=user_id)|Q(to_user_id=user_id)).order_by('-date_time')[0]
    print("30"*100)
    print(pop)
    for sl in sms_list:
        if sl.to_user_id == user_id and sl.status == 0:
            sl.status = 1
            sl.save()
        if sl.to_user_id == user_id and sl.status == 1:
            user_list_obj[sl.from_user_id]["unread_sms_count"] += 1

    active_chat_id = 0
    users_list = []
    if active_user:
        # if search_value:
        #     users_list = Siteuser.objects.filter(last_name__contains=search_value)
        #     for i in users_list:
        #         if i.id != user_id:
        #             active_chat_id = i.id
        #             break
        # else:
        for i in users_list:
            if i.id != user_id:
                active_chat_id = i.id
                break
    print(users_list)
    users_list_new = []
    for i in user_list_obj:
        users_list_new.append(user_list_obj[i])

    return render(request, 'index.html', {
        'user_id': user_id,
        'active_user': active_user,
        'users_list': users_list_new,
        'active_chat_id': active_chat_id,
        'sms_list': sms_list,
        'pop': pop
    })


def msgHandler(request):
    user_id = request.session.get('user_id', None)
    active_user = None
    if user_id:
        active_user = Siteuser.objects.get(id=int(user_id))

    if request.GET:
        action = request.GET.get('action', '')
        if action == 'get_all_new_messages':
            to_user_id = int(user_id)
            sms_list = Sms.objects.filter(Q(to_user_id = to_user_id) & Q(status = 0)).order_by('date_time')
            new_sms_list = []
            for sl in sms_list:
                new_sms = {
                    "from_user_id": sl.from_user_id,
                    "to_user_id": sl.to_user_id,
                    "sms": sl.sms,
                    "date_time": str(sl.date_time)[:19],
                    "status": sl.status
                }
                print("***"*10)
                print(sl)
                sl.status = 1
                sl.save()
                new_sms_list.append(new_sms)

            send_data = {"success": True, "_success": True, "sms_list": new_sms_list}
            json_data = json.dumps(send_data)
            return HttpResponse(json_data, content_type="application/json")

    if request.POST:
        print('*'*100)
        print('read_all_sms')
        action = request.POST.get('action', None)
        if action == 'read_all_sms':
            from_user_id = int(request.POST.get('from_user_id', 0))
            if from_user_id:
                sms_list = Sms.objects.filter(Q(from_user_id=from_user_id) & Q(to_user_id=user_id)).order_by('date_time')
                for sl in sms_list:
                    if sl.to_user_id == user_id and sl.status in [0, 1]:
                        sl.status = 2
                        sl.save()

    return HttpResponse({"success": True, "_success": True}, content_type="application/json")


def loginHandler(request):
    post_error = ''
    if request.POST:
        login = request.POST.get('login', '')
        password = request.POST.get('password', '')
        if login and password:

            temp_hash = md5()
            temp_hash.update(password.encode())
            password_hash = temp_hash.hexdigest()

            site_user = Siteuser.objects.filter(phone=login).filter(password=password_hash)
            if not site_user:
                site_user = Siteuser.objects.filter(email=login).filter(password=password_hash)
            if site_user:
                site_user = site_user[0]
                request.session['user_id'] = site_user.id
                return redirect('/')
            else:
                post_error = 'USER_NOT_FOUND'
        else:
            post_error = 'ERROR_ARGUMENTS'

    return render(request, 'login.html', {'post_error': post_error})


def logoutHandler(request):
    request.session['user_id'] = None
    return redirect('/')

    return render(request, 'logout.html', {})


def registerHandler(request):
    if request.POST:
        phone = request.POST.get('phone', '')
        if phone:
            if len(phone) == 11:
               site_user = Siteuser.objects.filter(phone=phone)
               if site_user:
                   new_site_user = site_user[0]
                   old_password = str(get_random_number(4))
                   password_hash = md5()
                   password_hash.update(old_password.encode())
                   new_passwoord = password_hash.hexdigest()
                   new_site_user.password = new_passwoord
                   new_site_user.save()
                   message = 'Kod dlya registrasiya ' + str(old_password)
                   send_message(phone, message)
                   return redirect('/login/')
               else:
                   new_site_user = Siteuser()
                   new_site_user.phone = phone
                   old_password = str(get_random_number(4))
                   print("****"*10)
                   print(old_password)
                   password_hash = md5()
                   password_hash.update(old_password.encode())
                   new_passwoord = password_hash.hexdigest()
                   new_site_user.password = new_passwoord
                   new_site_user.save()
                   message = 'Kod dlya registrasiya ' + str(old_password)
                   #send_message(phone, message)
                   return redirect('/login/')
            else:
                print('FORMAT ErROR')
        else:
            print('NO ARGUMRNT')
    return render(request, 'register.html', {})
