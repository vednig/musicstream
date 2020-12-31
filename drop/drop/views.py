from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import logout

import json
import billboard
from youtubesearchpython import SearchVideos
import redis
pool = redis.ConnectionPool(host='redis-19587.c114.us-east-1-4.ec2.cloud.redislabs.com', port=19587,password="6VICM85ERMMneJxAB8AUjFzEU7uRNX1d",db=0)
r = redis.Redis(connection_pool=pool)
import ast 
def land(request):
    
    if not request.user.is_authenticated:
        return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))
    # ...
                                            
    #user = authenticate(request,username='john', password='SECRET')
    if request.user is not None:
        chart = billboard.ChartData('hot-100')
        print('Welcome',chart[0])
        top50=[]
        populate=''
        final='<div class="know">'
        ''''
        for i in range(chart.entries.__len__()):
            top_song=chart[i]
            search = SearchVideos(top_song, offset = 1, mode = "json", max_results = 1)
            var = json.loads(search.result())
            x=var['search_result'][0]['thumbnails'][0]
            top50.append(x)
        #login(request, user)
        #populate=
        
        #request.user.populate=top50
        populate=top50
        r.set('content',str(populate))'''
        #populate=request.user.populate
        populate=r.get('content').decode()
        res =ast.literal_eval(populate)
        for i in range(len(res)):
            if i%1==0:
                print('fon')
                final+='</div>'
                final+='<div class="know">'
                final+='<div class="cont" >'
                final+="<img src='"+res[i]+"' id="+str(i)+" onclick=playthis(event)>"
                final+="<p class='bold-text'id='text"+str(i)+"' >"+str(chart[i])+"</p>"
                final+='</div>'
                
            else:
                print('x')
            #final+='<div class="row">'
                final+='<div class="cont">'
                final+="<img src='"+res[i]+"' id="+str(i)+"onclick=playthis(event) >"
                final+="<p class='bold-text' id='text"+str(i)+"' >"+str(chart[i])+"</p>"
                final+='</div>'
            #final+='</div>'
        final+='</div>'
    else:
        populate="no html"
    #populate="All the recommended html"
    about="you're from:::\n"+request.headers['User-Agent'] + "\n:::"
    pool.disconnect()
    return render(request,"index.html",{'section':'We"re Official','some_list':[24,86,97,96],'populate':final,'list':chart})
    
def contaddr(request):
    if request.method == 'GET':
        x=str(request.GET['query'])
        ret=r.get(x)
        return HttpResponse(ret)
def createuser(request):
    username = request.GET['username']
    password = request.GET['password']
    firstname= request.GET['firstname']
    email= request.GET['email']
    lastname=request.GET['lastname']
    user = User.objects.create_user(firstname, email, password)
    user.last_name = lastname
    user.save()
    return HttpResponse('Created')

def signup(request):
    return render(request,"registration/register.html")
    

def logout_view(request):
    logout(request)
    return render(request,"index.html")