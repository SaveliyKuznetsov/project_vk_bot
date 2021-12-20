import vk_api
from vk_api.bot_longpoll import VkBotLongPoll, VkBotEventType
import random
from vk_api import VkUpload
import datetime
from data import *
import requests
import bs4

TOKEN = '---'

vk = vk_api.VkApi(token=TOKEN)

upload = VkUpload(vk)
session = requests.Session()


# вывод сообщений в беседу
def send_messages(id1, text, attr=''):
    """

    :param id1: id того, с кем мы общаемся
    :param text: сообщения для вывода
    :param attr: проверка на пустоту сообщения
    :return:
    """
    random_id = random.randint(0, 1000000)
    if not attr:
        vk.method('messages.send', {'chat_id': id1, 'message': text, 'random_id': random_id})
    else:
        vk.method('messages.send',
                  {'chat_id': id1, 'message': text, 'random_id': random_id, 'attachment': attr})


# имя по ид
def _get_user_name(self, user_id):
    """

    :param user_id: id пользователя
    :return:  Имя пользователя
    """
    request = requests.get("https://vk.com/id" + str(user_id))
    bs = bs4.BeautifulSoup(request.text, "html.parser")
    user_name = str(bs.findAll("title")[0])
    print(user_name.split(' | ')[0])
    return user_name.split()[0][7:]


# сколько дней до...
def t_d(chat_id, msg):
    """

    :param chat_id: id чата в котором обрабатывается запрос пользователя
    :param msg: сообщение пользователя
    в ответ возвращаем сообщение по запросу
    """
    try:
        date1 = msg.lower()[16:]
        if date1.lower() == "лета" or date1.lower() == "лето":
            if 5 < datetime.date.today().month < 9:
                send_messages(chat_id, f'Уже лето!')
                date1 = datetime.date.today()
            elif datetime.date.today().month >= 9:
                d = datetime.date.today().year + 1
                date1 = datetime.date(d, 6, 1)
            else:
                d = datetime.date.today().year
                date1 = datetime.date(d, 6, 1)
        elif date1.lower() == "весны" or date1.lower() == "весна":
            if 2 < datetime.date.today().month < 6:
                send_messages(chat_id, f'Уже весна!')
                date1 = datetime.date.today()
            elif datetime.date.today().month >= 6:
                d = datetime.date.today().year + 1
                date1 = datetime.date(d, 3, 1)
            else:
                d = datetime.date.today().year
                date1 = datetime.date(d, 3, 1)
        elif date1.lower() == "осень" or date1.lower() == "осени":
            if 8 < datetime.date.today().month < 12:
                send_messages(chat_id, f'Уже осень!')
                date1 = datetime.date.today()
            elif datetime.date.today().month >= 12:
                d = datetime.date.today().year + 1
                date1 = datetime.date(d, 9, 1)
            else:
                d = datetime.date.today().year
                date1 = datetime.date(d, 9, 1)
        elif date1.lower() == "зима" or date1.lower() == "зимы":
            if (datetime.date.today().month < 3) or (datetime.date.today().month == 12):
                send_messages(chat_id, f'Уже зима!')
                date1 = datetime.date.today()
            else:
                d = datetime.date.today().year
                date1 = datetime.date(d, 12, 1)
        elif date1.lower() == "нового года" or date1.lower() == "новый год":
            d = datetime.date.today().year + 1
            date1 = datetime.date(d, 1, 1)
        else:
            inp = date1.split('.')
            if len(inp) != 3:
                send_messages(chat_id, f'Такой даты нет! Может, вы имели в виду сегодня?')
                date1 = datetime.date.today()
            else:
                date1 = [int(x) for x in inp]
                date1 = datetime.date(date1[-1], date1[-2], date1[0])
        cur_date = datetime.date.today()
        delta = date1 - cur_date
        send_messages(chat_id, f'Осталось всего {delta.days} дней. Это не так уж и много')
    except ValueError:
        send_messages(chat_id, f'Неподходящий формат - введите дату в формате дд.мм.гггг')
    except TypeError:
        send_messages(chat_id, f'Ошибка типа сообщения')


# слова наоборот
def abirgame(chat_id, word):
    """

    :param chat_id: id чата в котором обрабатывается запрос пользователя
    :param word: слово которое нам написал пользователь
    :return: Отправляем сообщение либо выходим из функции
    """
    if word.lower() == 'ценок':
        return False
    else:
        send_messages(chat_id, word[::-1])
        return True


