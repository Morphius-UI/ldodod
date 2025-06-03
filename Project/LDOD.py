import time
import telebot
from telebot import types
import pars_info


checker = False
token = '7475078721:AAHUczpsSz63r1AB736Yhz1ME5q8F7rpUhA'
bot = telebot.TeleBot(token)
students = []
adm = {}
adm_propusk = 0

pagesshop = 2
pagenow = 1



@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет')
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = types.KeyboardButton("Учитель")
    item2 = types.KeyboardButton("Ученик")
    markup.add(item1, item2)
    bot.send_message(message.chat.id, 'Кто вы?', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def cheak0(message):
    if message.text == 'Ученик':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        log = types.KeyboardButton("Войти")
        reg = types.KeyboardButton("Регистрация")
        back = types.KeyboardButton('Назад')
        markup.add(log, reg, back)
        bot.send_message(message.chat.id, 'Вход/регистрация', reply_markup=markup)
        bot.register_next_step_handler(message, child)

    if message.text == 'Учитель':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        back = types.KeyboardButton('Назад')
        markup.add(back)
        bot.send_message(message.chat.id, 'Логин:', reply_markup=markup)
        bot.register_next_step_handler(message, cheak1)

    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Учитель")
        item2 = types.KeyboardButton("Ученик")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, 'Кто вы?', reply_markup=markup)




def cheak1(message):
    string = pars_info.pars_admin_panel(Log=message.text)
    print(string)
    gan = True
    while gan == True:
        if message.text == 'Назад':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton("Учитель")
            item2 = types.KeyboardButton("Ученик")
            markup.add(item1, item2)
            bot.send_message(message.chat.id, 'Кто вы?', reply_markup=markup)
            gan = False
            break

        if message.text != string or string == None:
            bot.send_message(message.chat.id, 'Логин неверный')
            bot.register_next_step_handler(message, cheak1)
            break

        else:
            gan = False
            bot.register_next_step_handler(message, admin_base_login)
            bot.send_message(message.chat.id, 'Введите пароль')

def admin_base_login(message):
    global adm_propusk
    gan = True
    pas = pars_info.pars_admin_panel(pas=message.text)
    while gan == True:
        if pas != message.text:
            bot.send_message(message.chat.id, 'Пароль неверный')
            bot.register_next_step_handler(message, admin_base_login)
            break
        else:
            gan = False
            bot.send_message(message.chat.id, 'Добро пожаловать, admin!')
            adm_propusk = 1
            print('Вход выполнен, admin, ' + str(message.chat.id))
            admin_panel(message, k=1)

def admin_panel(message, k=None):
    if adm_propusk == 1:
        markup = types.InlineKeyboardMarkup()
        magaz = types.InlineKeyboardButton("Список учеников", callback_data="spisok")
        markup.add(magaz)
        if k == 0:
            bot.edit_message_text('<b>Панель админа</b>', parse_mode='HTML', chat_id=message.chat.id, message_id=message.id, reply_markup=markup)
        else:
            bot.send_message(message.chat.id, '<b>Панель админа</b>', parse_mode='HTML', reply_markup=markup)






