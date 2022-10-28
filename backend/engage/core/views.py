from django.db.models import F, Q,Prefetch
from django.http import HttpResponse, Http404,HttpResponseForbidden
from django.shortcuts import render, redirect
from django.utils import timezone
from engage.account.models import User
from engage.tournament.models import Tournament,TournamentPrize
from django.contrib.auth import login

from engage.core.models import HTML5Game, Event, FeaturedGame, Game
from engage.core.constants import NotificationTemplate
from engage.operator.models import OperatorAd
from engage.services import notify_when


@notify_when(events=[
    NotificationTemplate.HOME,
    NotificationTemplate.HOW_TO_USE
])
def home_view(request):
    now = timezone.now()

    featured_games = FeaturedGame.objects.all()
    games = Game.objects.all()
    ad = OperatorAd.objects.filter(
        (Q(start_date__gte=now) & Q(end_date__lte=now)) |
        (Q(start_date__isnull=True) & Q(end_date__isnull=True)),
        regions__in=[request.region]
    ).order_by('?').first()
    events = Event.objects.filter(
        regions__in=[request.region]
    ).all().order_by('?')[:20]

    previous_tournaments = Tournament.objects.select_related('game').prefetch_related(
        'tournamentparticipant_set',
        Prefetch(
            'tournamentprize_set',
            queryset=TournamentPrize.objects.order_by('position')
        )
    ).filter(regions__in=[request.region],end_date__lt=now).order_by('name')
    if 'user_id' in request.session:
        user_id = True
    else:
        user_id = False
    return render(request, 'index.html', {'featured_games': featured_games,
                                          'games': games,
                                          'ad': ad,
                                          'events': events,
                                          'previous_tournaments':previous_tournaments,
                                          'user_id': user_id})


    
def about_view(request):
    if  request.user.is_staff or request.user.is_superuser :
        return redirect('/auth/logout/')  
    return render(request, 'about.html', {})


## TODO: to handle header enrichment here
def register_view(request):
    if request.user and request.user.is_authenticated or ('user_id' in request.session and 'renewing' not in request.session):
       return redirect('/')
    else :
       # print(request.headers)
       refid = request.GET.get('referrer')
       print(refid)
       return render(request, 'register.html', {'wifi':True, 'refid':refid})

def waiting_view(request):
    # print('user_id' in request.session)
    if not 'user_id' in request.session:
        return redirect('/')
    elif (request.user and request.user.is_active):
        userid = request.session.pop('user_id', None)
        return redirect('/')
    else :
        # print(request.headers)
        # print("user", request.user)
        user = User.objects.get(pk=request.session['user_id'])
        return render(request, 'wait.html', {'wifi':True, 'user':user})

def clear_session_view(request):
    if 'user_id' in request.session:
        userid = request.session.pop('user_id', None)
        
        if 'subscribed' in request.session:
            subscribed = request.session.pop('subscribed', None)
            print("subscribed =", subscribed)
            if subscribed==1:
                subscription = 'free'
            elif subscribed==2:
                subscription = 'paid1'
            elif subscribed==3:
                subscription = 'paid2'
            print('successfully subscribed!')
            user = User.objects.get(pk=userid)
            user.is_active=True
            user.subscription=subscription
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    return redirect('/')

def new_register_view(request):
    if request.user and request.user.is_authenticated or ('user_id' in request.session and 'renewing' not in request.session):
        return redirect('/')
    else :
        refid = request.GET.get('referrer')
        return render(request, 'register1.html', {'refid':refid})


def header_view(request):
    strr = "<html>"
    for k in request.headers:
        strr += str(k) + ': '+ str(request.headers[k])
        strr += "<br>"
    strr += "</html>"
    return HttpResponse(strr)

def faq_view(request):
    return render(request, 'FAQ.html', {})


def terms_view(request):
    return render(request, 'terms.html', {})


def privacy_view(request):
    return render(request, 'privacy.html', {})


def disclaimer_view(request):
    return render(request, 'disclaimer.html', {})


def html5_game_view(request, game):
    try:
        html5_game = HTML5Game.objects.filter(
            regions__in=[request.region]
        ).get(slug__iexact=game)
    except HTML5Game.DoesNotExist:
        raise Http404

    return redirect(f'/html5_game/{html5_game.slug}/')


def firebase_sw_view(request):
    return HttpResponse("""
        importScripts('https://www.gstatic.com/firebasejs/9.1.1/firebase-app-compat.js');
        importScripts('https://www.gstatic.com/firebasejs/9.1.1/firebase-messaging-compat.js');

        firebase.initializeApp({
            apiKey: "AIzaSyA0HHeMbJieI4Qp5tyxn765mk0IWllTCco",
            authDomain: "engageplaywin-ced7f.firebaseapp.com",
            projectId: "engageplaywin-ced7f",
            storageBucket: "engageplaywin-ced7f.appspot.com",
            messagingSenderId: "615474016768",
            appId: "1:615474016768:web:7cfa190a078416cc3a9ee5",
            measurementId: "G-4FTX1VRLYN"
        });

        const messaging = firebase.messaging();
       
    """, status=200, content_type='application/javascript')


def view_404(request, exception=None): 
    return redirect('/')

def view_403(request, exception=None): 
    return redirect('/admin')

# def error_403(request, exception):
#         return render(request,'403.html') 