from django.shortcuts import render
from bgames.models import Boardgame, Favoured, Rate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


def BgamesList(request): 
    bgames = Boardgame.getAllBgames() 
    return render(request,'index.html',{'bgdata':bgames})


def Search(request):
    results = ''
    if request.method == "GET":
        name = request.GET.get('search')
        players = request.GET.get('players')
        if players !=None:
            if players.isdigit() or players =='':
                results = Boardgame.filterBgames(name,players)
            else:
                results = ''
    return render(request, 'search.html', {'results': results})


def Detail(request, id):
    current_user = request.user
    result = Boardgame.getBgame(id)
    fav = Favoured.getFavGameIds(current_user.id)
    if fav:
        if id in fav:
            b = True
        else: 
            b = False
    else:
        b = False
    rate = Rate.getUserGameRate(current_user.id,id)
    return render(request, 'detail.html',{'one_bgdata':result, 'b':b,'rate':rate})

def ShowFavoured(request):
    current_user = request.user
    favoured = Favoured.getUserFavoured(current_user.id)
    return render(request, 'personal.html', {'fav': favoured,'userdata':current_user})

def AddDelFavoured(request,id):
    current_user = request.user
    fav_list = Favoured.getFavGameIds(current_user.id)
    if request.method == 'POST':
        if id in fav_list:
            Favoured.deleteFromFav(current_user.id,id)
        else:
            Favoured.addFavBgame(current_user.id,id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def AddUpdRate(request,id):
    current_user = request.user
    rate = Rate.getUserGameRate(current_user.id,id)
    if request.method == 'POST':
        selected_option = float(request.POST['rates'])
        if selected_option:
            if rate:
                Boardgame.updateBgameRateUpd(current_user.id,id,rate,selected_option)
                Rate.updateRate(current_user.id,id,selected_option)
            else:
                Rate.addRate(current_user.id,id,selected_option)
                Boardgame.updateBgameRateAdd(id,selected_option)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SignUpView(generic.CreateView):    
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
