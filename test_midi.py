from dj.midi import get_output_names, test_connection

print("Outputs:", get_output_names())
print(test_connection())