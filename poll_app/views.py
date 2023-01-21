from math import floor
from django.shortcuts import render,redirect
from django.http import JsonResponse,HttpResponse
from .models import Poll
from django.contrib.auth.models import User
from users.models import UserDetails
# Create your views here.

def home_page(request):
    all = Poll.objects.all()
    all_list = []
    for i in all:
        data = {
            'id':i.id,
            'question':i.question,
            'user':i.user.username
        }
        all_list.append(data)
    context = {
            'current_user':request.session['user'],
        'polls':all_list
    }
        
    return render(request, 'home.html',context=context)


def profile_page(request):
    
    def percent(val1,val2):
        try:
            return floor((val1/val2)*100)
        except:
            return 0
    user = User.objects.get(username=request.session['user'])
    polls = Poll.objects.filter(user=user)
    ph_no = UserDetails.objects.get(user=user).ph_no
    all = []
    for poll in polls:
        data = {
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
        all.append(data)
    context = {
        'current_user':request.session['user'],
        'ph_no':ph_no,
        'email':user.email,
        'polls':all
    }
    return render(request, 'profile.html',context)


def create_poll(request):
    question = request.GET.get('question')
    op1 = request.GET.get('opt1')
    opt2 = request.GET.get('opt2')
    opt3 = request.GET.get('opt3')
    opt4 = request.GET.get('opt4')
    
    user = User.objects.get(username=request.session['user'])
    if Poll.objects.filter(user=user).count() < 5:
        poll = Poll.objects.create(user=user,question=question,option_1=op1,option_2=opt2,option_3=opt3,option_4=opt4)
        return JsonResponse({'msg':'Done'})
        
    else:
        return JsonResponse({'msg':'Max'})
    
def get_poll(request,id=None):
    id = int(id)
    poll = Poll.objects.get(id=id)
    poll = {
        'question':poll.question,
        'option_1':poll.option_1,
        'option_2':poll.option_2,
        'option_3':poll.option_3,
        'option_4':poll.option_4,
        'option_1_votes':poll.option_1_votes,
        'option_2_votes':poll.option_2_votes,
        'option_3_votes':poll.option_3_votes,
        'option_4_votes':poll.option_4_votes,
        'total_votes':poll.option_1_votes+poll.option_2_votes+poll.option_3_votes+poll.option_4_votes        
    }
    return JsonResponse({"poll":poll})
    
def handle_ans(request,id,ans):
    # ans = request.GET('ans')
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
        
    print(poll.option_1_votes)
    print(poll.option_2_votes)
    print(poll.option_3_votes)
    print(poll.option_4_votes)
        
    poll = {
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
    return JsonResponse(poll)
    
    
def del_pol(request,id):
    poll = Poll.objects.get(id=int(id))
    poll.delete()
    return redirect('/poll/profile')


from datetime import datetime,timedelta
def del_24hrs_poll(request):
    user = User.objects.get(username=request.session['user'])
    now = datetime.now()
    time = now - timedelta(hours=24)
    polls = Poll.objects.filter(user=user,date__lt= time)
    polls.delete()
    return redirect('/poll/profile')
