from django.db import models
from django.contrib.auth.models import User
import random
import  psycopg2
from psycopg2 import sql
from itertools import chain


# Функция для генерации ключа
def generate_id(ids):
    while(1):
        id = random.randint(0,32760)
        if id in ids:
            continue
        else:
            break
    return id   

#Table Module класс Настольная игра
class Boardgame(models.Model):
    def getAllBgames(): 
        return BoardgameGateway.getAllBgames() 
    def filterBgames(name,players):
        return BgameFinder.filterBgames(name,players)
    def getBgame(id):
        bgame = BgameFinder.findBgame(id)
        bgame_data = bgame.getBgame()
        return bgame_data
    def updateBgameRateAdd(game_id,rating):
        k = BgameFinder.findUsersRated(game_id)
        a = BgameFinder.findAveRate(game_id)
        new_users_rated = k + 1  
        new_average_rate =round((a*k+ rating)/new_users_rated,1)
        bgame_old = BgameFinder.findBgame(game_id)
        bgame_data = bgame_old.getBgame()
        bgame_new = BoardgameGateway(bgame_data,new_users_rated,new_average_rate) 
        bgame_new.update()
        return 0
    def updateBgameRateUpd(user_id,game_id,rating):
        old_rate = Rate.getUserGameRate(user_id,game_id)
        a = BgameFinder.findAveRate(game_id)
        k = BgameFinder.findUsersRated(game_id)
        new_average_rate = round((a*k - old_rate + rating)/k,1)
        bgame_old = BgameFinder.findBgame(game_id)
        bgame_data = bgame_old.getBgame()
        bgame_new = BoardgameGateway(bgame_data,k,new_average_rate) 
        bgame_new.update()

#Raw Data Gateway Шлюз записи данных для таблицы Board_game
class BoardgameGateway:
    game_id = models.IntegerField(primary_key=True)
    game_name = models.CharField(max_length=100)
    year = models.IntegerField()
    minplayers = models.IntegerField()
    maxplayers = models.IntegerField()
    minage = models.IntegerField()
    users_rated = models.IntegerField()
    average_rate = models.FloatField()
    mechanics = models.TextField()
    domains = models.TextField()
    thumbnail = models.TextField()
    image = models.TextField()
    description= models.TextField()
    minplaytime = models.IntegerField()
    maxplaytime = models.IntegerField()
    URL = models.TextField()
    def __init__(self, a, b=None, c = None):
        if b==None and c == None:    
            self.game_id = a[0]
            self.game_name = a[1]
            self.year = a[2]
            self.minplayers = a[3]
            self.maxplayers = a[4]
            self.minage = a[5]
            self.users_rated = a[6]
            self.average_rate = a[7]
            self.mechanics = a[8]
            self.domains = a[9]
            self.thumbnail = a[10]
            self.image = a[11]
            self.description= a[12]
            self.minplaytime = a[13]
            self.maxplaytime = a[14]
            self.URL = a[15]
        else:
            self.game_id = a[0]
            self.game_name = a[1]
            self.year = a[2]
            self.minplayers = a[3]
            self.maxplayers = a[4]
            self.minage = a[5]
            self.users_rated = b
            self.average_rate =c
            self.mechanics = a[8]
            self.domains = a[9]
            self.thumbnail = a[10]
            self.image = a[11]
            self.description= a[12]
            self.minplaytime = a[13]
            self.maxplaytime = a[14]
            self.URL = a[15]


    def __str__(self):
        return f"{self.game_id} {self.game_name}"
    def getAllBgames():
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM "Board_game"')
        bgames = cursor.fetchall() 
        cursor.close() 
        conn.close() 
        return bgames

    def getBgame(self):
        bgame = [self.game_id, self.game_name,self.year,self.minplayers,self.maxplayers,
        self.minage, self.users_rated, self.average_rate, self.mechanics,self.domains,
        self.thumbnail, self.image, self.description, self.minplaytime,
        self.maxplaytime, self.URL]
        return bgame

    def update(self):
        ur = str(self.users_rated)
        ar = str(self.average_rate)
        g = str(self.game_id)
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'UPDATE "Board_game" SET users_rated='+ur+',average_rate='+ar+' WHERE game_id='+g
        cursor.execute(sqlString)
        conn.commit() 
        cursor.close() 
        conn.close() 
        return 0
