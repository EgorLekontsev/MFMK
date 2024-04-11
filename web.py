from flask import Flask, render_template
'''
Keypad - кейпад
Frame1 - Главный экран - 1 2 3 4 фреймы индикаторов
Menu - Настройки
Frame2 - Планировщик уставок
Frame3 - Мониторинг(Тренды онлайн)
Frame4 - Мониторинг(Тренды истории)
Frame5 - Мониторинг(Наработки насосов)
Frame6 - Журнал(Текущие события)
Frame7 - Журнал(Журнал история)
Frame8 - Журнал(Журнал изменений)
Frame9 - Настройки станции(Параметры двигателей)
Frame10 - Настройки станции(Настройки датчиков)
Frame11 - Настройки станции(Параметры насосов общ.)
Frame12 - Настройки станции(вкл. доп. насосов)
Frame13 - Настройки станции(откл. доп. насосов)
Frame14 - Настройки станции(Опции)
Frame15 - Настройки станции(Аварийные режимы)
Frame16 - Инженерное меню(Настройки ПИД-рег.)
Frame17 - Инженерное меню(PLC)
Frame18 - Инженерное меню(Бэкап)
Frame19 - Настройки панели
Frame20 - Контакты
'''

app = Flask(__name__)

@app.route('/')
def MainScreen(): #Frame 1_1 1_2 1_3 1_4
    return render_template('Main.html')

@app.route('/Monitoring')
def MonitoringScreen():#Frame3 4 5
    return render_template('Monitoring.html')

@app.route('/Journal')
def JournalScreen():#Menu Frame6 7 8
    return render_template('Journal.html')

@app.route('/OptionsStation')
def OptionsStationScreen():#Frame9 10 11 12 13 14 15
    return render_template('OptionsStation.html')

@app.route('/EngineeringMenu')
def EngineeringMenuScreen():#Frame16 17 18
    return render_template('EngineeringMenu.html')

@app.route('/Menu')
def MenuScreen():#Menu Frame2 19 20
    return render_template('Menu.html')

if __name__ == '__main__':
    app.run(debug=True)
