from nicegui import ui, app
from rshell_commands import get_time_UTC
from nicegui.events import ValueChangeEventArguments
import pyperclip

def callback_shutdown(event: ValueChangeEventArguments, speedway):
    speedway.reader.disconnect()
    app.shutdown()

def callback_synchronise(event: ValueChangeEventArguments, speedway):
    speedway.synchronise()
    ui.notify('Speedway synchronised with PC')

def callback_racestart(racestart_label):
    t_utc = get_time_UTC(host = "speedwayr-12-36-0F.local", username = "root", password = "impinj")
    t_syd = t_utc.astimezone()
    racestart_label.content = t_syd.strftime("%Y/%m/%d %H:%M:%S")
    pyperclip.copy(t_syd.strftime("%H:%M:%S"))
    ui.notify('Race start captured')

def keyboard_wedge_delay_start(speedway, switch):
    speedway.keyboard_wedge_enabled = True
    switch.enable()
    ui.notify(f'Keyboard wedge enabled: True')

def callback_keyboard_wedge(event: ValueChangeEventArguments, speedway, switch):
    if event.value == True:
        switch.disable()
        ui.notify('Keyboard wedge starting in 5 seconds...')
        ui.timer(5.0, lambda: keyboard_wedge_delay_start(speedway, switch), once=True)
    else:
        speedway.keyboard_wedge_enabled = event.value
        ui.notify(f'Keyboard wedge enabled: {event.value}')

def callback_ignore_time(event: ValueChangeEventArguments, speedway):
    speedway.ignore_tag_time = event.value
    ui.notify(f'Updated ignore time: {event.value} s')  

def callback_antenna_generic(event: ValueChangeEventArguments, speedway, antenna_id):
    antennas = speedway.config_dict['antennas']
    if event.value == True:
        antennas.append(antenna_id)
        antennas.sort()
    else:
        antennas.remove(antenna_id)
        antennas.sort()
    speedway.config_dict['antennas'] = antennas
    ui.notify(f'Antenna {antenna_id} enabled: {event.value}')

def callback_antenna_1(event: ValueChangeEventArguments, speedway):
    callback_antenna_generic(event, speedway, 1)

def callback_antenna_2(event: ValueChangeEventArguments, speedway):
    callback_antenna_generic(event, speedway, 2)

def callback_antenna_3(event: ValueChangeEventArguments, speedway):
    callback_antenna_generic(event, speedway, 3)

def callback_antenna_4(event: ValueChangeEventArguments, speedway):
    callback_antenna_generic(event, speedway, 4)

def callback_hex_encoding(event: ValueChangeEventArguments, speedway):
    speedway.hex_encoding = event.value
    ui.notify(f'Hexadecimal encoding: {event.value}')

def callback_report_timeout(event: ValueChangeEventArguments, speedway):
    speedway.config_dict['report_timeout_ms'] = event.value
    ui.notify(f'Updated report period time: {int(event.value)} ms')   

def callback_configure_speedway(event: ValueChangeEventArguments, speedway):
    speedway.configure()
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