#Raw Data Gateway класс для создания новых объектов шлюза BgameGateway
class BgameFinder:
    def findBgame(id):
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        id = str(id)
        sqlString = 'SELECT * FROM "Board_game" WHERE game_id='+ id
        cursor.execute(sqlString)
        bgame_data = cursor.fetchall() 
        cursor.close() 
        conn.close() 
        bg = list(bgame_data[0])
        bgame = BoardgameGateway(bg)
        return bgame
    def findUsersRated(game_id):
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        g = str(game_id)
        sqlString = 'SELECT users_rated FROM "Board_game" WHERE game_id='+ g
        cursor.execute(sqlString)
        bgames = cursor.fetchall() 
        bgame = bgames[0][0]
        cursor.close() 
        conn.close() 
        return bgame
    def findAveRate(game_id):
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        g = str(game_id)
        sqlString = 'SELECT average_rate FROM "Board_game" WHERE game_id='+ g
        cursor.execute(sqlString)
        bgames = cursor.fetchall() 
        bgame = bgames[0][0]
        cursor.close() 
        conn.close() 
        return bgame
    def filterBgames(name,players):
        sqlString = 'SELECT * FROM "Board_game"'
        if name!='' and players =='':
            s = "'%"+name+"%'" 
            sqlString = 'SELECT * FROM "Board_game" WHERE game_name LIKE '+ str(s)
        if name =='' and players !='':
            s = players 
            sqlString = 'SELECT * FROM "Board_game" WHERE minplayers<='+str(s)+' AND maxplayers>='+str(s)
        if name !='' and players !='':
            i = "'%"+name+"%'" 
            s = players 
            sqlString = 'SELECT * FROM "Board_game" WHERE minplayers<='+str(s)+' AND maxplayers>='+str(s)+'AND game_name LIKE '+ str(i)
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        cursor.execute(sqlString)
        bgames = cursor.fetchall() 
        cursor.close() 
        conn.close() 
        return bgames

#Table Module класс Оценка
class Rate(models.Model):
    def getUserGameRate(user_id,game_id):
        return RateFinder.getUserGameRate(user_id,game_id)
    def addRate(user_id,game_id,rating):
        review_id = RateFinder.findFreeRateId()
        rate = RateGateway(review_id,user_id,game_id,rating)
        rate.insert()
        return 0
    def updateRate(user_id, game_id, rating):
        review = RateFinder.findReview(user_id,game_id)
        rate = RateGateway(review,rating)
        rate.update()
        return 0
        
#Raw Data Gateway Шлюз записи данных для таблицы Rate
class RateGateway():
    review_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="user")
    game = models.ForeignKey(Boardgame, on_delete=models.CASCADE, related_name ="game")
    rating = models.FloatField()
    def __init__(self,a,b,c=None,d=None):
        if c == None and d ==None:
            self.review_id = a[0]
            self.user = a[1]
            self.game = a[2]
            self.rating = b
        else:
            self.review_id = a
            self.user = b
            self.game = c
            self.rating = d 
    def insert(self):
        re = str(self.review_id)
        u = str(self.user)
        g = str(self.game)
        ra = str(self.rating)
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'INSERT INTO "Rate" VALUES ('+re+','+u+','+g+','+ra+')'
        cursor.execute(sqlString)
        conn.commit() 
        cursor.close() 
        conn.close() 
        return 0
    def update(self):
        re = str(self.review_id)
        ra = str(self.rating)
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'UPDATE "Rate" SET rating='+ra+' WHERE review_id='+re
        cursor.execute(sqlString)
        conn.commit() 
        cursor.close() 
        conn.close() 
        return 0
#Raw Data Gateway класс для создания новых объектов шлюза RateGateway   
class RateFinder():
    def getUserGameRate(user_id,game_id):
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        if user_id:
            u = str(user_id)
            g = str(game_id)
            sqlString = 'SELECT "Rate".rating FROM "Rate" JOIN "auth_user" ON "Rate".user_id ="auth_user".id JOIN "Board_game" ON "Rate".game_id = "Board_game".game_id WHERE "auth_user".id ='+u+' AND "Board_game".game_id ='+g
            cursor.execute(sqlString)
            rate = cursor.fetchall() 
            if rate:
                r = rate[0][0]
            else: 
                r = ''
            cursor.close() 
            conn.close() 
        else:
            r = ''
        return r
    def findFreeRateId():
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'SELECT review_id FROM "Rate"'
        cursor.execute(sqlString)
        rated = cursor.fetchall()
        rates = list(chain.from_iterable(rated))
        cursor.close() 
        conn.close() 
        review_id  = generate_id(rates)
        return review_id
    def findReview(user_id,game_id):
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        u = str(user_id)
        g = str(game_id)
        sqlString = 'SELECT "Rate".* FROM "Rate" JOIN "auth_user" ON "Rate".user_id ="auth_user".id JOIN "Board_game" ON "Rate".game_id = "Board_game".game_id WHERE "Rate".user_id ='+u+' AND "Rate".game_id='+g
        cursor.execute(sqlString)
        rated = cursor.fetchall() 
        rate = list(rated[0])
        cursor.close() 
        conn.close()
        return rate
   
