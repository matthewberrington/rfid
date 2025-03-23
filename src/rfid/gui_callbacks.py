from nicegui import ui
from get_server_time import get_time_UTC
from nicegui.events import ValueChangeEventArguments

# config_dict, reader, cb parameters

def callback_racestart(racestart_label):
    t = get_time_UTC(host = "speedwayr-12-36-0F.local", username = "root", password = "impinj")
    racestart_label.content = t.strftime("%Y/%m/%d %H:%M:%S")
    ui.notify('Race start captured')

def callback_keyboard_wedge(event: ValueChangeEventArguments):
    ui.notify(f'Keyboard wedge: {event.value}')

def callback_ignore_time(event: ValueChangeEventArguments):
    ui.notify(f'Updated ignore time: {event.value} s')  

def callback_antenna_generic(event: ValueChangeEventArguments, speedway, antenna_id):
    ui.notify(f'Antenna {antenna_id}: {event.value}')
    antennas = speedway.config_dict['antennas']
    if event.value == True:
        antennas.append(antenna_id)
        antennas.sort()
    else:
        antennas.remove(antenna_id)
        antennas.sort()
    speedway.config_dict['antennas'] = antennas

def callback_antenna_1(event: ValueChangeEventArguments, speedway):
    callback_antenna_generic(event, speedway, 1)

def callback_antenna_2(event: ValueChangeEventArguments, speedway):
    callback_antenna_generic(event, speedway, 2)

def callback_antenna_3(event: ValueChangeEventArguments, speedway):
    callback_antenna_generic(event, speedway, 3)

def callback_antenna_4(event: ValueChangeEventArguments, speedway):
    callback_antenna_generic(event, speedway, 4)

def callback_hex_encoding(event: ValueChangeEventArguments):
    ui.notify(f'Hexadecimal encoding: {event.value}')

def callback_report_timeout(event: ValueChangeEventArguments):
    ui.notify(f'Updated report period time: {event.value} ms')      

def callback_configure_speedway(event: ValueChangeEventArguments, speedway):
    speedway.configure()
    ui.notify(f'Speedway configured')

def callback_speedway(event: ValueChangeEventArguments, speedway_elements):
    if event.value == 1:
        ui.notify(f'Speedway stopped')  
        for element in speedway_elements:
            element.enable() 
    elif event.value == 2:
        ui.notify(f'Speedway started')
        for element in speedway_elements:
            element.disable()