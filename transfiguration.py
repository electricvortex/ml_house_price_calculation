import pandas as pd
import numpy as np


def floor_divider(df):
    floor = df['appartments_floor']
    building_floor = np.zeros(len(floor))
    appartments_floor = np.zeros(len(floor))
    for i in range(len(floor)):
        if ("из" in floor[i]):
            temp = floor[i].split("из")
            building_floor[i] = temp[1]
            appartments_floor[i] = temp[0]
        else:
            building_floor[i] = 0
            appartments_floor[i] = 0

    df['appartments_floor'] = appartments_floor
    df['building_floors'] = building_floor
    return df


def built_time_divider(df):
    time = df['built_time']
    temp = np.zeros(len(time))
    for i in range(len(time)):
        if "г.п." in time[i]:
            temporary = time[i]
            temp[i] = temporary[:-4]
        else:
            temp[i] = time[i]

    df['built_time'] = temp
    return df


def triangulation(df):
    latitude = df['latitude']
    longitude = df['longitude']
    #Almaty - 1: 43.340777, 76.950168
    #Kalkaman - 1: 43.232742, 76.797475
    #Tausamal: 43.196848, 76.979312
    first_point = []
    second_point = []
    third_point = []
    for i in range(len(latitude)):
        first_point.append((43.340777 - latitude[i]) + (76.950168 - longitude[i]))
        second_point.append((43.232742 - latitude[i]) + (76.797475 - longitude[i]))
        third_point.append((43.196848 - latitude[i]) + (76.979312 - longitude[i]))
    
    df['trngl_first_point'] = first_point
    df['trngl_second_point'] = second_point
    df['trngl_third_point'] = third_point
    return df


def return_normalized(csv_name):
    columns = ['Index', 'district', 'address', 'room_number', 'price', 'map_complex', 'house_type', 'built_time',
          'appartments_floor', 'all_space', 'state', 'bathroom', 'balcony', 'balcony_glassed', 'door',
          'phone', 'ceiling', 'safety', 'at_the_hotel', 'internet', 'furniture', 'floor', 'parking', 
           'latitude', 'longitude']
    data = pd.read_csv(csv_name, delimiter=";", header = None)
    data.columns = columns
    data['price'] = data['price'].str.replace("\xa0", "")
    data['price'] = data['price'].str.replace("₸", "")
    data.price = data.price.astype(int)

    data = floor_divider(data)
    data['built_time'] = data['built_time'].str.replace("г.п.", "")
    data['all_space'] = data['all_space'].str.replace("м2", "")
    data['ceiling'] = data['ceiling'].str.replace("м ", "")
    data.replace(-1, 0, inplace=True)
    #replacing -1 with 0 (-1 as object)
    tr = data['floor'][0]
    vl = 0
    data.replace(to_replace=tr, value=vl, inplace=True)
    #Replacing string with int
    data['state'].replace([' черновая отделка ', ' свободная планировка ', ' хорошее ',
        ' среднее ', ' евроремонт ', ' требует ремонта '], [2 , 1, 5, 4, 6, 3], inplace=True)
    data['bathroom'].replace([' 2 с/у и более ', ' совмещенный ', ' раздельный ',' нет '], 
                        [3, 1, 2, 0], inplace=True)
    data['balcony'].replace([' лоджия ', 0, ' балкон ', ' несколько балконов или лоджий ',
        ' балкон и лоджия '], [2, 0, 1, 4, 3], inplace=True)
    data['balcony_glassed'].replace([' да ', 0], [1, 0], inplace=True)
    data['at_the_hotel'].replace([' нет ', ' да ', 0], [0, 1, 0], inplace=True)
    data['door'].replace([' бронированная ', ' металлическая ', ' деревянная ', 0], [3, 2, 1, 0], inplace=True)
    data['phone'].replace([' есть возможность подключения ', 0, ' отдельный ', ' нет ',
        ' блокиратор '], [ 3, 0, 4, 0, 2], inplace=True)
    data['internet'].replace([' оптика ', 0, ' через TV кабель ', ' ADSL ', ' проводной '], [ 4, 0, 1, 2, 3],
                            inplace=True)
    data['furniture'].replace([' пустая ', ' полностью меблирована ', ' частично меблирована ', 0], [0, 1, 0.5, 0],
                            inplace=True)
    data['parking'].replace([' паркинг ', 0, ' рядом охраняемая стоянка ', ' гараж '], [1, 0, 1, 1],
                        inplace=True)
    data['house_type'].replace([' монолитный ', ' панельный ', ' кирпичный ', 0,
        ' каркасно-камышитовый ', ' иное '], [ 3, 2, 4, 0, 1, 0], inplace=True)
    data['floor'].replace([' -1 ', ' линолеум ', ' ламинат ', ' паркет ', ' дерево ',
        ' плитка ', ' пробковое ', ' ковролан '], [0, 1, 6, 7, 5, 3, 4, 2], inplace=True)

    data = triangulation(data)

    names = data['map_complex'].unique()
    complexs = data['map_complex']
    ans = np.zeros(len(data))
    for i in range(len(names)):
        for j in range(len(data)):
            if names[i] == complexs[j]:
                ans[j] = i
                
    data['map_complex'] = ans

    data.to_csv("new_dtrain.csv", index=False)

def main():
    return_normalized("tocsv.txt")


main()