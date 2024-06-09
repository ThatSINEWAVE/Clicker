import PyInstaller.__main__
import os

PyInstaller.__main__.run([
    'main_v2.py',
    '--onefile',
    '--windowed',
    '--add-data=assets;assets',
    '--name=SINEWAVE_Clicker_Game'
])

# Modify the generated spec file
spec_file = 'SINEWAVE_Clicker_Game.spec'
with open(spec_file, 'r') as f:
    spec_lines = f.readlines()

for i, line in enumerate(spec_lines):
    if line.startswith('exe = EXE('):
        spec_lines[i] = 'exe = EXE(icon=os.path.join(DISTPATH, "assets", "app", "window_icon.ico"),\n'
        break

with open(spec_file, 'w') as f:
    f.writelines(spec_lines)