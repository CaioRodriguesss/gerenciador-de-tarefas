import PyInstaller.__main__

PyInstaller.__main__.run(
    [
        'main.py',
        '--windowed',
        '--noconsole',
        '--name=GDT',
        '--icon=icon.ico',
        '--add-data=icon.ico;.'
    ]
)