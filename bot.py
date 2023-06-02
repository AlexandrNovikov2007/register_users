import sqlite3 as sq
from aiogram import types, Bot, Dispatcher, executor
from keyboards.keyboard import kb_client, kb_cl,nasad, kb_client_for_help, location
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup 
from aiogram.contrib.fsm_storage.memory import MemoryStorage 
import random   
import smtplib  
from platform import python_version  
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from gtts import gTTS
import os
import sqlite3
from geopy.geocoders import Nominatim
TOKEN="6288263212:AAEJsrQf-cXjFAUhurfg-zEGy_thoiQuV3o"

mas, dostup, confirmation , b, a=[], [], [], [], []
class FSMchat(StatesGroup):
    login=State()
    password=State()
    confirmation=State()
    
class FSMentrance(StatesGroup):
    login=State()
    password=State()
    
class FSMhelp_password(StatesGroup):
    login=State()
    confirmation=State()
    new_password=State()
    
    

bot=Bot(TOKEN)
storage=MemoryStorage()
dp=Dispatcher(bot, storage=storage)

@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    await message.answer(f"Привет {message.from_user.full_name}", reply_markup=kb_client)
    await message.answer('Для того чтобы пользоваться услугами бота пройдите регистрацию')
    await message.answer('Если у вас в течение сессии возникнут проблемы, напишите нашему менеджеру')
    await message.answer('https://t.me/evloevw06')
    
@dp.message_handler(commands=["Забыли_пароль"], state=None)
async def help_password(message: types.Message):
    await FSMhelp_password.login.set()
    await message.answer('Введите свою электронную почту', reply_markup=nasad)  

@dp.message_handler(state=FSMhelp_password.login)
async def load_login_for_help_password(message: types.Message, state: FSMContext):
    if message.text=='назад':
        await state.finish()
        await message.answer('Если у вас в течение сессии возникнут проблемы, напишите нашему менеджеру', reply_markup=kb_client)
        await message.answer('https://t.me/evloevw06')
    else:      
        login=message.text
        await state.update_data({'login': login})
        await FSMhelp_password.next()
        await message.answer('На вашу почту пришел код с подтверждением, пожалуйста введите его')
        server='smtp.mail.ru'
        mi_login='batareya74235@mail.ru'
        mi_password='d789vzDpaQKUVradj2na'
        recipients=[login]
        sender='batareya74235@mail.ru'
        subject='Подтверждение'
        text=str(random.randint(100000, 999999))
        a.append(text)
        msg=MIMEMultipart('alternative')
        msg['Subject']=subject
        msg['From']='Python script <'+ sender +'>'
        msg['To']=', '.join(recipients)
        msg['Reply-To']=sender
        msg['Return-Path']=sender
        msg['X-Mailer']='Python/' + (python_version())
        part_text=MIMEText(text, 'plain')
        msg.attach(part_text)
        mail= smtplib.SMTP_SSL(server)
        mail.login(mi_login, mi_password)
        mail.sendmail(sender, recipients, msg.as_string())
        mail.quit
        recipients.clear()
    
@dp.message_handler(state=FSMhelp_password.confirmation)
async def confirmation_for_help_password(message: types.Message, state: FSMContext):
    if message.text=='назад':
        await state.finish()
        await message.answer('Если у вас в течение сессии возникнут проблемы, напишите нашему менеджеру', reply_markup=kb_client)
        await message.answer('https://t.me/evloevw06')
    else:
        kod=message.text   
        if kod==a[0]:
            await message.answer('Введите новый пароль')
            await FSMhelp_password.next()
            a.clear()
    

@dp.message_handler(state=FSMhelp_password.new_password)
async def new_password(message: types.Message, state: FSMContext):
    if message.text=='назад':
        await state.finish()
        await message.answer('Если у вас в течение сессии возникнут проблемы, напишите нашему менеджеру', reply_markup=kb_client)
        await message.answer('https://t.me/evloevw06')
    else:
        new_password=message.text
        user_id=message.from_user.id
        with sq.connect("users.db") as con:
            cur=con.cursor()
            dan=cur.execute("SELECT password FROM users WHERE user_id=(?)", (user_id,))
            for row in dan:
                for q in row:
                    b.append(q)
                    if b[0]!=new_password:
                        dan=cur.execute("UPDATE users SET password=(?) WHERE password=(?)", (new_password, b[0],))
                        await message.answer('Ваш пароль успешно изменён')
                    else:
                        await message.answer('Ваш пароль сходный с предыдущим')
                    b.clear()
                    await state.finish()
        
@dp.message_handler(commands=["Вход"], state=None)
async def entrance(message: types.Message):
    await FSMentrance.login.set()
    await message.answer('Введите свою электронную почту', reply_markup=kb_client_for_help)
    
@dp.message_handler(state=FSMentrance.login)
async def load_login(message: types.Message, state: FSMContext):
    if message.text=='назад':
        await state.finish()
        await message.answer('Если у вас в течение сессии возникнут проблемы, напишите нашему менеджеру', reply_markup=kb_client)
        await message.answer('https://t.me/evloevw06')
    else:
        login=message.text
        await state.update_data({'login': login})
        await FSMentrance.next()
        await message.answer('Введите пароль')
        
