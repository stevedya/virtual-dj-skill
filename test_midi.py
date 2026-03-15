import mido

ports = mido.get_output_names()
print("Available MIDI outputs:", ports)

port_name = ports[1]  # your IAC port

with mido.open_output(port_name) as port:
    port.send(mido.Message("note_on", note=60, velocity=127))

print(f"Sent NOTE 60 to {port_name}")