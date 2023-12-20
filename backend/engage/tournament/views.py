from django.db.models import F, Prefetch
from django.shortcuts import render, redirect
from django.utils import timezone
from datetime import  timedelta
from engage.account.constants import SubscriptionPlan
from engage.tournament.models import Tournament, TournamentParticipant, TournamentPrize
from base64 import b64decode
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding
from django.contrib.auth import get_user_model, login
from engage.account.api import do_register
from engage.account.constants import SubscriptionPlan

UserModel = get_user_model()

def decrypt_msisdn(key, encrypted_msisdn):
    key = b64decode(key)
    
    # Reverse the replacements in the encrypted MSISDN
    encrypted_msisdn = encrypted_msisdn.replace("dsslsshd", "/").replace("dsplussd", "+")
    
    # Decode the base64-encoded encrypted MSISDN
    iv_and_ciphertext = b64decode(encrypted_msisdn.encode('utf-8'))
    
    # Split IV and ciphertext
    iv = iv_and_ciphertext[:16]
    ciphertext = iv_and_ciphertext[16:]
    
    # Initialize the decryption cipher
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    decryptor = cipher.decryptor()
    
    # Decrypt and unpad the data
    decrypted_data = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()
    unpadded_data = unpadder.update(decrypted_data) + unpadder.finalize()
    
    # Decode the UTF-8 data to get the original MSISDN
    msisdn = unpadded_data.decode('utf-8')
    
    return msisdn

def attempt_login_register(request):
    if 'msisdn' not in request.session or request.user.is_authenticated:
      print("inside first if")
      return
    try:
        mobilen = request.session['msisdn']
        request.user = mobilen
        user = UserModel.objects.filter(
            mobile__iexact=mobilen,
            region=request.region,
            
        ).first()
        if user:
            # user found attempt direct login
            usermob = str(user.mobile)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            
        else:
            # user not found attempt registration
            usermob = mobilen
            do_register(None, request, usermob, SubscriptionPlan.FREE)
    
    except UserModel.DoesNotExist:
        usermob = mobilen
        do_register(None, request, usermob, SubscriptionPlan.FREE)

def tournament_view(request, slug):
    user = request.user

    now = timezone.now()

    key = "Zjg0ZGJhYmI1MzJjNTEwMTNhZjIwYWE2N2QwZmQ1MzU="  # Replace with your encryption key
    encrypted_msisdn = request.GET.get('app', '')  # Replace with the encrypted MSISDN

    if encrypted_msisdn:
        decrypted_msisdn = decrypt_msisdn(key, encrypted_msisdn)
        if decrypted_msisdn.startswith('0'):
            without_0 = decrypted_msisdn[1:]
            decrypted_msisdn = '234' + without_0
        print("^^^Decrypted msisdn", decrypted_msisdn)
    
        request.session['msisdn'] = decrypted_msisdn
        attempt_login_register(request)
    else:
      print("CHC-request.user not found")

    try:
        tournament = Tournament.objects.select_related(
            'game',
        ).prefetch_related(
            'tournamentparticipant_set',
            Prefetch(
                'tournamentprize_set',
                queryset=TournamentPrize.objects.order_by('position')
            ),
        ).annotate(
            starts_in=F('start_date') - now
        ).get(
            slug=slug,
            regions__in=[request.region]
        )
    except Tournament.DoesNotExist:
        #if slug has been changed get by id

        try:
            tournament = Tournament.objects.select_related(
                'game',
            ).prefetch_related(
                'tournamentparticipant_set',
                Prefetch(
                    'tournamentprize_set',
                    queryset=TournamentPrize.objects.order_by('position')
                ),
            ).annotate(
                starts_in=F('start_date') - now
            ).get(
                id=slug,
                regions__in=[request.region]
            )
        except Tournament.DoesNotExist:
            #if slug has been changed get by id
            return redirect('/')

    participant = None
    if user.is_authenticated:
        participant = tournament.get_participant(user)

    can_join = True
    if user.is_authenticated and user.subscription == SubscriptionPlan.PAID1:
        can_join = not TournamentParticipant.objects.filter(
            tournament__regions__in=[request.region],
            participant=user,
            created__date=now.date()
        ).exists()
    if user.is_authenticated :
        game_account = tournament.game.usergamelinkedaccount_set.filter(user=user).last()
    else :
        game_account = tournament.game.usergamelinkedaccount_set.last()   
    
    now = timezone.now()
    starts_in = tournament.start_date - now
    if starts_in.days :
        starts_in_full = f'{starts_in.days} days, {int(starts_in.seconds // 3600)} hours and {int((starts_in.seconds // 60) % 60)} minutes'
    else:
        starts_in_full = f'{int(starts_in.seconds // 3600)} hours and {int((starts_in.seconds // 60) % 60)} minutes'
    
    tournament_started = tournament.start_date
    if tournament.time_compared_to_gmt and '+' in tournament.time_compared_to_gmt :
        tournament_started = tournament.start_date + timedelta(hours=int(tournament.time_compared_to_gmt))
    if tournament.time_compared_to_gmt and '-' in tournament.time_compared_to_gmt :
        tournament_started = tournament.start_date - timedelta(hours=int(tournament.time_compared_to_gmt))


    return render(request, 'tournament.html', {'tournament': tournament,
                                               'user': user,
                                               'starts_in_full': starts_in_full,
                                               'game_account': game_account,
                                               'tournament_started': tournament_started,
                                               'participant': participant,
                                               'can_join': can_join,
                                               'currentDate':now})
