from nicegui import ui, app
from nicegui.events import ValueChangeEventArguments
from . import gui_callbacks

def gui(speedway, export_directory):
    ui.markdown('#### General controls')
    ui.button('Shutdown',
        icon='close',
        color = 'red',
        on_click=lambda e: gui_callbacks.callback_shutdown(e, speedway))

    ui.button('Synchronise clocks',
        icon='sync',
        on_click=lambda e: gui_callbacks.callback_synchronise(e, speedway))

    with ui.row():
        ui.button('Race start',
            icon = 'timer',
            on_click=lambda: gui_callbacks.callback_racestart(racestart_label, export_directory))
        racestart_label = ui.markdown("dd/mm/yyyy HH:MM:SS")
        
    keyboard_wedge_switch = ui.switch(
        'Enable keyboard wedge',
        on_change=lambda e: gui_callbacks.callback_keyboard_wedge(e, speedway, keyboard_wedge_switch))
    keyboard_wedge_switch.disable()

    ui.markdown('#### Speedway controls')

    with ui.row(): 
        ui.markdown("Antennas:")
        antenna1 = ui.checkbox('1', on_change=lambda e: gui_callbacks.callback_antenna_1(e, speedway, configure_button))
        antenna2 = ui.checkbox('2', on_change=lambda e: gui_callbacks.callback_antenna_2(e, speedway, configure_button))
        antenna3 = ui.checkbox('3', on_change=lambda e: gui_callbacks.callback_antenna_3(e, speedway, configure_button))
        antenna4 = ui.checkbox('4', on_change=lambda e: gui_callbacks.callback_antenna_4(e, speedway, configure_button))
    
    hex_switch = ui.switch('Hexadecimal encoding', value = True, on_change=lambda e: gui_callbacks.callback_hex_encoding(e, speedway))
    report_period_number = ui.number(
        label='Report period (milliseconds)',
        value=speedway.config_dict['report_timeout_ms'],
        min=10, #10 ms minimum to avoid PC being overwhelmed
        format='%d',
              on_change=lambda e: gui_callbacks.callback_report_timeout(e, speedway))
    ignore_tag_number = ui.number(
        label='Ignore tag duration (seconds)',
        value=speedway.ignore_tag_time,
        min=20,
        format='%d',
        on_change=lambda e: gui_callbacks.callback_ignore_time(e, speedway))

    configure_button = ui.button('Configure Speedway',
        icon = 'build',
        on_click=lambda e: gui_callbacks.callback_configure_speedway(e, speedway, speedway_toggle))
    configure_button.disable()
    elements_to_lock = [antenna1, antenna2, antenna3, antenna4, hex_switch, report_period_number, configure_button, ignore_tag_number]
    speedway_toggle = ui.toggle({1: 'Stop Speedway', 2: 'Start Speedway'},
        value = 1,
        on_change= lambda e: gui_callbacks.callback_run_speedway(e, speedway, elements_to_lock, keyboard_wedge_switch))
    speedway_toggle.disable()

    ui.run()
