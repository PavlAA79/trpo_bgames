from django.db import models
from django.contrib.auth.models import User
import random
import  psycopg2

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
    bgames_table = []
    def __init__(self):
        self.bgames_table = BgameFinder.getAllBgames()
    def __str__(self):
        st = ''
        for i in range(len(self.bgames_table)):
            st = st + str(self.bgames_table[i])
        return st
    def findBgame(self,game_id):
        bgames = self.bgames_table
        for bg in bgames:
            if bg.getGameId() == game_id:
                found_bgame = bg
        return found_bgame
    def getAllBgames(self):
        bgames = BgameFinder.getAllBgames()
        bgames_list = []
        for bg in bgames:
            bgames_list.append(bg.getBgame())
        bgames_list.sort(key=lambda b: b[1])
        return bgames_list
    def filterBgames(self,name,players):
        if players != '':
            players = int(players)
        bgames = self.bgames_table
        result = []
        if name != '' and players != '':
            for bg in bgames:
                if (name in bg.getName()) and (bg.getMinPlayers()<=players and bg.getMaxPlayers()>=players):
                    result.append(bg.getBgame())
        if name != '' and players == '':
            for bg in bgames:
                if (name in bg.getName()):
                    result.append(bg.getBgame())
        if name == '' and players != '':
            for bg in bgames:
                if (bg.getMinPlayers()<=players and bg.getMaxPlayers()>=players):
                    result.append(bg.getBgame())
        result.sort(key=lambda r: r[1])
        return result
    def getBgame(self,game_id):
        bg = self.findBgame(game_id)
        found_bgame = bg.getBgame()
        return found_bgame
    def getUserFavGames(self,fav_list):
        bg_table = self.bgames_table
        user_fav = []
        for bg in bg_table:
            if bg.getGameId() in fav_list:
                user_fav.append(bg.getBgame())
        user_fav.sort(key=lambda u: u[1])
        return user_fav
    def updateBgameRateAdd(self,game_id,rating):
        bgame_old = self.findBgame(game_id)
        k = bgame_old.getUsersRated()
        a = bgame_old.getAveRate()
        new_users_rated = k + 1  
        new_average_rate =round((a*k+ rating)/new_users_rated,1)
        bgame_old.setAveRate(new_average_rate)
        bgame_old.setUsersRated(new_users_rated)
        bgame_old.update()
        return 0
    def updateBgameRateUpd(self,game_id,old_rate,rating):
        bgame_old = self.findBgame(game_id)
        a = bgame_old.getAveRate()
        k = bgame_old.getUsersRated()
        new_average_rate = round((a*k - old_rate + rating)/k,1)
        bgame_old.setAveRate(new_average_rate)
        bgame_old.update()

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
    def __init__(self, a):   
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
    def __str__(self):
        return f"{self.game_id} {self.game_name}"
    def getBgame(self):
        bgame = [self.game_id, self.game_name,self.year,self.minplayers,self.maxplayers,
        self.minage, self.users_rated, self.average_rate, self.mechanics,self.domains,
        self.thumbnail, self.image, self.description, self.minplaytime,
        self.maxplaytime, self.URL]
        return bgame
    def getName(self):
        return self.game_name
    def getMinPlayers(self):
        return self.minplayers
    def getMaxPlayers(self):
        return self.maxplayers
    def getGameId(self):
        return self.game_id
    def getUsersRated(self):
        return self.users_rated
    def setUsersRated(self,users_rated):
        self.users_rated = users_rated
    def getAveRate(self):
        return self.average_rate
    def setAveRate(self,average_rate):
        self.average_rate = average_rate
    def update(self):
        ur = str(self.users_rated)
        ar = str(self.average_rate)
        g = str(self.game_id)
        conn = psycopg2.connect( host='localhost', user='postgres', password='123', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'UPDATE "Board_game" SET users_rated='+ur+',average_rate='+ar+' WHERE game_id='+g
        cursor.execute(sqlString)
        conn.commit() 
        cursor.close() 
        conn.close() 
        return 0
#Raw Data Gateway класс для проведения поиска BgameFinder
class BgameFinder:
    def getAllBgames():
        conn = psycopg2.connect( host='localhost', user='postgres', password='123', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM "Board_game"')
        bgames = cursor.fetchall()
        bgames_list = []
        for bg in bgames:
            bgames_list.append(BoardgameGateway(list(bg)))
        cursor.close() 
        conn.close() 
        return bgames_list


#Table Module класс Оценка
class Rate(models.Model):
    rate_table = []
    def __init__(self):
        self.rate_table = RateFinder.getAllRates()
    def findFreeRateId(self):
        rates = self.rate_table
        review_ids = []
        for review in rates:
            review_ids.append(review.getReviewId())
        review_id = generate_id(review_ids)
        return review_id
    def findReview(self,user_id,game_id):
        rates = self.rate_table
        success = False
        for review in rates:
            if (review.getUserId() == user_id) and (review.getGameId() == game_id):
                user_review = review
                success = True
        if success == False:
            user_review = ''
        return user_review
    def getUserGameRate(self,user_id,game_id):
        review = self.findReview(user_id,game_id)
        if review != '':
            rate = review.getRating()
        else:
            rate = ''
        return rate
    def addRate(self,user_id,game_id,rating):
        review_id = self.findFreeRateId()
        review = [review_id,user_id,game_id,rating]
        rate = RateGateway(review)
        rate.insert()
        return 0
    def updateRate(self,user_id, game_id, rating):
        review = self.findReview(user_id,game_id)
        review.setRating(rating)
        review.update()
        return 0
        
#Raw Data Gateway Шлюз записи данных для таблицы Rate
class RateGateway():
    review_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="user")
    game = models.ForeignKey(Boardgame, on_delete=models.CASCADE, related_name ="game")
    rating = models.FloatField()
    def __init__(self,a):
        self.review_id = a[0]
        self.user = a[1]
        self.game = a[2]
        self.rating = a[3]
    def __str__(self):
        return f"{self.review_id} {self.user} {self.game} {self.rating}"
    def getRating(self):
        return self.rating
    def setRating(self,rating):
        self.rating = rating
    def getUserId(self):
        return self.user
    def getGameId(self):
        return self.game
    def getReviewId(self):
        return self.review_id
    def insert(self):
        re = str(self.review_id)
        u = str(self.user)
        g = str(self.game)
        ra = str(self.rating)
        conn = psycopg2.connect( host='localhost', user='postgres', password='123', dbname='Board_gamesDB')
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
        conn = psycopg2.connect( host='localhost', user='postgres', password='123', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'UPDATE "Rate" SET rating='+ra+' WHERE review_id='+re
        cursor.execute(sqlString)
        conn.commit() 
        cursor.close() 
        conn.close() 
        return 0
#Raw Data Gateway класс для проведения поиска RateFinder
class RateFinder():
    def getAllRates():
        conn = psycopg2.connect( host='localhost', user='postgres', password='123', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM "Rate"')
        rates = cursor.fetchall()
        rates_list = []
        for rate in rates:
            rates_list.append(RateGateway(list(rate)))
        cursor.close() 
        conn.close() 
        return rates_list 

   
#Table Module класс Избранное
class Favoured(models.Model):
    fav_table = []
    def __init__(self):
        self.fav_table = FavouredFinder.getAllFavRecords()
    def findFreeFavId(self):
        fav_tab = self.fav_table
        fav = []
        for f in fav_tab:
            fav.append(f.getFavId())
        fav_id = generate_id(fav)
        return fav_id
    def addFavBgame(self,user_id, game_id):
        fav_id = self.findFreeFavId()
        fav_record = [fav_id,user_id, game_id]
        new_fav = FavouredGateway(fav_record)
        new_fav.insert()
        return 0
    def getFavGameIds(self,user_id):  
        fav = self.fav_table
        fav_list = []
        for f in fav:
            if f.getUserId() == user_id:
                fav_list.append(f.getFavGameId())
        return fav_list  
    def deleteFromFav(self,user_id,game_id):
        fav_tab = self.fav_table
        for f in fav_tab:
            if (f.getFavGameId() == game_id) and (f.getUserId()==user_id):
                fav_del = f
        fav_del.delete()
        return 0

#Raw Data Gateway Шлюз записи данных для таблицы Favoured
class FavouredGateway():
    fav_id = models.IntegerField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name ="user")
    game = models.ForeignKey(Boardgame, on_delete=models.CASCADE, related_name ="game")
    def __init__(self, a):
        self.fav_id = a[0]
        self.user = a[1]
        self.game = a[2]           
    def __str__(self):
        return f"{self.fav_id} {self.user} {self.game}"
    def getFavGameId(self):
        return self.game
    def getUserId(self):
        return self.user
    def getFavId(self):
        return self.fav_id
    def insert(self):
        f = str(self.fav_id)
        u = str(self.user)
        g = str(self.game)
        conn = psycopg2.connect( host='localhost', user='postgres', password='123', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'INSERT INTO "Favoured" VALUES ('+f+','+u+','+g+')'
        cursor.execute(sqlString)
        conn.commit() 
        cursor.close() 
        conn.close() 
        return 0
    def delete(self):
        f = str(self.fav_id)
        conn = psycopg2.connect( host='localhost', user='postgres', password='123', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        sqlString = 'DELETE FROM "Favoured" WHERE fav_id='+f
        cursor.execute(sqlString)
        conn.commit() 
        cursor.close() 
        conn.close() 
        return 0

#Raw Data Gateway  класс для проведения поиска FavouredFinder
class FavouredFinder():
    def getAllFavRecords():
        conn = psycopg2.connect( host='localhost', user='postgres', password='123', dbname='Board_gamesDB')
        cursor = conn.cursor() 
        cursor.execute('SELECT * FROM "Favoured"')
        fav = cursor.fetchall()
        fav_list = []
        for f in fav:
            fav_list.append(FavouredGateway(list(f)))
        cursor.close() 
        conn.close() 
        return fav_list    