# верю не верю
def true_or_false(chat_id, inpu, number):
    """

    :param chat_id: id чата в котором обрабатывается запрос пользователя
    :param inpu: сообщение на вход от пользователя
    :param number: номер карточки вопроса

    """
    if inpu == 'хватит':
        send_messages(chat_id, 'Ладно, больше не буду')
        return False, 0
    if ans_dict[inpu] == ANS_CARDS[number]:
        send_messages(chat_id, 'Ты прав')
    else:
        send_messages(chat_id, 'Не угадал')
    number = random.randint(0, len(QUE_CARDS) - 1)
    send_messages(chat_id, QUE_CARDS[number])
    return True, number


# виселица
def gallows(chat_id, char):
    """

    :param chat_id: id чата в котором обрабатывается запрос пользователя
    :param char: сообщение пользователя
    :return: возвращаем то, угадал ли пользователь букву
    """
    global nu, visTrue, current_ans, wrong
    char = char.lower()
    if char == 'сдаюсь':
        send_messages(chat_id, 'Вы закончили игру')
        visTrue = False
        send_messages(chat_id, f'Правильный ответ: {ANWERS[nu+1]}')
        return visTrue
    if not char.isalpha() or len(char) != 1:
        send_messages(chat_id, 'Введите одну букву, пожалуйста')
        send_messages(chat_id, '  '.join(current_ans))
        send_messages(chat_id, 'Введите букву: ')
        return visTrue
    if char in current_ans:
        send_messages(chat_id, 'Эта буква уже открыта')
        send_messages(chat_id, '  '.join(current_ans))
        send_messages(chat_id, 'Введите букву: ')
        return visTrue
    elif char in ANWERS[nu].lower() and char not in current_ans:
        for flag in range(len(ANWERS[nu])):
            if char == ANWERS[nu][flag].lower():
                current_ans[flag] = char
        if '-' not in current_ans:
            send_messages(chat_id, f'Правильный ответ: {ANWERS[nu]}')
            send_messages(chat_id, 'Поздравляем, вы выиграли!')
            visTrue = False
            return visTrue
        send_messages(chat_id, '  '.join(current_ans))
        send_messages(chat_id, 'Введите букву: ')
        return visTrue
    else:
        wrong += 1
        if wrong == MAX_WRONG:
            send_messages(chat_id, 'Попыток не осталось. Вы проиграли =((')
            send_messages(chat_id, f'Правильный ответ: {ANWERS[nu]}')
            visTrue = False
            return visTrue
        send_messages(chat_id, f'Такой буквы нет. Осталось попыток: {MAX_WRONG - wrong}')
        send_messages(chat_id, '  '.join(current_ans))
        send_messages(chat_id, 'Введите букву: ')
        return visTrue



def know_nomber(chat_id, text, num, knownumTrue, raund):
    """

    :param chat_id: id чата в котором обрабатывается запрос пользователя
    :param text: сообщение пользвателя
    :param num: загаданное число
    :param knownumTrue: параметр в списке
    :param raund: номер раунда

    """
    if text == num:
        send_messages(chat_id, 'Верно! Победа =)) С ' + str(raund) + " попытки")
        return [False, 1]
    elif text < num:
        send_messages(chat_id, 'Больше бери!')
        raund += 1
    else:
        send_messages(chat_id, 'Много! Уменьшай')
        raund += 1
    return knownumTrue, raund


# крестики-нолики
def krestnul(p, desk, c):
    """

    :param p: номер игрока
    :param desk: рисунок нашей доски
    :param c: координаты клетки которую дал пользователь
    :return:
    """
    c = [int(c[0]), int(c[2])]
    if desk[c[0]][c[1]] == '.':
        if p == 1:
            desk[c[0]][c[1]] = '+'
        else:
            desk[c[0]][c[1]] = '0'
        send_messages(chat_id, f'  '.join(desk[0]))
        send_messages(chat_id, f'  '.join(desk[1]))
        send_messages(chat_id, f'  '.join(desk[2]))
        send_messages(chat_id, f'  '.join(desk[3]))
    else:
        send_messages(chat_id, 'Неверный ход')
        return 0, desk
    if desk[1][1] == desk[1][2] == desk[1][3] == '+' or desk[2][1] == desk[2][2] == desk[2][
        3] == '+' or \
            desk[3][1] == desk[3][2] == desk[3][3] == '+' or desk[1][1] == desk[2][1] == desk[3][
        1] == '+' or \
            desk[1][2] == desk[2][2] == desk[3][2] == '+' or desk[1][3] == desk[2][3] == desk[3][
        3] == '+' or \
            desk[1][1] == desk[2][2] == desk[3][3] == '+' or desk[3][1] == desk[2][2] == desk[1][
        3] == '+':
        send_messages(chat_id, "Победа 1-ого игрока!")
        return 0, desk
    if desk[1][1] == desk[1][2] == desk[1][3] == '0' or desk[2][1] == desk[2][2] == desk[2][
        3] == '0' or \
            desk[3][1] == desk[3][2] == desk[3][3] == '0' or desk[1][1] == desk[2][1] == desk[3][
        1] == '0' or \
            desk[1][2] == desk[2][2] == desk[3][2] == '0' or desk[1][3] == desk[2][3] == desk[3][
        3] == '0' or \
            desk[1][1] == desk[2][2] == desk[3][3] == '0' or desk[3][1] == desk[2][2] == desk[1][
        3] == '0':
        send_messages(chat_id, "Победа 2-ого игрока!")
        return 0, desk
    return 1, desk





