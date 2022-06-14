#!/usr/bin/env python
# coding: utf-8

# # Скрипт для сбора информации об авиабазе

# ## Импортируем библиотеки

# In[15]:


import numpy as np 
import pandas as pd 
import pyflightdata 
import time  


# ## Создаем объект f класса FlightData модуля pyflightdata и используем метод 'login' (входим в аккаунт flightradar24)

# In[16]:


#Объект
f=pyflightdata.FlightData()

#Зарегестрируйтесь на сайте www.flightradar24.com  НЕ ИСПОЛЬЗУЙТЕ УКАЗАННЫЕ НИЖЕ ЛОГИН И ПАРОЛЬ
f.login('azazel1416@yandex.ru','Radar534')


# ## Создаем DataFrame с указанными полями, а также определяем список авиабаз

# In[48]:


#Датафрейм
data = pd.DataFrame(columns = ['name','code','country','city','latitude','longitude','imageLink'])

#Список авиабаз
afbList = ['LTAG', 'KLTS','PGUA','OAIX','KXMR','KVBG','KDYS','KDMA','KXTA',
'DNA','UTSL','BIKF','KUV','EGUL','KLFI','FRU','EGUN','KLSV','KOFF','RMS','KROW','BGTL',
'KSZL','EGVA','OASD','EDW','PAED','KADW','KVOK','KVD','YLV','UBBI','LIPA','RIV','SUU','WHP','TAY','TLL','EPU','KDL','URE ','RIX',
'VNT','LPX','VNO','KUN','SQQ','PLQ','GDN','SZZ','BZG','POZ','WMI','WAW','LCJ','LUZ','WRO','KTW','KRK','RZE','IEV','RWN',
'GML','VIN','ADB','ADA','TBS','KBP','PED','KBL']


# ## Пример ответа с сайта flightradar24  при использовании метода 'get_airport_details'

# In[55]:


#Получаем подробную информацию об авиабазе
res = f.get_airport_details('LTAG')
res


# ## Алгоритм сбора даных

# In[51]:


#Для каждой afb из списка:
for i in afbList:
    
    main = f.get_airport_details(i) #Метод для получения информации об afb с сайта fr24 
    time.sleep(2) #Искуственная задержка 2сек,чтобы избежать 429 ошибки
    
    if main != []:
        
        #Название  afb
        if main['name'] != '':
            name = main['name']
        else:
            name = '-'
            
        
        #Код afb
        code = i 
        
        #Страна, в которой находится afb
        if main['position']['country']['name'] != '':
            country = main['position']['country']['name']
        else:
            country = '-'
        
        #Населенный пункт
        if main['position']['region']['city'] != '':
            city = main['position']['region']['city']
        else:
            city = '-'
            
        #Координаты для дальнейшего нанесения маркеров на карту
        if main['position']['latitude'] != '':
            latitude = main['position']['latitude']
        else:
            latitudetude = '-'
        if main['position']['longitude'] != '':
            longitude = main['position']['longitude']
        else:
            longitude = '-'
        
        #Фото аэропорта - ВПП/терминал/что-то
        if main['airportImages'] != 'None':
            if main['airportImages']['large'][0]['link'] != '':
                imageLink = main['airportImages']['large'][0]['link']
                print(imageLink)
            else:
                imageLink = '-'
        else:
            imageLink = '-'
        
        #Запись строки в DataFrame
        data.loc[len(data)] = [name, code, country, city, latitude, longitude, imageLink]


# ## Отображаем таблицу

# In[ ]:


#Удаляем дубликаты
data.drop_duplicates()

#Отображаем таблицу
data

