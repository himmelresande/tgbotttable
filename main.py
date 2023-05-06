import telebot
import psycopg2
import datetime
from telebot import types
from datetime import date

conn = psycopg2.connect(database="timestable3_db",
                        user="postgres",
                        password="8090",
                        host="localhost",
                        port="5432")
cursor = conn.cursor()
psql_select_timetable1 = "select day, string_agg(table_column, '\n\n') as table_row from (select day, timetable_week1.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from timetable_week1, teacher where teacher.subject = timetable_week1.subject order by start_time)timetable_week1 group by 1 order by case when day = 'Monday' then 1 when day = 'Tuesday' then 2 when day = 'Wednesday' then 3 when day = 'Thursday' then 4 else 5 end;"
psql_select_timetable2 = "select day, string_agg(table_column, '\n\n') as table_row from (select day, timetable_week2.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from timetable_week2, teacher where teacher.subject = timetable_week2.subject order by start_time)timetable_week2 group by 1 order by case when day = 'Monday' then 1 when day = 'Tuesday' then 2 when day = 'Wednesday' then 3 when day = 'Thursday' then 4 else 5 end;"


today = date.today()
num = int(today.isocalendar().week)
if (num % 2) == 0:
   this_week = "timetable_week2"
else:
   this_week = "timetable_week1"

if this_week == "timetable_week2":
    show_this_week = psql_select_timetable2
    show_next_week = psql_select_timetable1
else:
    show_this_week = psql_select_timetable1
    show_next_week = psql_select_timetable2

# store tgbot token
token = '5652162259:AAE5tmpX2CmyY7MLylugB5AZxFXoRuJOyyI'
bot = telebot.TeleBot(token)


# decorator for /start
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row('/mtuci')
    keyboard.row('/week')
    keyboard.row('/this_week', '/next_week')
    keyboard.row('monday')
    keyboard.row('tuesday')
    keyboard.row('wednesday')
    keyboard.row('thursday')
    keyboard.row('friday')
    bot.send_message(message.chat.id,
                     'Здравствуйте! Хотите узнать свежую информацию из МТУСИ? Нажмите /help чтобы увидеть команды бота',
                     reply_markup=keyboard)


# decorator for /help
@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     'Бот может показать вам ваше расписание если вы отправите день недели. \nВы можете управлять ботом этими командами: \n/mtuci - официальный сайт МТУСИ\n/week - показывает какая сейчас неделя\n/this_week - показывает Вам расписание на эту неделю\n/next_week - показывает Вам расписание на следующую неделю')


# decorator for /mtuci
@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, 'Перейдите по ссылке для информации - https://mtuci.ru/')


# decorator for /week
@bot.message_handler(commands=['week'])
def start_message(message):
    if this_week == 'timetable_week1':
        bot.send_message(message.chat.id, 'Сейчас четная неделя')
    else:
        bot.send_message(message.chat.id, 'Сейчас нечетная неделя')


# decorator for this week
@bot.message_handler(commands=['this_week'])
def start_message(message):
    cursor.execute(show_this_week)
    tb1_records = cursor.fetchall()
    for row in tb1_records:
        w1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
        bot.send_message(message.chat.id, w1_display)


# decorator for next week
@bot.message_handler(commands=['next_week'])
def start_message(message):
    cursor.execute(show_next_week)
    tb2_records = cursor.fetchall()
    for row in tb2_records:
        w2_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
        bot.send_message(message.chat.id, w2_display)


# decorator for monday
@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == 'monday':
        cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, {}.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from {}, teacher where day ='Monday' and teacher.subject = {}.subject order by start_time) {} group by 1;".format(
                this_week, this_week, this_week, this_week))
        tb1_records = cursor.fetchall()
        for row in tb1_records:
            m1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
            bot.send_message(message.chat.id, m1_display)
    elif message.text.lower() == 'tuesday':
        cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, {}.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from {}, teacher where day ='Tuesday' and teacher.subject = {}.subject order by start_time) {} group by 1;".format(
                this_week, this_week, this_week, this_week))
        tb1_records = cursor.fetchall()
        for row in tb1_records:
            m1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
            bot.send_message(message.chat.id, m1_display)
    elif message.text.lower() == 'wednesday':
        cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, {}.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from {}, teacher where day ='Wednesday' and teacher.subject = {}.subject order by start_time) {} group by 1;".format(
                this_week, this_week, this_week, this_week))
        tb1_records = cursor.fetchall()
        for row in tb1_records:
            m1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
            bot.send_message(message.chat.id, m1_display)
    elif message.text.lower() == 'thursday':
        cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, {}.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from {}, teacher where day ='Thursday' and teacher.subject = {}.subject order by start_time) {} group by 1;".format(
                this_week, this_week, this_week, this_week))
        tb1_records = cursor.fetchall()
        for row in tb1_records:
            m1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
            bot.send_message(message.chat.id, m1_display)
    elif message.text.lower() == 'friday':
        cursor.execute(
            "select day, string_agg(table_column, '\n\n') as table_row from (select day, {}.subject ||' | '|| room_numb ||' | '|| start_time ||'-'|| finish_time ||' | '|| full_name as table_column from {}, teacher where day ='Friday' and teacher.subject = {}.subject order by start_time) {} group by 1;".format(
                this_week, this_week, this_week, this_week))
        tb1_records = cursor.fetchall()
        for row in tb1_records:
            m1_display = '{}\n___________________\n{} \n___________________'.format(row[0], row[1])
            bot.send_message(message.chat.id, m1_display)
    elif message.text.lower() != '':
        bot.send_message(message.chat.id,
                         'Извините, такой команды нет')


bot.polling()