def share(a):
    """
    Функция для обработки числа для игры
    :param a: число для обработки
    :return: список чисел
    """
    return a // 1000, (a // 100) % 10, (a % 100) // 10, a % 10


def cow(a, b):
    """
    Задаем колнки по заданному интервалу
    :param a: размер
    :param b: размер

    """
    bull, ccow = 0, 0
    for i in range(4):
        if a[i] == b[i]:
            bull += 1
        elif a[i] in b:
            ccow += 1
    return bull, ccow


def change(res):
    global s
    q = list(map(lambda x: [cow(share(x), res), x],
                 [i for i in range(1234, 9876) if len(set(str(i))) == 4]))
    w = []
    for elem in q:
        if history(elem[1], s):
            w.append(elem)
    return min(w, key=lambda x: (x[0][0], x[0][1]))[1]

# история запроса
def history(x, ss):
    for elem in ss:
        if cow(share(x), elem[0]) != elem[1]:
            return False
    return True


# игровые переменные
knownumTrue, gorodaTrue, abirTrue, visTrue, tofTrue, bikTrue = False, False, False, False, False, False
raund, raund1, bol, i, number = 0, 0, 0, -1, 0
word_b = ''
cur_towns = []
s = []
desk = [[' ', '1', '2', '3'], ['1', '.', '.', '.'], ['2', '.', '.', '.'], ['3', '.', '.', '.']]
MAX_WRONG = 5
global num

# запрос в вк
def bik(chat_id, res, normal):
    pass

