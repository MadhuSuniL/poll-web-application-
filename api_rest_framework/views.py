from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from users.models import UserDetails
from poll_app.models import Poll
from .serializers import *
# Create your views here.

class LoginApi(GenericAPIView):
    serializer_class = loginSerializer
    queryset = User.objects.all()
    
    def post(self,request):
        username = request.data.get('un')
        password = request.data.get('ps')
    
        user = authenticate(username=username,password=password)
        if user is None:
            return Response('User not Found',404)
        request.session['user'] = user.username
        return Response('Login successful!',200)
    

class RegisterApi(GenericAPIView):
    serializer_class = RegisterSerializer
    queryset = User.objects.all()
    
    def post(self,request):
        username = request.data.get('un')
        email = request.data.get('email')
        no = request.data.get('no')
        password = request.data.get('ps')
        
        user = User.objects.create_user(username=username,email=email,password=password)
        details = UserDetails.objects.create(user=user,ph_no=no)
        return Response('Registration successful!',200)
    
    
    
class PollApi(GenericAPIView):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    
    def get(self,request):
        data = self.serializer_class(data=self.queryset,many=True)
        return Response(data.data)
    
    def post(self,request):
        question = request.data.get('question')
        opt1 = request.data.get('opt1')
        opt2 = request.data.get('opt2')
        opt3 = request.data.get('opt3')
        opt4 = request.data.get('opt4')
        
        user = User.objects.get(username=request.session['user'])
        if Poll.objects.filter(user=user).count() < 5:
            poll = Poll.objects.create(user=user,question=question,option_1=opt1,option_2=opt2,option_3=opt3,option_4=opt4)
            return Response('Created....!',201)
        return Response('Max polls reached..!')
    
    
    
class PollDetails(GenericAPIView):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    
    def get(self,request,id):
        poll = Poll.objects.get(id=int(id))
        data = self.serializer_class(poll)
        return Response(data.data)
    
    def put(self,request,id):
        id = int(id)
        poll = Poll.objects.get(id=id)
        if int(ans) == 1:
            poll.option_1_votes += 1
        elif int(ans) == 2:
            poll.option_2_votes += 1
        elif int(ans) == 3:
            poll.option_3_votes += 1
        elif int(ans) == 4:
            poll.option_4_votes += 1
        poll.save()
        
        from math import floor
        def percent(val1,val2):
            return floor((val1/val2)*100)    
        poll = {
            'id':poll.id,
            'question':poll.question,
            'option_1':poll.option_1,
            'option_2':poll.option_2,
            'option_3':poll.option_3,
            'option_4':poll.option_4,
            'option_1_votes':percent(poll.option_1_votes,poll.option_1_votes+poll.option_2_votes+poll.option_3_votes+poll.option_4_votes),
            'option_2_votes':percent(poll.option_2_votes,poll.option_1_votes+poll.option_2_votes+poll.option_3_votes+poll.option_4_votes),
            'option_3_votes':percent(poll.option_3_votes,poll.option_1_votes+poll.option_2_votes+poll.option_3_votes+poll.option_4_votes),
            'option_4_votes':percent(poll.option_4_votes,poll.option_1_votes+poll.option_2_votes+poll.option_3_votes+poll.option_4_votes),
        }
        return Response(poll)
        
    def delete(self,request,id):    
        poll = Poll.objects.get(id=int(id))
        poll.delete()
        return Response(None,200)
    
from datetime import datetime,timedelta
    
class Delete24Api(GenericAPIView):
    serializer_class = PollSerializer
    queryset = Poll.objects.all()
    
    def delete(self,request):
        user = User.objects.get(username=request.session['user'])
        now = datetime.now()
        time = now - timedelta(hours=24)
        polls = Poll.objects.filter(user=user,date__lt= time)
        polls.delete()
        return Response(None,200)
