from flask import Flask, render_template, jsonify, request
import json

app = Flask(__name__)

@app.route('/')
def MainScreen():
    return render_template('DirectMenu/Main.html')

@app.route('/Main1')
def Main1Screen():
    return render_template('DirectMenu/Main1.html')

@app.route('/Main2')
def Main2Screen():
    return render_template('DirectMenu/Main2.html')

@app.route('/Main3')
def Main3Screen():
    return render_template('DirectMenu/Main3.html')

@app.route('/SetpointPlanner')
def SetpointPlannerScreen():
    return render_template('DirectMenu/SetpointPlanner.html')

@app.route('/OnlineTrends')
def OnlineTrendsScreen():
    return render_template('DirectMonitoring/OnlineTrends.html')

@app.route('/HistoryTrends')
def HistoryTrendsScreen():
    return render_template('DirectMonitoring/HistoryTrends.html')

@app.route('/PumpOperatingTime')
def PumpOperatingTimeScreen():
    return render_template('DirectMonitoring/PumpOperatingTime.html')

@app.route('/CurrentEvent')
def CurrentEventScreen():
    return render_template('DirectJournal/CurrentEvent.html')

@app.route('/JournalHistory')
def JournalHistoryScreen():
    return render_template('DirectJournal/JournalHistory.html')

@app.route('/ChangeLog')
def ChangeLogScreen():
    return render_template('DirectJournal/ChangeLog.html')

@app.route('/EngineParameters')
def EngineParametersScreen():
    return render_template('DirectOptionsStation/EngineParameters.html')

@app.route('/SensorSettings')
def SensorSettingsScreen():
    return render_template('DirectOptionsStation/SensorSettings.html')

@app.route('/PumpParametersInGeneral')
def PumpParametersInGeneralScreen():
    return render_template('DirectOptionsStation/PumpParametersInGeneral.html')

@app.route('/OnAdditionalPumps')
def OnAdditionalPumpsScreen():
    return render_template('DirectOptionsStation/OnAdditionalPumps.html')

@app.route('/OffOfAdditionalPumps')
def OffOfAdditionalPumpsScreen():
    return render_template('DirectOptionsStation/OffOfAdditionalPumps.html')

@app.route('/Options')
def OptionsScreen():
    return render_template('DirectOptionsStation/Options.html')

@app.route('/EmergencyModes')
def EmergencyModesScreen():
    return render_template('DirectOptionsStation/EmergencyModes.html')

@app.route('/SettingsPID')
def SettingsPIDScreen():
    return render_template('DirectEngineeringMenu/SettingsPID.html')

@app.route('/PLC')
def PLCScreen():
    return render_template('DirectEngineeringMenu/PLC.html')

@app.route('/Backup')
def BackupScreen():
    return render_template('DirectEngineeringMenu/Backup.html')

@app.route('/SettingsPanel')
def SettingsPanelScreen():
    return render_template('DirectMenu/SettingsPanel.html')

@app.route('/Contacts')
def ContactsScreen():
    return render_template('DirectMenu/Contacts.html')

@app.route('/Keyboard')
def KeyboardScreen():
    return render_template('DirectInput/Keyboard.html')

@app.route("/data")
def data():
    with open("data/jsonstorage.json", "r") as f:
        json_data = f.read()

    data = json.loads(json_data)

    return jsonify(data)

@app.route('/update_data', methods=['POST'])
def update_data():
    new_data = request.form.to_dict()

    with open("data/jsonstorage.json", "r") as file:
        json_data = json.load(file)

    json_data.update(new_data)  # Обновить словарь с данными из JSON

    with open("data/jsonstorage.json", "w") as file:
        json.dump(json_data, file)

    return 'Data updated successfully'

if __name__ == '__main__':
    app.run(debug=True)
