from nicegui import ui, app
from .rshell_commands import get_time_UTC
from nicegui.events import ValueChangeEventArguments
import pyperclip
import datetime
import os
import csv
from stat import S_IREAD, S_IWUSR
def callback_shutdown(event: ValueChangeEventArguments, speedway):
    if speedway.reader is not None:
        speedway.reader.disconnect()
    app.shutdown()

def callback_synchronise(event: ValueChangeEventArguments, speedway):
    speedway.synchronise()
    ui.notify('Speedway synchronised with PC')

def callback_racestart(racestart_label, export_directory):
    t_utc = get_time_UTC(host = "speedwayr-12-36-0F.local", username = "root", password = "impinj")
    t_syd = t_utc.astimezone()
    racestart_label.content = t_syd.strftime("%d/%m/%Y %H:%M:%S")
    pyperclip.copy(t_syd.strftime("%H:%M:%S"))
    date_suffix = '_' + datetime.datetime.now().strftime('%Y-%m-%d')
    filepath = os.path.join(export_directory, 'race_starts'+date_suffix+'.csv')
    if os.path.isfile(filepath):
        os.chmod(filepath, S_IREAD|S_IWUSR)
    with open(filepath, 'a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(
                [t_syd.strftime("%H:%M:%S.%f"),
                    t_syd.strftime("%d/%m/%Y")])
    os.chmod(filepath, S_IREAD)

    ui.notify('Race start captured')
    



def keyboard_wedge_delay_start(speedway, switch):
    speedway.keyboard_wedge_enabled = True
    switch.enable()
    ui.notify(f'Keyboard wedge enabled: True')

def callback_keyboard_wedge(event: ValueChangeEventArguments, speedway, switch):
    WEDGE_DELAY = 10.0
    if event.value == True:
        switch.disable()
        ui.notify(f'Keyboard wedge starting in {WEDGE_DELAY} seconds...')
        ui.timer(WEDGE_DELAY, lambda: keyboard_wedge_delay_start(speedway, switch), once=True)
    else:
        speedway.keyboard_wedge_enabled = event.value
        ui.notify(f'Keyboard wedge enabled: {event.value}')

def callback_ignore_time(event: ValueChangeEventArguments, speedway):
    speedway.ignore_tag_time = event.value
    ui.notify(f'Updated ignore time: {event.value} s')  

def callback_antenna_generic(event: ValueChangeEventArguments, speedway, configure_button, antenna_id):
    antennas = speedway.config_dict['antennas']
    if event.value == True:
        antennas.append(antenna_id)
        antennas.sort()
    else:
        antennas.remove(antenna_id)
        antennas.sort()
    speedway.config_dict['antennas'] = antennas
    if speedway.config_dict['antennas']:
        configure_button.enable()
    else:
        configure_button.disable()
    ui.notify(f'Antenna {antenna_id} enabled: {event.value}')


def callback_antenna_1(event: ValueChangeEventArguments, speedway, configure_button):
    callback_antenna_generic(event, speedway, configure_button, 1)

def callback_antenna_2(event: ValueChangeEventArguments, speedway, configure_button):
    callback_antenna_generic(event, speedway, configure_button, 2)

def callback_antenna_3(event: ValueChangeEventArguments, speedway, configure_button):
    callback_antenna_generic(event, speedway, configure_button, 3)

def callback_antenna_4(event: ValueChangeEventArguments, speedway, configure_button):
    callback_antenna_generic(event, speedway, configure_button, 4)

def callback_hex_encoding(event: ValueChangeEventArguments, speedway):
    speedway.hex_encoding = event.value
    ui.notify(f'Hexadecimal encoding: {event.value}')

def callback_report_timeout(event: ValueChangeEventArguments, speedway):
    speedway.config_dict['report_timeout_ms'] = event.value
    ui.notify(f'Updated report period time: {int(event.value)} ms')   

def callback_configure_speedway(event: ValueChangeEventArguments, speedway, speedway_toggle):
    speedway.configure()
    speedway_toggle.enable()
    ui.notify(f'Speedway configured')

def callback_run_speedway(event: ValueChangeEventArguments, speedway, elements_to_lock, keyboard_wedge_switch):
    if event.value == 1:
        # Turn off keyboard wedge
        keyboard_wedge_switch.value = False
        # Disable keyboard wedge switch
        keyboard_wedge_switch.disable()
        speedway.reader.disconnect()
        ui.notify(f'Speedway stopped')
        for element in elements_to_lock:
            element.enable() 
    elif event.value == 2:
        speedway.reader.connect()
        ui.notify(f'Speedway started')
        # Allow keyboard wedge to be turned on
        keyboard_wedge_switch.enable()
        # Key speedway settings
        for element in elements_to_lock:
            element.disable()