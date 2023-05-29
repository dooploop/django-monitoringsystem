import difflib
import io
import json
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse
import os
import platform
from datetime import datetime
import time
import psutil
from host.forms import UserLoginForm, UserRegistrationForm

# Create your views here.

from host.tools import get_md5


def index(request):
    try:
        system_info = os.uname()
        node = system_info.nodename
        system = system_info.sysname
    except Exception as e:
        system_info = platform.uname()
        node = system_info.node
        system = system_info.system

    boot_time = psutil.boot_time()
    boot_time = datetime.fromtimestamp(boot_time)
    now_time = datetime.fromtimestamp(time.time())
    info = {
        'node': node,
        'system': system,
        "kernel_name": system,
        'release': system_info.release,
        'version': system_info.version,
        'machine': system_info.machine,
        'now_time': now_time,
        'boot_time': boot_time,
        'boot_delta': now_time - boot_time
    }
    return render(request, 'index.html', {'info': info})


@login_required
def disk(request):
    parts = psutil.disk_partitions()
    disks = []
    for part in parts:
        usage = psutil.disk_usage(part.device)
        disk = {
            'device': part.device,
            'mountpoint': part.mountpoint,
            'fstype': part.fstype,
            'opts': part.opts,
            'total': usage.total,
            'percent': usage.percent
        }
        disks.append(disk)
    return render(request, 'disk.html', {'disks': disks})

import requests
'''def users(request):
        all_users = []
         [suser(name='Fan', terminal=None, host=None, started=1595661568.4721968, pid=None)]
        users = psutil.users()
        for user in users:
            one_user = {
                'name': user.name,
                'host': user.host,
                'started': datetime.fromtimestamp(user.started)
            }
            all_users.append(one_user)
        res = requests.get('http://127.0.0.1:8000/member')
        print(res.content)
        all_users  = json.loads(res.content)
        return render(request, 'users.html', {'users': all_users})'''

   

@login_required
def diff(request):
    print("Запроса: ", request.method)
    if request.method == 'POST':
        files = request.FILES
        content1 = files.get('filename1').read()
        content2 = files.get('filename2').read()

        if get_md5(content1) == get_md5(content2):
            return HttpResponse("Согласованное содержимое файла")
        else:
            hdiff = difflib.HtmlDiff()
            content1 = content1.decode('utf-8').splitlines()
            content2 = content2.decode('utf-8').splitlines()
            result = hdiff.make_file(content1, content2)  
            return HttpResponse(result)
    return render(request, 'diff.html')

def dicttolist(dict):
    listmain = []
    for lists in dict:
        l1 = list(lists.values())
       # print(l1)
        listmain.append(l1)
    return listmain

def monitor(request):
    # the list the contain all process dictionaries
    processes = []
    for process in psutil.process_iter():
        # get all process info in one shot
        with process.oneshot():
            # get the process id
            pid = process.pid
            if pid == 0:
                # System Idle Process for Windows NT, useless to see anyways
                continue
            # get the name of the file executed
            name = process.name()
            # get the time the process was spawned
            try:
                create_time = datetime.fromtimestamp(process.create_time())
            except OSError:
                # system processes, using boot time instead
                create_time = datetime.fromtimestamp(psutil.boot_time())
            try:
                # get the number of CPU cores that can execute this process
                cores = len(process.cpu_affinity())
            except psutil.AccessDenied:
                cores = 0
            # get the CPU usage percentage
            cpu_usage = process.cpu_percent(interval=0.1)
            # get the status of the process (running, idle, etc.)
            status = process.status()
            try:
                # get the process priority (a lower value means a more prioritized process)
                nice = int(process.nice())
            except psutil.AccessDenied:
                nice = 0
            try:
                # get the memory usage in bytes
                memory_usage = process.memory_full_info().uss
            except psutil.AccessDenied:
                memory_usage = 0
            # total process read and written bytes
            io_counters = process.io_counters()
            read_bytes = io_counters.read_bytes
            write_bytes = io_counters.write_bytes
            # get the number of total threads spawned by this process
            n_threads = process.num_threads()
            # get the username of user spawned the process
            try:
                username = process.username()
            except psutil.AccessDenied:
                username = "N/A"
            
        processes.append({
            'program_id': pid, 
            'name': name, 
            'create_time': create_time,
            'cores': cores,
             'cpu_usage': cpu_usage, 
             'status': status, 
             'Приоритет': nice,
            'memory_usage': memory_usage, 
            'n_threads': n_threads
        })
             
       # print(cpu_usage)
   # return processes
   # processes = dicttolist(processes)
    return render(request, 'monitor.html', {'processes': processes})


