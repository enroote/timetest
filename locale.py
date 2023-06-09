import subprocess

# Run the "locale -a" command to get the available locales
output = subprocess.check_output(['locale', '-a']).decode('utf-8')

# Split the output by newline to get individual locales
locales = output.strip().split('\n')

# Print the available locales
for loc in locales:
    print(loc)