if __name__ == '':
    longpoll = VkBotLongPoll(vk, 204241258)
    for event in longpoll.listen():
        print(event.type)
        if event.type == VkBotEventType.MESSAGE_NEW: #Если появилось сообщение - обрабатываем
            if event.from_chat:
                chat_id = event.chat_id
                msg = event.object.message["text"].lower()
                bad_words = ['лень', "тоска", "уныние", "скука"]  # слова-маркеры
                if msg == "привет":
                    send_messages(chat_id,
                                  'Привет, чтобы узнать, что я могу пиши "команды"')
                try:
                    dey = event.message.action['type']
                    invite_id = event.message.action['member_id']
                except:
                    dey = ''
                    invite_id = -100
                if dey == 'chat_invite_user':
                    send_messages(chat_id, f"Приветик, {_get_user_name(chat_id, str(invite_id))}!")
                elif set(msg.split()) & set(bad_words):
                    send_messages(chat_id, 'Без плохих слов!')
                elif msg.lower() == "кто я":
                    name = _get_user_name(chat_id, str(invite_id))
                    if name == '404':
                        send_messages(chat_id, f"Я не знаю")
                    else:
                        send_messages(chat_id, f"Ты - {name}, не забывай об этом!")
                elif msg.lower().count("кто ид - "):
                    invite_id = msg.lower().split('кто ид - ')[1]
                    name = _get_user_name(chat_id, str(invite_id))
                    if name == '404':
                        send_messages(chat_id, f"Я не знаю")
                    else:
                        send_messages(chat_id, f"Это - {name}, не забывай об этом!")
                elif msg.lower().count("добавить фразу"):
                    frazes.append(msg[15:])
                    send_messages(chat_id, f'Ваша фраза - {msg[15:]} - добавлена в список')
                elif msg.lower() == "команды":
                    attachments = []
                    image = random.choice(image_urls)
                    photo = upload.photo_messages(photos=image)[0]
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                    send_messages(chat_id, koms, ','.join(attachments))
                elif msg.lower() == "грустно":
                    send_messages(chat_id, f'Все будет окей!)')
                elif msg.lower() == "весело":
                    send_messages(chat_id, f'Так держать! Полный вперед! На аборда-аж!')
                elif msg.lower() == "крестики-нолики":
                    bol = 1
                    i = 1
                    send_messages(chat_id,
                                  f"Да начнется битва! Ход игрока {1}. Введите координату типа: 1 3")
                elif bol and len(msg.lower()) == 3 and set(msg.lower()) & set('123'):
                    p = i % 2
                    if p == 0:
                        p = 2
                    c = msg
                    bol, desk = krestnul(p, desk, c)
                    i += 1
                    if bol:
                        if p == 2:
                            b = 1
                        else:
                            b = 2
                        send_messages(chat_id, f"Ход игрока {b}")
                elif msg.lower() == "угадайка":
                    send_messages(chat_id, f'Угадайка. Поехали. ВВедите число')
                    num = random.randint(1, 100)
                    raund = 1
                    knownumTrue = True
                elif knownumTrue and msg.isdigit():
                    knownumTrue, raund = know_nomber(chat_id, int(msg), num, knownumTrue, raund)
                elif msg.lower() == "прогноз":  # псевдопредсказание дня
                    attachments = []
                    image = random.choice(im_uri)
                    photo = upload.photo_messages(photos=image)[0]
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                    send_messages(chat_id, random.choice(futurum), ','.join(attachments))
                elif msg.lower() == 'картинка':
                    attachments = []
                    image = random.choice(f1)
                    photo = upload.photo_messages(photos=image)[0]
                    attachments.append('photo{}_{}'.format(photo['owner_id'], photo['id']))
                    send_messages(chat_id, '', ','.join(attachments))
                elif msg.lower() == 'фраза':
                    send_messages(chat_id, random.choice(frazes))
                elif msg.lower() == "города":
                    raund1 = 1
                    gorodaTrue = True
                    send_messages(chat_id, f'Города. Начинайте с "Город ..."')
                    cur_towns = []
                    word_b = ''
                elif msg.lower() == "виселица":
                    visTrue = True
                    send_messages(chat_id,
                                  f'Ваша задача ответить на загадку, угадывая слово по одной букве. '
                                  f'Если хотите закончить игру досрочно, напишите "сдаюсь". '
                                  f'У вас есть право на {MAX_WRONG} ошибок.'
                                  f' Чтобы ввести букву начните сообщение с "Буква "')
                    nu = random.randint(0, len(QUESTIONS) - 1)
                    send_messages(chat_id, QUESTIONS[nu])
                    wrong = 0
                    current_ans = ['-'] * len(ANWERS[nu])
                    send_messages(chat_id, '  '.join(current_ans))
                    send_messages(chat_id, 'Введите букву: ')
                elif msg.lower().count("буква ") and visTrue:
                    letter = msg.lower().split("буква ")[1]
                    visTrue = gallows(chat_id, letter)
                elif msg.lower().count("сдаюсь") and visTrue:
                    visTrue = gallows(chat_id, 'сдаюсь')
                elif msg.lower().count("сколько дней до"):
                    t_d(chat_id, msg)
                elif msg.lower() == "абырвалг":
                    abirTrue = True
                    send_messages(chat_id, f'Торобоан аволс мешип\n *ценок - конец')
                elif abirTrue:
                    abirTrue = abirgame(chat_id, msg)
                elif msg.lower() == "верю не верю":
                    tofTrue = True
                    send_messages(chat_id, f'Ваша задача угадать, правдиво ли данное высказывание')
                    number = random.randint(0, len(QUE_CARDS) - 1)
                    send_messages(chat_id, QUE_CARDS[number])
                elif tofTrue and ((msg.lower() in ans_dict) or msg.lower() == 'хватит'):
                    tofTrue, number = true_or_false(chat_id, msg.lower(), number)
                elif msg.lower().count('посчитай'):
                msg = msg.split('посчитай ')[1]
                try:
                    st = eval(msg)
                    send_messages(chat_id, f'Будет: {st}')
                except ZeroDivisionError:
                    send_messages(chat_id, f'Ошибка! Делить на 0 нельзя!')
                except TypeError:
                    send_messages(chat_id, f'Я тебя не понимаю. Не забудь про ввод цифрами')
                except SyntaxError:
                    send_messages(chat_id, f'Я тебя не понимаю. Не забудь про ввод цифрами')
                except NameError:
                    send_messages(chat_id, f'Я тебя не понимаю. Не забудь про ввод цифрами')
                elif msg.lower() == "быки и коровы":
                    bikTrue = True
                    send_messages(chat_id,
                                  f'Цель игры - угадать число из 4 разных цифр по количеству общих цифр(коров) '
                                  f'и цифр, которые находятся на нужном месте(быков)')
                    send_messages(chat_id, 'Введите четырехзначное число:')
                elif bikTrue and (len(msg) == 4 and msg.isdigit()):
                    res = share(int(msg))  # принимаем пользовательское число
                    normal = share(change(res))  # новый задуманный кортеж
                    bikTrue = bik(chat_id, res, normal)
