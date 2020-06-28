# -*-coding: UTF-8 -*-

from flask import Flask, render_template, request, redirect, url_for
import pandas as pd
import folium
from pyroutelib3 import Router
import threading
import handle
import random


app = Flask(__name__)
after_dot = 1000
city = str()
places = list()
tr_choice = str()
routes = dict()
places_number_name = dict()
places_name_coor = dict()
week_routes = dict()
name_in = 'SampleIn_1.txt'


def find_route(names: list, pos: (float, float), transport_type: str):
    """
    creates a file with distance matrix among chosen places

    :param names: names of the places you want to visit
    :param pos: your position at the moment (starting point)
    :param transport_type: obvious
    :return: None
    """

    global after_dot, routes, places_number_name, places_name_coor, name_in, city

    places_number_name[1] = 'curr_pos'

    for i in range(1, len(names) + 1):
        places_number_name[i + 1] = names[i - 1]

    places_name_coor['curr_pos'] = pos

    data = pd.read_csv(city + ".csv")
    all_names = data['Название']
    all_lon = data['Долгота']
    all_lat = data['Широта']
    wh = list()
    types = ['Памятники', 'Дома и дворцы', 'Башни и ворота', 'Современные здания', 'Московское центральное кольцо (МЦК)']

    for name in names:
        places_name_coor[name] = (all_lon[pd.Index(all_names).get_loc(name.replace(',', '+++'))], all_lat[pd.Index(all_names).get_loc(name.replace(',', '+++'))])

    file_m = open(name_in, 'w', encoding='UTF-8')
    file_m.write(str(len(names) + 1) + '\n')
    router = Router(transport_type)  # , 'static/Moscow_test.osm')
    key = 0
    for name_start in places_name_coor.keys():
        if name_start != 'curr_pos':
            idx = pd.Index(all_names).get_loc(name_start.replace(',', '+++'))
            type = data['Тип Постройки'][pd.Index(all_names).get_loc(name_start.replace(',', '+++'))]
            week = [data['Mon'][idx],
                    data['Tue'][idx],
                    data['Wed'][idx],
                    data['Thu'][idx],
                    data['Fri'][idx],
                    data['Sat'][idx],
                    data['Sun'][idx]
                    ]
            for d in week:
                if d != 'None':
                    wh.append(' 1 ')
                elif type not in types:
                    wh.append('-1 ')
                else:
                    wh.append(' 1 ')
        wh.append('\n')
        to_write = str()
        start = router.findNode(places_name_coor[name_start][0], places_name_coor[name_start][1])
        for name_end in places_name_coor.keys():
            key += 1
            end = router.findNode(places_name_coor[name_end][0], places_name_coor[name_end][1])
            status, route = router.doRoute(start, end)
            if status == 'success':
                routeLatLons = list(map(router.nodeLatLon, route))
                routes[key] = routeLatLons
                '''
                print('\n\n+++++++++++++++\n\n',
                      '>>>>>>>', routeLatLons,
                      '\n\n+++++++++++++++\n\n')
                '''
                sum_ = 0

                for i in range(len(routeLatLons) - 1):
                    sum_ += router.distance(routeLatLons[i], routeLatLons[i + 1])
                sum_ *= after_dot
                to_write += ' ' + str(sum_)[:str(sum_).index('.')] + ' '
            elif status == 'no_route':
                routes[key] = route
                to_write += '-1 '
        to_write = to_write.rstrip()
        file_m.write(to_write + '\n')

    for i in wh:
        file_m.write(i)
    file_m.close()


@app.route('/waiting/<name>')
def wait(name):
    t = threading.enumerate()
    t_names = list()
    for t_i in t:
        t_names.append(t_i.getName())
    # print(t_names)
    if name in t_names:
        return render_template('wait.html')
    else:
        return redirect(url_for('done'))


