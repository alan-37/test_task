from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Q
from .models import Ad, ExchangeProposal
from .forms import AdForm, SignUpForm, LoginForm
from django.contrib.auth import login, authenticate
from django.contrib.auth import logout
from django.core.exceptions import PermissionDenied


def ads_list(request):
    query = request.GET.get('q', '')
    category = request.GET.get('category')
    condition = request.GET.get('condition')

    ads = Ad.objects.filter(available=True)

    if query:
        ads = ads.filter(Q(title__icontains=query) | Q(description__icontains=query))
    if category:
        ads = ads.filter(category=category)
    if condition:
        ads = ads.filter(condition=condition)
    categories = Ad.objects.values_list('category', flat=True).distinct()

    return render(request, 'ads/list_ads.html', {'query': query,
                                                'current_category': category,
                                                'current_condition': condition,
                                                'categories': categories,
                                                 'ads': ads,})


def ads_detail(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    return render(request, 'ads/ads_detail.html', {'ad': ad})


@login_required
def profile_view(request):
    user_ads = Ad.objects.filter(user=request.user)
    incoming_proposals = ExchangeProposal.objects.filter(ad_receiver__user=request.user)
    outgoing_proposals = ExchangeProposal.objects.filter(ad_sender__user=request.user)
    return render(request, 'ads/profile.html', {
        'user': request.user,
        'user_ads': user_ads,
        'incoming_proposals': incoming_proposals,
        'outgoing_proposals': outgoing_proposals,
    })

@login_required
def accept_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, ad_receiver__user=request.user)
    proposal.status = 'accepted'
    proposal.save()
    return redirect('profile')

@login_required
def reject_proposal(request, proposal_id):
    proposal = get_object_or_404(ExchangeProposal, id=proposal_id, ad_receiver__user=request.user)
    proposal.status = 'rejected'
    proposal.save()
    return redirect('profile')


@login_required
def send_proposal(request, ad_receiver_id):
    receiver_ad = get_object_or_404(Ad, id=ad_receiver_id)
    user_ads = Ad.objects.filter(user=request.user)
    if receiver_ad.user == request.user:
        return render(request, 'ads/send_proposal.html', {
            'error': 'Нельзя предлагать обмен на своё же объявление.',
            'receiver_ad': receiver_ad,
            'user_ads': user_ads,
        })
    if not user_ads.exists():
        return render(request, 'ads/send_proposal.html', {
            'error': 'У вас нет объявлений для обмена.',
            'receiver_ad': receiver_ad,
        })

    if request.method == "POST":
        sender_id = request.POST.get('ad_sender')
        comment = request.POST.get('comment', '')
        try:
            sender_ad = Ad.objects.get(id=sender_id, user=request.user)
            ExchangeProposal.objects.create(
                ad_sender=sender_ad,
                ad_receiver=receiver_ad,
                comment=comment,
                status='pending'
            )
            return redirect('ads_list')
        except Ad.DoesNotExist:
            return render(request, 'ads/error.html', {'message': 'Объявление не найдено.'})

    return render(request, 'ads/send_proposal.html', {'user_ads': user_ads,
                                                      'receiver_ad': receiver_ad, })


@login_required
def create_ad(request):
    if request.method == "POST":
        form = AdForm(request.POST, request.FILES)
        if form.is_valid():
            ad = form.save(commit=False)
            ad.user = request.user
            ad.save()
            return render(request, 'ads/create_ad_true.html', {'form': form,
                                                               'order': ad, })
    else:
        form = AdForm()
    return render(request, 'ads/create_ad.html', {'form': form})


@login_required
def edit_ad(request, pk):
    ad = get_object_or_404(Ad, pk=pk)
    if request.user != ad.user:
        raise PermissionDenied("Вы не можете редактировать это объявление.")

    if request.method == "POST":
        form = AdForm(request.POST, request.FILES, instance=ad)
        if form.is_valid():
            form.save()
            return redirect('ads_detail', pk=ad.pk)
    else:
        form = AdForm(instance=ad)
    return render(request, 'ads/edit_ad.html', {'form': form, 'order': ad})


@login_required
def delete_ad(request, pk):
    ad = get_object_or_404(Ad, id=pk)
    if request.user != ad.user:
        raise PermissionDenied("Вы не можете удалить это объявление.")
    ad.delete()
    return redirect('ads_list')


def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('ads_list')
    else:
        form = SignUpForm()
    return render(request, 'ads/signup.html', {'form': form})


def login_view(request):
    form = LoginForm(data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('ads_list')
    return render(request, 'ads/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('ads_list')