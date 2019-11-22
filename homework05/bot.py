import requests
import config
import telebot
from datetime import datetime
from bs4 import BeautifulSoup
from telebot import apihelper

access_token = config.access_token
apihelper.proxy = {'https': 'socks5://georgy.komarov:2naturala1613@aws.komarov.ml:7777'}
bot = telebot.TeleBot(access_token)


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}/raspisanie_zanyatiy_{group}.htm'.format(
        domain='http://www.ifmo.ru/ru/schedule/0/',
        week=week,
        group=group
    )
    response = requests.get(url)
    web_page = response.text
    return web_page

def parse_schedule_for_a_monday(web_page):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": "1day"})


    # Время проведения занятий
    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday'])
def get_monday(message):
    """ Получить расписание на понедельник """
    _, group = message.text.split()
    web_page = get_page(group)
    times_lst, locations_lst, lessons_lst = parse_schedule_for_a_monday(web_page)
    resp = ''
    for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
        resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


DAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']


def get_schedule(web_page, day):
    """ Получить расписание на указанный день """

    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на день
    schedule_table = soup.find("table", attrs={"id": f"{DAYS.index(day) + 1}day"})
    print(schedule_table)
    if schedule_table == None:
        pass
    else:

        # Время проведения занятий
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]

        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
        return times_list, locations_list, lessons_list

@bot.message_handler(commands=DAYS)
def get_day(message):

    _, week, group = message.text.split()
    day = _[1:]
    web_page = get_page(group, week)
    if get_schedule(web_page, day) == None:
        bot.send_message(message.chat.id, 'Тебе повезло - в этот день нет занятий!', parse_mode='HTML')
    else:
        times_lst, locations_lst, lessons_lst = get_schedule(web_page, day)
        resp = ''
        for time, location, lession in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')

@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _, week, group = message.text.split()
    web_page = get_page(group, week)
    soup = BeautifulSoup(web_page, "html5lib")
    resp = ''
    days_rus = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота' ]
    for i in range(6):
        schedule_table = soup.find("table", attrs={"id": f"{i + 1}day"})
        if schedule_table != None:
            times_list = schedule_table.find_all("td", attrs={"class": "time"})
            times_list = [time.span.text for time in times_list]

            # Место проведения занятий
            locations_list = schedule_table.find_all("td", attrs={"class": "room"})
            locations_list = [room.span.text for room in locations_list]

            # Название дисциплин и имена преподавателей
            lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
            lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
            lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

            times_lst, locations_lst, lessons_lst = \
                times_list, locations_list, lessons_list
            resp += days_rus[i] + "\n"
            for time, location, lession in zip(times_lst, locations_lst, lessons_lst):

                resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
    bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['tommorow'])
def get_tommorow(message):
    """ Получить расписание на следующий день """
    _, group = message.text.split()
    s = datetime.today().weekday()
    week = '0'
    web_page = get_page(group, week)
    parity = ['Четная', 'Нечетная']
    soup = BeautifulSoup(web_page, "html5lib")
    week_parity = soup.find("p", attrs={"class": "col-lg-3 navbar-text visible-lg-block"})
    week_parity = week_parity.find("strong")
    if parity[1] in week_parity:
        week = '2'
    else:
        week = '1'
    if s == 6:
        s = -1
        week = (str(int(week) + 1) % 2)
    web_page = get_page(group, week)
    soup = BeautifulSoup(web_page, "html5lib")
    schedule_table = soup.find("table", attrs={"id": f"{s + 2}day"})
    if schedule_table != None:
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]
        # Место проведения занятий
        locations_list = schedule_table.find_all("td", attrs={"class": "room"})
        locations_list = [room.span.text for room in locations_list]

        # Название дисциплин и имена преподавателей
        lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
        lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
        lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
        resp = ''
        for time, location, lession in zip(times_list, locations_list, lessons_list):
            resp += '<b>{}</b>, {}, {}\n'.format(time, location, lession)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')

    else:
        bot.send_message(message.chat.id, 'Завтра у тебя нет пар!', parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    a = datetime.today()
    a1 = str(a.hour)
    a2 = str(a.minute)
    if a.hour < 10:
        a1 = '0' + str(a.hour)
    if a.minute < 10:
        a2 = '0' + str(a.minute)
    time_now = a1 + ':' + a2
    _, group = message.text.split()
    s = datetime.today().weekday()
    week = '0'
    web_page = get_page(group, week)
    parity = ['Четная', 'Нечетная']
    soup = BeautifulSoup(web_page, "html5lib")
    week_parity = soup.find("p", attrs={"class": "col-lg-3 navbar-text visible-lg-block"})
    week_parity = week_parity.find("strong")
    if parity[1] in week_parity:
        week = '2'
    else:
        week = '1'
    web_page = get_page(group, week)
    soup = BeautifulSoup(web_page, "html5lib")
    for i in range(7):
        schedule_table = soup.find("table", attrs={"id": f"{s + 1}day"})
        if schedule_table != None:
            times_list = schedule_table.find_all("td", attrs={"class": "time"})
            times_list = [time.span.text for time in times_list]
            # Место проведения заняти
            locations_list = schedule_table.find_all("td", attrs={"class": "room"})
            locations_list = [room.span.text for room in locations_list]

            # Название дисциплин и имена преподавателей
            lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
            lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
            lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]
            for time in times_list:
                if time < time_now:
                    i = times_list.index(time)
                    # Место проведения заняти
                    locations_list = locations_list[i]

                    # Название дисциплин и имена преподавателей
                    lessons_list = lessons_list[i]
                    resp = ''
                    resp += '<b>{}</b>, {}, {}\n'.format(time, locations_list, lessons_list)
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                    s = 10
                    break
        if s != 10:
            s = (s + 1) % 7
        else:
            break


bot.remove_webhook()
bot.polling()