@app.route('/done', methods=['POST', 'GET'])
def done():
    global routes, city, places_name_coor, places_number_name, after_dot, week_routes

    # print(places_number_name)

    chosen_day = 'AllToday'

    if request.method == 'GET':
        week_routes.clear()
        handle.main(name_in)

        file = open('Output.txt', 'r')

        amount = int(file.readline())
        for i in range(amount):
            order = eval(file.readline())
            cost = int(file.readline())
            day = file.readline().strip()
            reindex = eval(file.readline())

            week_routes[day] = [order, cost, reindex]

        file.close()

        num_icon = {0: 'https://cdn4.iconfinder.com/data/icons/go-round-the-houses/60/house-location-512.png',
                    1: 'https://cdn2.iconfinder.com/data/icons/integers/60/number-one-512.png',
                    2: 'https://cdn2.iconfinder.com/data/icons/integers/60/number-two-512.png',
                    3: 'https://cdn2.iconfinder.com/data/icons/integers/60/number-three-512.png',
                    4: 'https://cdn2.iconfinder.com/data/icons/integers/60/number-four-512.png',
                    5: 'https://cdn2.iconfinder.com/data/icons/integers/60/number-five-512.png',
                    6: 'https://cdn2.iconfinder.com/data/icons/integers/60/number-six-512.png',
                    7: 'https://cdn2.iconfinder.com/data/icons/integers/60/number-seven-512.png',
                    8: 'https://cdn2.iconfinder.com/data/icons/integers/60/number-eight-512.png',
                    9: 'https://cdn2.iconfinder.com/data/icons/integers/60/number-nine-512.png'}

        for day in week_routes.keys():
            route_map = folium.Map(location=places_name_coor['curr_pos'], zoom_start=10)
            for i, node in enumerate(week_routes[day][0]):
                folium.Marker(
                    location=places_name_coor[places_number_name[week_routes[day][-1][node[0]]]],
                    popup=places_number_name[week_routes[day][-1][node[0]]].replace('curr_pos', 'Вы'),
                ).add_to(route_map)

            order = week_routes[day][0]
            reindex = week_routes[day][-1]
            n = int(len(routes) ** (1 / 2))
            # print(day)
            for place_i in order:
                # print(place_i[0] - 1, place_i[1])
                # print(reindex[place_i[0]] - 1, reindex[place_i[1]])
                r = hex(random.randint(0, 255))[2:]
                g = hex(random.randint(0, 255))[2:]
                b = hex(random.randint(0, 255))[2:]
                if len(r) == 1:
                    r = '0' + r
                if len(g) == 1:
                    g = '0' + g
                if len(b) == 1:
                    b = '0' + b

                color = '#' + r + g + b
                # print(color)
                folium.PolyLine(
                    routes[(reindex[place_i[0]] - 1) * n + reindex[place_i[1]]],
                    color=color
                ).add_to(route_map)
            route_map.save('templates/week/' + day + '.html')

    if request.method == 'POST':
        chosen_day = request.form.get('day')

    order = week_routes[chosen_day][0]
    reindex = week_routes[chosen_day][-1]
    names_ordered = list()
    names_ordered.append(places_number_name[reindex[order[0][0]]].replace('curr_pos', 'Текущее местоположение'))
    for place_i in order:
        names_ordered.append(places_number_name[reindex[place_i[1]]].replace('curr_pos', 'Текущее местоположение'))

    return render_template(
        'done.html',
        cost=week_routes[chosen_day][1] / after_dot,
        order=names_ordered,
        day=chosen_day,
        days=week_routes.keys()
    )


@app.route("/", methods=['POST', 'GET'])
def register():
    tt = {'car': 'Машина', 'cycle': 'Велосипед/мотоцикл', 'foot': 'Пешком'}
    global city, places, tr_choice
    start_coords = {'Москва': [55.7522200, 37.6155600], 'Санкт-Петербург': [59.9386300, 30.3141300], '': [55.7522200, 37.6155600]}
    if request.method == 'POST':
        if 'city' in request.form.to_dict().keys():
            city = request.form.get('city')
        if 'tr_type' in request.form.to_dict().keys():
            tr_choice = request.form.get('tr_type')
        if 'places' in request.form.to_dict().keys():
            places = request.form.getlist('places')
        if city and tr_choice and places:
            t = threading.Thread(target=find_route, args=(places, (55.803139, 37.409651), tr_choice), daemon=False)
            t.start()
            return redirect(url_for('wait', name=t.getName()))
        if city:
            folium_map = folium.Map(location=start_coords[city], zoom_start=12)
            folium_map.save("templates/" + city + ".html")
    elif request.method == 'GET':
        city = ''
        places = []
        tr_choice = ''

    d = dict()

    if city:
        data = pd.read_csv(city + '.csv')
        d = dict(zip(data['Название'], list(zip(data['Долгота'], data['Широта']))))

    return render_template('layout.html', options=d, sc=city, types=tt, tc=tr_choice)


if __name__ == "__main__":
    app.run(debug=False, host='0.0.0.0', port=8080)