def apidatas(request):
    return render(request, 'apidatas.html')
@login_required
def about(request):
    return render(request, 'about.html')

def auth(request):
    return render(request, 'auth.html')

from django.shortcuts import render
from .models import Members, UserProfile




from rest_framework import generics
from .serializers import ProgramSerializer
from .models import all_users_data
from rest_framework.response import Response
from rest_framework import status


from rest_framework import generics
from .models import all_users_data
from .serializers import ProgramSerializer
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from rest_framework.views import APIView


class ProgramListView(APIView):

    def post(self, request, *args, **kwargs):
        # get the data from the request
        program_data = request.data
        
        # check if a program with the same program_id exists in the database
        program, created = all_users_data.objects.get_or_create(program_id=program_data['program_id'], defaults=program_data)
        
        if not created:
            # if the program already exists, update its data with the new data
            serializer = ProgramSerializer(program, data=program_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            # if a new program is created, serialize it and return the serialized data
            serializer = ProgramSerializer(program)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
    def get(self, request, *args, **kwargs):
        name = request.GET.get('name')
        if name != "":
         programs = all_users_data.objects.filter(name=name).values()
         if len(programs) < 1 :
            programs = all_users_data.objects.all()
        else:
         programs = all_users_data.objects.all()
        serializer = ProgramSerializer(programs, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ProgramDetailView(APIView):
    @login_required
    def get(self, request, program_id):
        program = all_users_data.objects.filter(program_id=program_id).first()
        if program:
            serializer = ProgramSerializer(program)
            return Response(serializer.data)
        else:
            return Response(status=status.HTTP_404_NOT_FOUND)
    @login_required
    def post(self, request):
        serializer = ProgramSerializer(data=request.data)
        if serializer.is_valid():
            program_id = serializer.validated_data['program_id']
            program, created = all_users_data.objects.get_or_create(program_id=program_id)
            if not created:
                return Response({"detail": "Program with program_id {} already exists".format(program_id)},
                                status=status.HTTP_400_BAD_REQUEST)
            program.program_name = serializer.validated_data['program_name']
            program.name = serializer.validated_data['name']
            program.host = serializer.validated_data['host']
            program.cores = serializer.validated_data['cores']
            program.cpu_usage = serializer.validated_data['cpu_usage']
            program.status = serializer.validated_data['status']
            program.memory_usage = serializer.validated_data['memory_usage']
            program.data = serializer.validated_data['data']
            program.banch_id = serializer.validated_data['banch_id']
            program.save()
            serializer = ProgramSerializer(program)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @login_required
    def put(self, request, program_id):
        program = all_users_data.objects.filter(program_id=program_id).first()
        if not program:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = ProgramSerializer(program, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    @login_required
    def delete(self, request):
        # Delete old programs
        if request.method == 'DELETE':
        # Delete old programs
            threshold = datetime.fromtimestamp(float(request.GET.get('threshold')) / 1000)
            all_users_data.objects.filter(date__lt=threshold).delete()

            return True


from django.shortcuts import render
from django.contrib.auth.models import User
from django.utils import timezone

@login_required
def all_data(request):
    # Вычисляем время 5 минут назад
    five_minutes_ago = timezone.now() - timezone.timedelta(seconds=10)

    # Выбираем все объекты MyModel, у которых created_at меньше, чем five_minutes_ago
    old_objects = all_users_data.objects.filter(data__lt=five_minutes_ago)

    # Удаляем выбранные объекты
    old_objects.delete()
    user = User.objects.all()
    query = request.GET.get('q')
    list= all_users_data.objects.filter(name = query)
    context = {'data1': user, 'data2': list}
    
    return render(request, 'index.html', {'program_list':context})

from .models import agents

from django.contrib.auth.models import User
@login_required
def users_list(request):
    user = User.objects.all()
    return render(request, 'users_list.html', {'user':user})
    

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from .forms import UserLoginForm

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Перенаправляем пользователя на главную страницу
            return redirect('index')
    return render(request, 'login.html')


from django.contrib.auth import logout
from django.shortcuts import redirect

def my_logout(request):
    logout(request)
    return redirect('login')


