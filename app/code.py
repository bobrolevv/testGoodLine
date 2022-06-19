import requests, pprint
from bs4 import BeautifulSoup



def parse1(id):
    req = requests.get(url=f'https://reqres.in/api/users?id={id}').json()
    result = (req.get('data')['first_name']
              + ' '
              + req.get('data')['last_name'])
    return result


def groups(data):
    result = {}     # пустой началдьный словарь
    count = 0       # начальное количество сотрудников отдела
    people_up = 0   # начальное количество ЖИВЫХ сотружников отдела (тех, кто работал)
                    # в конце нужно будет уьрать из выдачи
    avg_hours = 0   # начальное средняя выработка

    # 1 проход, формируем список отделов с начальными (нулевыми) данными
    for item in data:
        result[item.get('dept')] = {
            'count': count,
            'avg_hours': avg_hours,
            'people': [],
            'people_up': people_up
        }

    # 2 проход, реализуем логику подсчета
    for item in data:
        # временно, в avg_hours будем суммировать нароботку
        avg_hours = result[item.get('dept')]['avg_hours']

        # считаем количество сотрудников в отделе
        result[item.get('dept')]['count'] = (
                result[item.get('dept')]['count'] + 1)

        # наполняем отдел сотрудниками
        result[item.get('dept')]['people'].append(
            {'name': item.get('name'),
             'phone': item.get('phone')})

        if item.get('hours'):
            # считаем количество ЖИВЫХ
            result[item.get('dept')]['people_up'] = (
                    result[item.get('dept')]['people_up'] + 1)

            # суммируем часы в avg_hours
            result[item.get('dept')]['avg_hours'] = (
                    avg_hours + item.get('hours'))


    # считаем среднюю нароботку (сумма часов / к-во ЖИВЫХ)
    result[item.get('dept')]['avg_hours'] = round(
        result[item.get('dept')]['avg_hours'] /
        result[item.get('dept')]['people_up']
        )

    # удаляем people_up из выдачи
    result[item.get('dept')].pop('people_up')

    return result


def parse2():
    # url = 'https://www.kinopoisk.ru/premiere/ru/'
    # headers = {
    #     'Accept': '*/*',
    #     'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'
    # }
    #
    # req = requests.get(url=url, headers=headers).text
    # with open('index.html', 'w') as f:
    #     f.write(req)

    with open('index.html', 'r') as f:
        src = f.read()

    soup = BeautifulSoup(src, 'lxml')
    prem = soup.find_all('div', class_='premier_item')
    # print(prem[0])
    for item in prem:
        print(item)
        print('name:', item.find('div', class_='textBlock').find('a').text)
        print('name_eng:', item.find('div', class_='textBlock').find('a').next_element.next_element.next_element.text)
        print('film_link:', 'https://www.kinopoisk.ru/'+ item.find('a').get('href'))
        print('film_rating:', item.find('span', class_='ajax_rating'))
        print('-'*10)

parse2()
