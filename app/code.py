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


# def req():
#     url = 'https://www.kinopoisk.ru/premiere/ru/'
#     headers = {
#         'Accept': '*/*',
#         'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'
#     }
#
#     for number in range(1, 10):
#         req2 = requests.get(url=f'{url}page//{number}//', headers=headers)
#         print(number, req2.url, req2.status_code)
#         # with open('index.html', 'w') as f:
#         #     f.write(req)
#         soup = BeautifulSoup(req2.text, 'lxml')
#         try:
#             end = soup.find('div', class_='js-rum-hero'
#                      ).find('td', class_='news').text
#             break
#         except Exception:
#             pass



def parse2():
    url = 'https://www.kinopoisk.ru/premiere/ru/'
    headers = {
        'Accept': '*/*',
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:101.0) Gecko/20100101 Firefox/101.0'
    }

    i = 0
    for number in range(1, 10):
        req2 = requests.get(url=f'{url}page//{number}//', headers=headers)
        soup = BeautifulSoup(req2.text, 'lxml')

        try:
            end = soup.find('div', class_='js-rum-hero'
                     ).find('td', class_='news').text
            break
        except Exception:
            prem = soup.find_all('div', class_='premier_item')

            for item in prem:
                i += 1
                print(i)
                print('name:', item.find('div', class_='textBlock').find('a').text)
                print('name_eng:', item.find('div', class_='textBlock').find('a').next_element.next_element.next_element.text)
                print('film_link:', 'https://www.kinopoisk.ru/'+ item.find('a').get('href'))

                if item.find('span', class_='ajax_rating').find('u'):
                    film_rating = item.find('span', class_='ajax_rating').find('u').text.strip()
                print('film_rating:', film_rating.partition('\xa0')[0])

                print('wait_rating:', '-')

                if item.find('span', class_='ajax_rating').find('b'):
                    votes = item.find('span', class_='ajax_rating').find('b').text.strip()
                print('votes:', votes)

                print('date:', item.find('meta').get('content'))

                print('company:', item.find('s', class_='company').find('a').text)
                print('genres:', item.find('div', class_='textBlock').find_all('span')[3].text)

                print('-'*10)

        # name - название фильма
        # name_eng - название фильма на английском
        # film_link - ссылка на страницу фильма
        # film_rating - рейтинг фильма(если есть)
        # wait_rating - рейтинг ожидания(если есть)
        # votes - количество голосов
        # date - дата премьеры
        # company - компания, выпускающая фильм
        # genres - жанры фильма(массив)

def main():
    parse2()
    # req()

if __name__ == '__main__':
    main()
