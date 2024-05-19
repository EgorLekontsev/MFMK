from flask import Flask, render_template, jsonify, request
from datetime import datetime
import os
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
    current_date = datetime.now()
    formatted_date = current_date.strftime('%d.%m.%Y')
    file_path = f"data/Log/{formatted_date}.json"
    if not os.path.exists(file_path):
        with open(file_path, "w") as f:
            json.dump([], f)

    with open("data/jsonstorage.json", "r") as file:
        json_data = json.load(file)

    data = json_data["Current_Data"]

    folder_path = 'data/Log'
    file_list = os.listdir(folder_path)
    file_list = [os.path.splitext(filename)[0] for filename in file_list if filename.endswith('.json')]

    if data != formatted_date:
        if len(file_list) == 1:
            json_data["Current_Data"] = file_list[0]

            with open("data/jsonstorage.json", "w") as file:
                json.dump(json_data, file)

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


@app.route("/data")
def data():
    with open("data/jsonstorage.json", "r") as f:
        json_data = f.read()

    data = json.loads(json_data)

    return jsonify(data)


def function_create_data(name_file, data):
    file_path = f"data/Log/{name_file}.json"

    if os.path.exists(file_path):
        with open(file_path, "r") as file:
            json_data = json.load(file)

        if not isinstance(json_data, list):
            json_data = []

        json_data.append(data)

        with open(file_path, "w") as file:
            json.dump(json_data, file)

        return 'Data added successfully'
    else:
        json_data = [data]

        with open(file_path, "w") as file:
            json.dump(json_data, file)

        return 'Data added successfully'


@app.route("/data_log")
def data_log():
    current_date = datetime.now()
    formatted_date = current_date.strftime('%d.%m.%Y')
    file_path = f"data/Log/{formatted_date}.json"

    if (os.path.exists(file_path)):
        with open("data/jsonstorage.json", "r") as file:
            json_data = json.load(file)

        data = json_data["Current_Data"]

        file_path = f"data/Log/{data}.json"

        with open(file_path, "r") as file:
            json_data = file.read()

        data_last = json.loads(json_data)

        return jsonify(data_last)
    else:
        with open(file_path, "w") as f:
            json.dump([], f)

        return 'Data added successfully'


@app.route('/update_data', methods=['POST'])
def update_data():
    new_data = request.form.to_dict()

    with open("data/jsonstorage.json", "r") as file:
        json_data = json.load(file)

    json_data.update(new_data)

    with open("data/jsonstorage.json", "w") as file:
        json.dump(json_data, file)

    return 'Data updated successfully'


@app.route('/add_data_to_log', methods=['POST'])
def add_data_to_log():
    new_data = request.get_json()

    function_create_data(new_data["Date"], new_data)

    return 'Data added successfully'


@app.route('/get_file_list')
def get_file_list():
    folder_path = 'data/Log'
    file_list = os.listdir(folder_path)

    file_list = [os.path.splitext(filename)[0] for filename in file_list if filename.endswith('.json')]

    return jsonify(file_list)


if __name__ == '__main__':
    app.run(debug=True)
