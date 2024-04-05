from pywebio import config
from pywebio.input import *
from pywebio.output import *

def bmi():
    put_buttons(['Меню'], onclick=menu)

def menu(btn):
    clear()
    put_buttons(['Главный экран'], onclick=main_screen)
    put_buttons(['Планировщик уставок'], onclick=setpoint_planner)
    put_buttons(['Мониторинг'], onclick=monitoring)
    put_buttons(['Журнал'], onclick=journal)
    put_buttons(['Настройки станции'], onclick=station_settings)
    put_buttons(['Инженерное меню'], onclick=engineering_menu)
    put_buttons(['Настройки панели'], onclick=panel_settings)
    put_buttons(['Контакты'], onclick=contacts)

def main_screen(btn):
    clear()
    put_buttons(['Меню'], onclick=menu)

def setpoint_planner(btn):
    pass

def monitoring(btn):
    clear()
    put_buttons(['Главный экран'], onclick=main_screen)
    put_buttons(['Назад'], onclick=menu)
    put_buttons(['Тренды онлайн'], onclick=online_trends)
    put_buttons(['Тренды истории'], onclick=history_trends)
    put_buttons(['Наработка насосов'], onclick=operating_time_of_pumps)

def online_trends(btn):
    pass
def history_trends(btn):
    pass
def operating_time_of_pumps(btn):
    pass
def journal(btn):
    clear()
    put_buttons(['Главный экран'], onclick=main_screen)
    put_buttons(['Назад'], onclick=menu)
    put_buttons(['Текущие события'], onclick=current_events)
    put_buttons(['Журнал историй'], onclick=history_magazine)
    put_buttons(['Журнал измерений'], onclick=measurement_log)

def current_events(btn):
    pass
def history_magazine(btn):
    pass
def measurement_log(btn):
    pass
def station_settings(btn):
    clear()
    put_buttons(['Главный экран'], onclick=main_screen)
    put_buttons(['Назад'], onclick=menu)
    put_buttons(['Параметры двигателей'], onclick=engine_parameters)
    put_buttons(['Настройки датчиков'], onclick=sensor_settings)
    put_buttons(['Параметры насосов общ.'], onclick=pump_parameters_in_general)
    put_buttons(['Вкл. доп. насосов'], onclick=on_additional_pumps)
    put_buttons(['Откл. доп. насосов'], onclick=off_of_additional_pumps)
    put_buttons(['Опции'], onclick=options)
    put_buttons(['Аварийные режимы'], onclick=emergency_modes)
def engine_parameters(btn):
    pass
def sensor_settings(btn):
    pass
def pump_parameters_in_general(btn):
    pass
def on_additional_pumps(btn):
    pass
def off_of_additional_pumps(btn):
    pass
def options(btn):
    pass
def emergency_modes(btn):
    pass
def engineering_menu(btn):
    clear()
    put_buttons(['Главный экран'], onclick=main_screen)
    put_buttons(['Назад'], onclick=menu)
    put_buttons(['Настройки ПИД-рег.'], onclick=PID_reg_settings)
    put_buttons(['PLC'], onclick=PLC)
    put_buttons(['Бэкап'], onclick=Backup)
def PID_reg_settings(btn):
    pass
def PLC(btn):
    pass
def Backup(btn):
    pass
def panel_settings(btn):
    pass
def contacts(btn):
    pass

if __name__ == '__main__':
    bmi()