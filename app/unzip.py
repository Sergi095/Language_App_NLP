import platform
import subprocess
import zipfile
import os

import winreg

def get_zip_path():
    try:
        # Open the WinRAR key
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\WinRAR")

        # Get the installation path
        winrar_path = winreg.QueryValueEx(reg_key, "exe64")[0]

        return winrar_path
    except FileNotFoundError:
        pass
    try:
        # Try to get the 7-Zip installation path
        reg_key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE, r"SOFTWARE\7-Zip"
        )
        seven_zip_path = winreg.QueryValueEx(reg_key, "exe64")[0]
        return seven_zip_path
    except FileNotFoundError:
        pass


def unzip_models():

    zip_file_path = "../Neural_Machine_Translator/saved_model_zip/saved_model_en_es"
    zip_file_path_2 = "../Neural_Machine_Translator/saved_model_zip_en_es/saved_model_en_es"
    target_directory = "../Neural_Machine_Translator/"

    # print(os.listdir("../Neural_Machine_Translator/saved_model_zip/"))
    # Unzip the file
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        subprocess.call(['unzip', f'{zip_file_path}.zip', '-d', f'{target_directory}'])
    else:
        zip_program_path = get_zip_path()
        subprocess.call([zip_program_path, "x", "-ibck", f"{zip_file_path}.zip", "*.*", target_directory])
        subprocess.call([zip_program_path, "x", "-ibck", f"{zip_file_path_2}.zip", "*.*", target_directory])


if __name__ == "__main__":
    print('running')
    unzip_models()
    # path = get_winrar_path()
    # print(path)

