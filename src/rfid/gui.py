from nicegui import ui
from nicegui.events import ValueChangeEventArguments
import gui_callbacks

with ui.row():
    ui.button('Race start', on_click=lambda: gui_callbacks.callback_racestart(racestart_label))
    racestart_label = ui.markdown("yyyy/mm/dd HH:MM:SS")
    
ui.switch('Enable keyboard wedge', on_change=gui_callbacks.callback_keyboard_wedge)
ui.switch('Hexadecimal encoding', on_change=gui_callbacks.callback_hex_encoding)
with ui.row(): 
    ui.markdown("Antennas:")
    ui.checkbox('1', on_change=gui_callbacks.callback_antenna_1)
    ui.checkbox('2', on_change=gui_callbacks.callback_antenna_2)
    ui.checkbox('3', on_change=gui_callbacks.callback_antenna_3)
    ui.checkbox('4', on_change=gui_callbacks.callback_antenna_4)
ui.number(label='Ignore tag duration', value=20, format='%.2f',
          on_change=gui_callbacks.callback_ignore_time)
result = ui.label()

toggle1 = ui.toggle({1: 'Stop Speedway', 2: 'Start Speedway'}, value=1, on_change=gui_callbacks.callback_speedway)



ui.run()
