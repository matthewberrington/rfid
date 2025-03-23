from nicegui import ui
from nicegui.events import ValueChangeEventArguments
import gui_callbacks

ui.markdown('## General controls')
with ui.row():
    ui.button('Race start', on_click=lambda: gui_callbacks.callback_racestart(racestart_label))
    racestart_label = ui.markdown("yyyy/mm/dd HH:MM:SS")
    
ui.switch('Enable keyboard wedge', on_change=gui_callbacks.callback_keyboard_wedge)

ui.number(label='Ignore tag duration (seconds)', value=20, format='%.2f',
          on_change=gui_callbacks.callback_ignore_time)

ui.markdown('## Speedway controls')
with ui.row(): 
    ui.markdown("Antennas:")
    antenna1 = ui.checkbox('1', on_change=gui_callbacks.callback_antenna_1)
    antenna2 = ui.checkbox('2', on_change=gui_callbacks.callback_antenna_2)
    antenna3 = ui.checkbox('3', on_change=gui_callbacks.callback_antenna_3)
    antenna4 = ui.checkbox('4', on_change=gui_callbacks.callback_antenna_4)
hex_switch = ui.switch('Hexadecimal encoding', on_change=gui_callbacks.callback_hex_encoding)
report_period_number = ui.number(label='Report period (milliseconds)', value=100, format='%.0f',
          on_change=gui_callbacks.callback_report_timeout)

configure_button = ui.button('Configure Speedway',
          on_click=gui_callbacks.callback_configure_speedway)
elements = [antenna1, antenna2, antenna3, antenna4, hex_switch, report_period_number, configure_button]
toggle1 = ui.toggle({1: 'Stop Speedway', 2: 'Start Speedway'}, value=1, on_change= lambda e: gui_callbacks.callback_speedway(e, elements))

ui.run()
