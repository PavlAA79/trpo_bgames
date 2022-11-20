from django.shortcuts import render
from bgames.models import Boardgame, Favoured, Rate
from django.http import HttpResponseRedirect
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import generic


def BgamesList(request): 
    bgames_table = Boardgame()
    bgames = bgames_table.getAllBgames() 
    return render(request,'index.html',{'bgdata':bgames})


def Search(request):
    results = ''
    if request.method == "GET":
        name = request.GET.get('search')
        players = request.GET.get('players')
        b = Boardgame()
        if players !=None:
            if players.isdigit() or players =='':
                results = b.filterBgames(name,players)
            else:
                results = ''
    return render(request, 'search.html', {'results': results})


def Detail(request, id):
    current_user = request.user
    b = Boardgame()
    result = b.getBgame(id)
    f = Favoured()
    fav = f.getFavGameIds(current_user.id)
    if fav:
        if id in fav:
            b = True
        else: 
            b = False
    else:
        b = False
    r = Rate()
    rate = r.getUserGameRate(current_user.id,id)
    return render(request, 'detail.html',{'one_bgdata':result, 'b':b,'rate':rate})

def ShowFavoured(request):
    current_user = request.user
    f = Favoured()
    b = Boardgame()
    fav_list = f.getFavGameIds(current_user.id)
    favoured = b.getUserFavGames(fav_list)
    return render(request, 'personal.html', {'fav': favoured,'userdata':current_user})

def AddDelFavoured(request,id):
    current_user = request.user
    f = Favoured()
    fav_list = f.getFavGameIds(current_user.id)
    if request.method == 'POST':
        if id in fav_list:
            f.deleteFromFav(current_user.id,id)
        else:
            f.addFavBgame(current_user.id,id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

def AddUpdRate(request,id):
    current_user = request.user
    r = Rate()
    rate = r.getUserGameRate(current_user.id,id)
    b = Boardgame()
    if request.method == 'POST':
        selected_option = float(request.POST['rates'])
        if selected_option:
            if rate:
                b.updateBgameRateUpd(id,rate,selected_option)
                r.updateRate(current_user.id,id,selected_option)
            else:
                r.addRate(current_user.id,id,selected_option)
                b.updateBgameRateAdd(id,selected_option)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class SignUpView(generic.CreateView):    
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'signup.html'
