import pandas as pd
import numpy as np
from sklearn.utils import shuffle
from sklearn.model_selection import train_test_split
import math
from sklearn.ensemble import RandomForestRegressor
from sklearn.preprocessing import StandardScaler, Normalizer, RobustScaler

def out_the_model(filename):
    df = pd.read_csv(filename, delimiter=",")
    zeros = df[df['latitude'] == 0]
    df = df[df['latitude'] != 0]
    subset = list(df.columns.values)
    subset = subset.remove('price')
    data = df.drop_duplicates(subset = subset)
    data = data[data.price < 1000000000]
    data = data[data.price < 800000000]
    data = data[data.price < 400000000]

    data.replace(-1, 0, inplace=True)
    data.replace(' С ', '0', inplace=True)

    data = shuffle(data)
    data.drop(32983, inplace=True)
    data = data.reset_index(drop=True)

    X = data[['room_number', 'house_type', 'district',
        'built_time', 'appartments_floor', 'all_space', 'state', 'bathroom',
        'balcony', 'balcony_glassed', 'door', 'phone', 'ceiling', 'safety',
        'at_the_hotel', 'internet', 'furniture', 'parking', 'building_floors', 'map_complex', 'floor',
            'trngl_first_point', 'trngl_second_point', 'trngl_third_point']]

    y = data['price']
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=7)

    rfr_model = RandomForestRegressor(n_estimators = 200, random_state=7)
    rfr_model.fit(X_train, y_train)
    return rfr_model


def normalization(data):
    to_model = data.split("|")
    temp = ['room_number': to_model[0], 'house_type': '0', 'district':'0',
       'built_time':'0', 'appartments_floor':'0', 'all_space':'0', 'state':'0', 'bathroom':'0',
       'balcony':'0', 'balcony_glassed':'0', 'door':'0', 'phone':'0', 'ceiling':'0', 'safety':'0',
       'at_the_hotel':'0', 'internet':'0', 'furniture':'0', 'parking':'0', 'building_floors':'0', 'map_complex':'0', 'floor':'0',
          'trngl_first_point':'0', 'trngl_second_point':'0', 'trngl_third_point':'0']
    if (to_model[1] in "house_type_иное"):
        temp['house_type_иное'] = 1
    elif (to_model[1] in "house_type_каркасно-камышитовый"):
        temp['house_type_каркасно-камышитовый'] = 1
    elif (to_model[1] in "house_type_кирпичный"):
        temp['house_type_кирпичный'] = 1
    elif (to_model[1] in "house_type_монолитный"):
        temp['house_type_монолитный'] = 1
    elif (to_model[1] in "house_type_панельный"):
        temp['house_type_панельный'] = 1

    if (to_model[2] in "state_евроремонт"):
        temp['state_евроремонт'] = 1
    elif (to_model[2] in "state_свободная планировка"):
        temp['state_свободная планировка'] = 1
    elif (to_model[2] in "state_среднее"):
        temp['state_среднее'] = 1
    elif (to_model[2] in "state_требует ремонта"):
        temp['state_требует ремонта'] = 1
    elif (to_model[2] in "state_хорошее"):
        temp['state_хорошее'] = 1
    elif (to_model[2] in "state_черновая отделка"):
        temp['state_черновая отделка'] = 1

    if (to_model[5] in "bathroom_2 с/у и более"):
        temp['bathroom_2 с/у и более'] = 1
    elif (to_model[5] in "bathroom_нет"):
        temp['bathroom_нет'] = 1
    elif (to_model[5] in "bathroom_раздельный"):
        temp['bathroom_раздельный'] = 1
    elif (to_model[5] in "bathroom_совмещенный"):
        temp['bathroom_совмещенный'] = 1


    temp['built_time'] = float(to_model[6])
    temp['all_space'] = float(to_model[7])
    temp['balcony'] = float(to_model[8])
    temp['phone'] = float(to_model[9])
    temp['parking'] = float(to_model[10])
    temp['furniture'] = float(to_model[11])
    temp['at_the_hostel'] = float(to_model[12])
    temp['appartments_floor'] = float(to_model[13])
    temp['building_floors'] = float(to_model[14])
    lat, lon = HousePricing.yandex_geocoder(to_model[15])
    temp['trngl_first_point'] = ((43.340777 - float(lat)) + (76.950168 - float(lon)))
    temp['trngl_second_point'] = ((43.232742 - float(lat)) + (76.797475 - float(lon)))
    temp['trngl_third_point'] = ((43.196848 - float(lat)) + (76.979312 - float(lon)))
    answer = pd.DataFrame(temp, index=[0])
    return answer


def predict(model, data):
    answer = normalization(data)
    return model.predict(answer)

def main():
    //do smth

main()