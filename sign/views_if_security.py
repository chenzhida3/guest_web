# -*- coding: utf-8 -*-
'''
 @File    : views_if_security.py
 @Time    : 2019/6/25 9:55
 @Author  : Chenzd
 @Project : 签名加密
 @Software: PyCharm
'''
import time
import hashlib

from django.core.exceptions import ValidationError
from django.http import JsonResponse

from sign.models import Event


def user_sign(request):
    '''用户签名'''
    client_time = request.POST.get('time', '')
    client_sign = request.POST.get('sign', '')
    if client_sign == '' or client_time == '':
        return "sign null"
    now_time = time.time()
    server_time = str(now_time).split('.')[0]
    defferent_time = int(server_time)-int(client_time)
    if defferent_time >= 60:
        return "timeout"
    md5 = hashlib.md5()
    sign_str = client_time + "&Guest-Bugmaster"
    sign_bytes_utf8 = sign_str.encode(encoding="utf-8")
    md5.update(sign_bytes_utf8)
    server_md5 = md5.hexdigest()
    if client_sign != server_md5:
        return "sign error"
    else:
        return "sign right"

def add_event(request):
    '''添加发布会接口'''
    sign_result = user_sign(request)
    if sign_result == 'sign null':
        return JsonResponse({'status': 10011, 'message': 'user sign null'})
    if sign_result == 'timeout':
        return JsonResponse({'status': 10012, 'message': 'user sign timeout'})
    if sign_result == 'sign error':
        return JsonResponse({'status': 10013, 'message': 'user sign error'})

    eid = request.POST.get('eid', '')  # 发布会id
    name = request.POST.get('name', '')  # 发布会标题
    limit = request.POST.get('limit', '')  # 限制人数
    status = request.POST.get('stauts', '')  # 状态
    address = request.POST.get('address', '')  # 地址
    start_time = request.POST.get('start_time', '')  # 发布会时间
    if eid == '' or name == '' or limit == '' or address == '' or start_time == '':
        return JsonResponse({'status': 10021, 'message': 'parameter error'})
    result = Event.objects.filter(id=eid)
    if result:
        return JsonResponse({'status': 10022, 'message': 'event id already exits'})
    result = Event.objects.filter(name=name)
    if result:
        return JsonResponse({'status': 10023, 'message': 'event name already exits'})
    if status == '':
        status = 1
    else:
        status = 0
    try:
        Event.objects.create(id=eid, name=name, limit=limit, address=address, status=int(status), start_time=start_time)
    except ValidationError as e:
        error = 'start_time format error.It must be in YYYY-MM-DD HH:MM:SS format.'
        return JsonResponse({'status': 10024, 'message': error})
    return JsonResponse({'status': 200, 'message': 'add event success'})