@dp.message_handler(state=FSMentrance.password)
async def load_password(message: types.Message, state: FSMContext):
    if message.text=='назад':
        await state.finish()
        await message.answer('Если у вас в течение сессии возникнут проблемы, напишите нашему менеджеру', reply_markup=kb_client)
        await message.answer('https://t.me/evloevw06')
    else:
        password_from_user=message.text
        data=await state.get_data()
        login_from_user=data.get('login')
        user_id=message.from_user.id
        with sq.connect("users.db") as con:
            cur=con.cursor()
            dan=cur.execute("SELECT login, password FROM users WHERE user_id=(?)", (user_id,))
            for row in dan:
                for i in row:
                    mas.append(i)
        if password_from_user==mas[1] and login_from_user==mas[0]:
            dostup.append('YES')
            await message.answer('Добро пожаловать', reply_markup=location)
            await message.answer('введите текст который необходимо озвучить')
        else:
            await message.answer('Неправильный логин или пороль, попробуйте заново, нажав кнопочку ввойти')
        await state.finish()
        mas.clear()
    
@dp.message_handler(commands=["Зарегистрироваться"], state=None)
async def start_register(message: types.Message):
    await FSMchat.login.set()
    await message.answer('Введите свою электронную почту', reply_markup=nasad)
      
@dp.message_handler(state=FSMchat.login)
async def load_login(message: types.Message, state: FSMContext):
    if message.text=='назад':
        await state.finish()
        await message.answer('Если у вас в течение сессии возникнут проблемы, напишите нашему менеджеру', reply_markup=kb_client)
        await message.answer('https://t.me/evloevw06')
    else:
        if '@' in message.text:
            login=message.text
            await state.update_data({'login': login})
            await FSMchat.next()
            await message.answer('Придумайте пароль для своего аккаунта')
        else:
            await message.answer('Введите корректную почту, содержащую "@"')
        
    
@dp.message_handler(state=FSMchat.password)
async def load_password(message: types.Message, state: FSMContext):
    if message.text=='назад':
        await state.finish()
        await message.answer('Если у вас в течение сессии возникнут проблемы, напишите нашему менеджеру', reply_markup=kb_client)
        await message.answer('https://t.me/evloevw06')
    else:
        data=await state.get_data()
        login=data.get('login')
        password=message.text
        await state.update_data({'password': password,'login': login})
        await FSMchat.next()
        await message.answer('На вашу почту пришел код с подтверждением, пожалуйста введите его')
        server='smtp.mail.ru'
        mi_login='batareya74235@mail.ru'
        mi_password='d789vzDpaQKUVradj2na'
        recipients=[login]
        sender='batareya74235@mail.ru'
        subject='Подтверждение'
        text=str(random.randint(100000, 999999))
        confirmation.append(text)
        msg=MIMEMultipart('alternative')
        msg['Subject']=subject
        msg['From']='Python script <'+ sender +'>'
        msg['To']=', '.join(recipients)
        msg['Reply-To']=sender
        msg['Return-Path']=sender
        msg['X-Mailer']='Python/' + (python_version())
        part_text=MIMEText(text, 'plain')
        msg.attach(part_text)
        mail= smtplib.SMTP_SSL(server)
        mail.login(mi_login, mi_password)
        mail.sendmail(sender, recipients, msg.as_string())
        mail.quit
        recipients.clear()
    
   
    
@dp.message_handler(state=FSMchat.confirmation)
async def load_password(message: types.Message, state: FSMContext):
    if message.text=='назад':
        await state.finish()
        await message.answer('Если у вас в течение сессии возникнут проблемы, напишите нашему менеджеру', reply_markup=kb_client)
        await message.answer('https://t.me/evloevw06')
    else:
        kod=message.text    
        data=await state.get_data()
        login=data.get('login')
        password=data.get('password')
        
        name_user=message.from_user.full_name
        user_id=message.from_user.id
        if kod==confirmation[0]:
            with sq.connect("users.db") as con:
                cur=con.cursor()
                try:
                    cur.execute('INSERT INTO users (user_id, name_user, login, password) VALUES(?, ?, ?, ?)', (user_id, name_user, login, password,)) 
                    await message.answer('Спасибо вы успешно прошли регистрацию, войдите в систему и вам станет доступна функция озвучки текста', reply_markup=kb_cl)
                except sqlite3.IntegrityError:
                    await message.answer('Вы уже зарегистрированы в системе, нажмите на кнопку ввойти и войдите в систему')
            await state.finish()
            confirmation.clear()
 

       
@dp.message_handler(content_types=['text'])
async def vver(message: types.Message):
    if  dostup[0]=='YES':
        chat_id=message.from_user.id
        f = open('abc.txt','w', encoding='utf8')
        f.write(message.text)
        f.close()
        txt=open('abc.txt', 'r', encoding='utf8').read()
        audio = gTTS(text=txt, lang='ru', slow=False)
        audio.save("output.wav")
        await bot.send_audio(message.from_user.id, open("output.wav", "rb"))
        os.remove("output.wav") 
    
@dp.message_handler(content_types=['location'])
async def location_for_user(message : types.Message):
    geolocator = Nominatim(user_agent = "name_of_your_app")
    location = geolocator.reverse('{} {}'.format(message.location.latitude, message.location.longitude))
    await message.answer(location.address)
    
if __name__=="__main__":
    executor.start_polling(dp, skip_updates=True)