#Table Module класс Избранное
class Favoured(models.Model):
    def getUserFavoured(user_id):
        return FavouredFinder.getUserFavoured(user_id)
    def addFavBgame(user_id, game_id):
        new_fav = FavouredGateway(FavouredFinder.findFreeFavId(),user_id, game_id)
        new_fav.insert()
        return 0
    def getFavGameIds(user_id):
        return FavouredFinder.getFavGameIds(user_id)
    def deleteFromFav(user_id,game_id):
        fav_id = FavouredFinder.findFavId(user_id,game_id)
        fav = FavouredGateway(fav_id,user_id,game_id)
        fav.delete()
        return 0

#Raw Data Gateway Шлюз записи данных для таблицы Favoured
class FavouredGateway():
    fav_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="user")
    game = models.ForeignKey(Boardgame, on_delete=models.CASCADE, related_name ="game")
    def __init__(self, a,b,c):
        self.fav_id = a
        self.user = b
        self.game = c
    def insert(self):
        f = str(self.fav_id)
        u = str(self.user)
        g = str(self.game)
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'INSERT INTO "Favoured" VALUES ('+f+','+u+','+g+')'
        cursor.execute(sqlString)
        conn.commit() 
        cursor.close() 
        conn.close() 
        return 0
    def delete(self):
        f = str(self.fav_id)
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'DELETE FROM "Favoured" WHERE fav_id='+f
        cursor.execute(sqlString)
        conn.commit() 
        cursor.close() 
        conn.close() 
        return 0

#Raw Data Gateway класс для создания новых объектов шлюза FavouredGateway
class FavouredFinder():
    def getUserFavoured(user_id):
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        u = str(user_id)
        sqlString = 'SELECT "Board_game".game_id,"Board_game".game_name, "Board_game".minplayers,"Board_game".maxplayers, "Board_game".minage,"Board_game".average_rate,"Board_game".thumbnail FROM "Favoured" JOIN "auth_user" ON "Favoured".user_id ="auth_user".id JOIN "Board_game" ON "Favoured".game_id = "Board_game".game_id WHERE "auth_user".id ='+u
        cursor.execute(sqlString)
        favoured = cursor.fetchall()
        cursor.close() 
        conn.close() 
        return favoured
    def getFavGameIds(user_id):
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor()
        if user_id:
            u = str(user_id)
            sqlString = 'SELECT "Favoured".game_id FROM "Favoured" JOIN "auth_user" ON "Favoured".user_id ="auth_user".id JOIN "Board_game" ON "Favoured".game_id = "Board_game".game_id WHERE "Favoured".user_id ='+u
            cursor.execute(sqlString)
            favoured = cursor.fetchall()
            fav = list(chain.from_iterable(favoured))
            cursor.close() 
            conn.close()
        else:
            fav = ''
        return fav
    def findFreeFavId():
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'SELECT fav_id FROM "Favoured"'
        cursor.execute(sqlString)
        favoured = cursor.fetchall()
        fav = list(chain.from_iterable(favoured))
        cursor.close() 
        conn.close() 
        fav_id  = generate_id(fav)
        return fav_id
    def findFavId(user_id,game_id):
        conn = psycopg2.connect( host='localhost', user='postgres', password='Traumelc22', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        u = str(user_id)
        g = str(game_id)
        sqlString = 'SELECT "Favoured".fav_id FROM "Favoured" JOIN "auth_user" ON "Favoured".user_id ="auth_user".id JOIN "Board_game" ON "Favoured".game_id = "Board_game".game_id WHERE "Favoured".user_id ='+u+' AND "Favoured".game_id='+g
        cursor.execute(sqlString)
        favoured = cursor.fetchall() 
        fav = favoured[0][0]
        cursor.close() 
        conn.close()
        return fav
