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
    return render_template('DirectMenu/Main.html')

@app.route('/SetpointPlanner')
def SetpointPlannerScreen(): #Frame 2
    return render_template('DirectMenu/SetpointPlanner.html')

@app.route('/Monitoring')
def MonitoringScreen():#Frame3 4 5
    return render_template('DirectMenu/Monitoring.html')

@app.route('/OnlineTrends')
def OnlineTrendsScreen():#Frame3 4 5
    return render_template('DirectMonitoring/OnlineTrends.html')

@app.route('/HistoryTrends')
def HistoryTrendsScreen():#Frame3 4 5
    return render_template('DirectMonitoring/HistoryTrends.html')

@app.route('/PumpOperatingTime')
def PumpOperatingTimeScreen():#Frame3 4 5
    return render_template('DirectMonitoring/PumpOperatingTime.html')

@app.route('/Journal')
def JournalScreen():#Menu Frame6 7 8
    return render_template('DirectMenu/Journal.html')

@app.route('/CurrentEvent')
def CurrentEventScreen():#Menu Frame6 7 8
    return render_template('DirectJournal/CurrentEvent.html')

@app.route('/JournalHistory')
def JournalHistoryScreen():#Menu Frame6 7 8
    return render_template('DirectJournal/JournalHistory.html')

@app.route('/ChangeLog')
def ChangeLogScreen():#Menu Frame6 7 8
    return render_template('DirectJournal/ChangeLog.html')

@app.route('/OptionsStation')
def OptionsStationScreen():#Frame9 10 11 12 13 14 15
    return render_template('DirectMenu/OptionsStation.html')

@app.route('/EngineParameters')
def EngineParametersScreen():#Frame9 10 11 12 13 14 15
    return render_template('DirectOptionsStation/EngineParameters.html')

@app.route('/SensorSettings')
def SensorSettingsScreen():#Frame9 10 11 12 13 14 15
    return render_template('DirectOptionsStation/SensorSettings.html')

@app.route('/PumpParametersInGeneral')
def PumpParametersInGeneralScreen():#Frame9 10 11 12 13 14 15
    return render_template('DirectOptionsStation/PumpParametersInGeneral.html')

@app.route('/OnAdditionalPumps')
def OnAdditionalPumpsScreen():#Frame9 10 11 12 13 14 15
    return render_template('DirectOptionsStation/OnAdditionalPumps.html')

@app.route('/OffOfAdditionalPumps')
def OffOfAdditionalPumpsScreen():#Frame9 10 11 12 13 14 15
    return render_template('DirectOptionsStation/OffOfAdditionalPumps.html')

@app.route('/Options')
def OptionsScreen():#Frame9 10 11 12 13 14 15
    return render_template('DirectOptionsStation/Options.html')

@app.route('/EmergencyModes')
def EmergencyModesScreen():#Frame9 10 11 12 13 14 15
    return render_template('DirectOptionsStation/EmergencyModes.html')

@app.route('/SettingsPID')
def SettingsPIDScreen():#Frame16 17 18
    return render_template('DirectEngineeringMenu/SettingsPID.html')

@app.route('/PLC')
def PLCScreen():#Frame16 17 18
    return render_template('DirectEngineeringMenu/PLC.html')

@app.route('/Backup')
def BackupScreen():#Frame16 17 18
    return render_template('DirectEngineeringMenu/Backup.html')

@app.route('/SettingsPanel')
def SettingsPanelScreen():#Frame16 17 18
    return render_template('DirectMenu/SettingsPanel.html')

@app.route('/Contacts')
def ContactsScreen():#Frame16 17 18
    return render_template('DirectMenu/Contacts.html')

if __name__ == '__main__':
    app.run(debug=True)