def child(message):
    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Учитель")
        item2 = types.KeyboardButton("Ученик")
        markup.add(item1, item2)
        bot.send_message(message.chat.id, 'Кто вы?', reply_markup=markup)
        bot.register_next_step_handler(message, cheak0)
    if message.text == 'Войти':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Назад")
        markup.add(item1)
        bot.send_message(message.chat.id, '<b>Введите логин:</b>\n', reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(message, auth_login)
    if message.text== "Регистрация":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Назад")
        markup.add(item1)
        bot.send_message(message.chat.id, 'Введите ваш логин, <b>как в электронном дневнике</b>', reply_markup=markup, parse_mode="HTML")
        bot.register_next_step_handler(message, register_child_login)


def auth_login(message):
    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Войти")
        item2 = types.KeyboardButton("Регистрация")
        item3 = types.KeyboardButton("Назад")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Вход/регистрация', reply_markup=markup)
        bot.register_next_step_handler(message, child)
    else:
        try:
            login = message.text
            login_cheak = pars_info.pars_users(login=login)
            reg_cheak = pars_info.pars_users(register=login)
            if reg_cheak != None:
                if login_cheak == login:
                    time.sleep(3)
                    bot.send_message(message.chat.id, 'Введите <b>пароль</b>', parse_mode="HTML")
                    bot.register_next_step_handler(message, auth_password)
                else:
                    bot.send_message(message.chat.id, 'Неверный <b>логин</b>, пожалуйста попробуйте еще раз!', parse_mode='HTML')
                    bot.register_next_step_handler(message, auth_login)
            else:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item2 = types.KeyboardButton("Регистрация")
                markup.add(item2)
                bot.send_message(message.chat.id, 'Вы не зарегистрированы, для начала пройдите регистрацию!', reply_markup=markup)
                bot.register_next_step_handler(message, child)


        except:
            bot.send_message(message.chat.id, 'Неправильный формат, попробуйте еще раз')
            bot.register_next_step_handler(message, auth_login)  # , startapp

def auth_password(message):
    try:
        password = message.text
        pas_cheak = pars_info.pars_users(password=password)
        if pas_cheak == str(password):
            rep = bot.send_message(message.chat.id, '<b>Идентификация</b>', parse_mode='HTML')
            tochka = ''
            for i in range(6):
                time.sleep(1)
                tochka += '.'
                bot.edit_message_text(chat_id=message.chat.id, message_id=rep.message_id, text=f'<b>{rep.text}{tochka}</b>', parse_mode='HTML')
                if tochka == '...':
                    tochka = ''
            bot.delete_message(message.chat.id, rep.id)
            menu(message)
        else:
            bot.send_message(message.chat.id, '<b>Неверный пароль, повторите!</b>', parse_mode='HTML')
            bot.register_next_step_handler(message, auth_password)
    except:
        pass
        


def register_child_login(message):
    if message.text == 'Назад':
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 = types.KeyboardButton("Войти")
        item2 = types.KeyboardButton("Регистрация")
        item3 = types.KeyboardButton("Назад")
        markup.add(item1, item2, item3)
        bot.send_message(message.chat.id, 'Вход/регистрация', reply_markup=markup)
        bot.register_next_step_handler(message, child)
    else:
        try:
            global login
            login = message.text
            log_cheak = pars_info.pars_users(login=login)
            log_tr = pars_info.truth(login)
            if log_cheak == None and log_tr != None:
                bot.send_message(message.chat.id, '<b>Введите пароль для своей учетной записи</b>', parse_mode="HTML")
                print(login)
                bot.register_next_step_handler(message, register_child_password)
            elif log_cheak != None:
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item2 = types.KeyboardButton("Войти")
                markup.add(item2)
                bot.send_message(message.chat.id, 'Вы уже зарегистрированы, войдите в систему!', reply_markup=markup)
                bot.register_next_step_handler(message, child)
            elif log_tr == None:
                bot.send_message(message.chat.id, 'Такого пользователя нет в базе данных!')
                bot.register_next_step_handler(message, register_child_login)

        except:
            bot.send_message(message.chat.id, 'Неправильный формат, попробуйте еще раз')
            bot.register_next_step_handler(message, register_child_login)  # , startapp

def register_child_password(message):
    try:
        pas = message.text
        pars_info.register(message, login, password=pas)
        markup = types.InlineKeyboardMarkup()
        access = types.InlineKeyboardButton(text="✅", callback_data='access')
        not_access = types.InlineKeyboardButton(text="❌", callback_data='no_access')
        markup.add(access, not_access)
        bot.send_message(message.chat.id, '<b>Вы уверены?</b>', parse_mode='HTML', reply_markup=markup)
    except:
        pass


def menu(message=None):
    global pagenow
    global pagesshop
    markup = types.InlineKeyboardMarkup()
    magaz = types.InlineKeyboardButton("💼Магазин", callback_data="magaz")
    minigame = types.InlineKeyboardButton("⚽️Мини-игры", callback_data="minigame")
    score = types.InlineKeyboardButton("🎖Мой профиль", callback_data="score")
    markup.add(magaz, minigame, score)
    print(message)
    bot.send_message(message.chat.id,f"<b>Добро пожаловать в Ldod score, @{message.chat.username}!😁</b>\nЗдесь вы можете получить награды за хорошие отметки..\nЗа каждую четвертную отметку вы получаете очки, которые вы можете потратить на призы в разделе <b>'Магазин'</b>😌\nТакже вы получаете возможность самостоятельно накопить на данные награды с помощью раздела 'Мини-игры'..\nИграйте, развивайтесь и получайте призы😎", reply_markup=markup, parse_mode='HTML')
    bot.register_next_step_handler(message, answermenu)

@bot.callback_query_handler(func=lambda call: True)
def answermenu(call):
    _id = {1 : 30000, 2 : 100000, 3 : 10000, 4 : 5000}
    _type_id = {1 : 'Фирменная кружка Ldod Score', 2: 'Фирменная футболка Ldod Score', 3: 'Значок Ldod Score', 4 : 'Фирменная ручка'}
    global pagesshop, magaz
    global pagenow
    global chat_id
    global message_id
    global pagenow1
    global _all_spis
    global price
    global userId
    message_id = call.message.message_id
    price = 0
    chat_id = call.message.chat.id
    if call.data == 'magaz':
        pagenow = 1
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text="Назад в меню", callback_data='back')
        t1 = types.InlineKeyboardButton(text="Товар", callback_data='t1')
        markup.add(back, t1)
        textmagaz = 'Добро пожаловать в магазин💼\nЗдесь вы можете преобрести товары за ваши поинты.\nВаши поинты:' #+ points
        bot.edit_message_text(textmagaz, reply_markup = markup, chat_id=call.message.chat.id, message_id=call.message.message_id)

    if call.data == 'back':
        pagenow = 1
        bot.delete_message(call.message.chat.id, call.message.id)
        menu(call.message)

    if call.data == "t1":
        bot.delete_message(chat_id, call.message.id)
        pagenow = 1
        def magaz(photo=None, caption=None):
            markup = types.InlineKeyboardMarkup()
            buy = types.InlineKeyboardButton(text="Купить", callback_data='buy')
            back = types.InlineKeyboardButton(text="Назад в меню", callback_data='back')
            nextpage = types.InlineKeyboardButton(text="➡️", callback_data='nextpage')
            if pagenow == 1:
                markup.add(buy, nextpage, back)
                photo = open('ldodod/Project/kryzka.jpg', 'rb')
                caption = '<b>Фирменная кружка Ldod Score</b>\n\nЦена: <b>30000 поинтов.</b>'
                price = 30000
            elif pagenow == 4:
                backpage = types.InlineKeyboardButton(text="⬅️", callback_data='backpage')
                markup.add(buy, backpage, back)
            else:
                backpage = types.InlineKeyboardButton(text="⬅️", callback_data='backpage')
                markup.add(buy, backpage, nextpage ,back)
            bot.send_photo(chat_id=chat_id, photo=photo, caption=caption, parse_mode='HTML', reply_markup=markup)
        magaz()

    if call.data == 'buy':
        name = _type_id[pagenow]
        price = _id[pagenow]
        _log = pars_info.pars_users(_login=chat_id)
        _point = pars_info.pars_users(points=_log)
        if _point >= price:
            markup = types.InlineKeyboardMarkup()
            accept = types.InlineKeyboardButton(text="✅", callback_data='buy1')
            disaccept = types.InlineKeyboardButton(text="❌", callback_data='disbuy')
            markup.add(accept, disaccept)
            bot.delete_message(call.message.chat.id, call.message.id)
            bot.send_message(chat_id=chat_id, text=f'<b>Вы уверены в покупке</b>\n{name}\nЦена: {price}', reply_markup=markup, parse_mode="HTML")
        else:
            bot.answer_callback_query(callback_query_id=call.id, text='Не хватает поинтов на балансе ❌')

    if call.data == 'buy1':
        price = _id[pagenow]
        pars_info.buy_user(chat_id, price)
        name = _type_id[pagenow]
        UsrInfo = bot.get_chat_member(chat_id, chat_id).user.username
        bot.send_message(1362364051, f'@{UsrInfo} купил {name}\nid={chat_id}')
        bot.send_message(chat_id, '<b>Успешно✅</b>\n\nВаш запрос отправлен администратору, свяжемся в ближайшее время!', parse_mode='HTML')
        time.sleep(6)
        cap = 'Вернуться назад?'
        markup = types.InlineKeyboardMarkup()
        accept = types.InlineKeyboardButton(text="Назад", callback_data='back')
        markup.add(accept)
        bot.edit_message_text(cap ,chat_id, message_id, reply_markup=markup)



    if call.data == "nextpage":
        pagenow+=1
        if pagenow == 2:
            photo = open('ldodod/Project/t-shirt.jpg', 'rb')
            caption = '<b>Фирменная футболка Ldod Score</b>\n\nЦена: <b>100000 поинтов.</b>'
            bot.delete_message(call.message.chat.id, call.message.id)
            price = 100000
            magaz(photo, caption)
        elif pagenow == 3:
            photo = open('ldodod/Project/znachok.jpg', 'rb')
            caption = '<b>Значок Ldod Score</b>\n\nЦена: <b>10000 поинтов.</b>'
            bot.delete_message(call.message.chat.id, call.message.id)
            price = 10000
            magaz(photo, caption)
        elif pagenow == 4:
            photo = open('ldodod/Project/rushka.png', 'rb')
            caption = '<b>Фирменная ручка</b>\n\nЦена: <b>5000 поинтов.</b>'
            bot.delete_message(call.message.chat.id, call.message.id)
            price = 5000
            magaz(photo, caption)
        elif pagenow == 5:
            photo = open('ldodod/Project/aluonka.png', 'rb')
            caption = '<b>Шоколадка "Аленка"</b>\n\nЦена: <b>10000 поинтов.</b>'
            bot.delete_message(call.message.chat.id, call.message.id)
            price = 10000
            magaz(photo, caption)
    if call.data == "backpage":
        pagenow -= 1
        if pagenow == 1:
            bot.delete_message(call.message.chat.id, call.message.id)
            magaz()
        elif pagenow == 2:
            photo = open('ldodod/Project/t-shirt.jpg', 'rb')
            caption = '<b>Фирменная футболка Ldod Score</b>\n\nЦена: <b>100000 поинтов.</b>'
            bot.delete_message(call.message.chat.id, call.message.id)
            price = 100000
            magaz(photo, caption)
        elif pagenow == 3:
            photo = open('ldodod/Project/znachok.jpg', 'rb')
            caption = '<b>Значок Ldod Score</b>\n\nЦена: <b>10000 поинтов.</b>'
            bot.delete_message(call.message.chat.id, call.message.id)
            price = 10000
            magaz(photo, caption)
        elif pagenow == 4:
            photo = open('ldodod/Project/rushka.png', 'rb')
            caption = '<b>Значок Ldod Score</b>\n\nЦена: <b>5000 поинтов.</b>'
            bot.delete_message(call.message.chat.id, call.message.id)
            price = 5000
            magaz(photo, caption)
        elif pagenow == 5:
            photo = open('ldodod/Project/aluonka.png', 'rb')
            caption = '<b>Шоколадка "Аленка"</b>\n\nЦена: <b>10000 поинтов.</b>'
            bot.delete_message(call.message.chat.id, call.message.id)
            price = 10000
            magaz(photo, caption)

    if call.data == 'minigame':
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text="Назад в меню", callback_data='back')
        g1 = types.InlineKeyboardButton(text="Крестики нолики", callback_data='g12')
        g2 = types.InlineKeyboardButton(text="4 в ряд", callback_data='g2')
        g3 = types.InlineKeyboardButton(text="Морской бой", callback_data='g3')
        markup.add(g1, g2, g3, back)
        textminigame = 'Добро пожаловать в магазин💼\nЗдесь вы можете преобрести товары за ваши поинты.\nВаши поинты:'  # + points
        bot.edit_message_text(textminigame, reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id)

    if call.data == 'g12':
        bot.answer_callback_query(callback_query_id=call.id, text='Ошибка. Попробуйте позже.')
    if call.data == 'g2':
        bot.answer_callback_query(callback_query_id=call.id, text='Ошибка. Попробуйте позже.')
    if call.data == 'g3':
        bot.answer_callback_query(callback_query_id=call.id, text='Ошибка. Попробуйте позже.')


    if call.data == 'g1':
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text="Назад в меню", callback_data='back')
        lvl1 = types.InlineKeyboardButton(text="Легкий", callback_data='lvl1')
        lvl2 = types.InlineKeyboardButton(text="Средний", callback_data='lvl2')
        lvl3 = types.InlineKeyboardButton(text="Тяжелый", callback_data='lvl3')
        lvl4 = types.InlineKeyboardButton(text="Невозможный", callback_data='lvl4')
        markup.add(lvl1, lvl2, lvl3, lvl4, back)
        bot.edit_message_text("<b>🎓ИГРА КРЕСТИКИ НОЛИКИ🎓</b>\nПравила: вы играете с искусственным интеллектом, ваша задача обыграть его😁\nВ случае победы вы получаете"
                              "ваши токены + к этому награда за игру\n<b>Играть вы можете всего 5 раз в день</b>\n\n<b>Легкий</b>\nВзнос на игру:10токенов\nВозможный выйгрыш:10 токенов\n"
                              "\n<b>Средний</b>\nВзнос на игру:15токенов\nВозможный выйгрыш:15 токенов\n"
                              "\n<b>Тяжелый</b>\nВзнос на игру:20токенов\nВозможный выйгрыш:20 токенов\n"
                              "\n<b>Невозможный</b>\nВзнос на игру:40токенов\nВозможный выйгрыш:99999 токенов", reply_markup=markup, chat_id=chat_id, message_id=message_id, parse_mode='HTML')
    if call.data == 'score':
        _time = pars_info.pars_users(_time=chat_id)
        _log = pars_info.pars_users(_login=chat_id)
        _klass = pars_info.pars_users(klass=_log)
        _point = pars_info.pars_users(points=_log)
        timeda = time.strftime("%d %b %Y ", time.localtime(_time))
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text="Назад в меню", callback_data='back')
        cheaktruth = types.InlineKeyboardButton(text="Проверить вычисления ваших поинтов", callback_data='cheaktruth')
        markup.add(cheaktruth, back)
        profile = f'<b>Ваш профиль</b>\n\nДата регистрации: <b>{timeda}</b>\n\nВаш логин: <b>{_log}</b>\n\nВаш класс: <b>{_klass}</b>\n\nВаши поинты: <b>{_point}</b>'  # + points
        bot.edit_message_text(profile, reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML")

    def page():
        usr, point = pars_info.admin_spisok()
        itog = f'<b>Страница {pagenow1}</b>\n'
        markup = types.InlineKeyboardMarkup()
        back = types.InlineKeyboardButton(text="Назад", callback_data='back1')
        nextpage = types.InlineKeyboardButton(text="➡️", callback_data='nextpage1')
        if len(usr) > pagenow1*10:
            if pagenow1 == 1:
                markup.row(back, nextpage)
                for i in range(10):
                    itog += f'@{bot.get_chat_member(call.message.chat.id, usr[i]).user.username} - {point[i]}\n'
                bot.edit_message_text(itog, reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML")
            else:
                backpage = types.InlineKeyboardButton(text="⬅️", callback_data='backpage1')
                markup.row(backpage, nextpage, back)
                for i in range((pagenow1 * 10 - 10), (pagenow1 * 10)-1):
                    try:
                        if usr[i] != None:
                            itog += f'@{bot.get_chat_member(call.message.chat.id, usr[i]).user.username} - {point[i]}\n'
                    except:
                        _all_spis = True
                        pass
                bot.edit_message_text(itog, reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML")
        else:
            if pagenow1 <= 1:
                markup.row(back)
                try:
                    for i in range(10):
                        itog += f'@{bot.get_chat_member(call.message.chat.id, usr[i]).user.username} - {point[i]}\n'
                        bot.edit_message_text(itog, reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML")
                except:
                    bot.edit_message_text(itog, reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML")
            else:
                backpage = types.InlineKeyboardButton(text="⬅️", callback_data='backpage1')
                markup.row(backpage, back)
                for i in range((pagenow1 * 10 - 10), (pagenow1 * 10)-1):
                    try:
                        if usr[i] != None:
                            itog += f'@{bot.get_chat_member(call.message.chat.id, usr[i]).user.username} - {point[i]}\n'
                    except:
                        _all_spis = True
                        pass
                bot.edit_message_text(itog, reply_markup=markup, chat_id=call.message.chat.id, message_id=call.message.message_id, parse_mode="HTML")
    if call.data == 'spisok':
        print(124124)
        pagenow1 = 1
        page()
    if call.data == 'back1':
        pagenow1 = 1
        print(pagenow1)
        admin_panel(call.message, k=0)
    if call.data == 'nextpage1':
        pagenow1 += 1
        print(pagenow1)
        page()
    if call.data == 'backpage1':
        pagenow1 = pagenow1 - 1
        print(pagenow1)
        page()

    if call.data == 'cheaktruth':
        bot.answer_callback_query(callback_query_id=call.id, text='Все в норме!')
    if call.data == 'access':
        menu(call.message)
    if call.data == 'no_access':
        pars_info.deregister(call.message)
        bot.edit_message_text('<b>Введите пароль еще раз</b>', chat_id, call.message.id, parse_mode='HTML')
        bot.register_next_step_handler(call.message, register_child_password)



bot.infinity_polling()

