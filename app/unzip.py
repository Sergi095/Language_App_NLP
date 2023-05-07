import platform
import subprocess
import os




def main():

    zip_file_path = "../Neural_Machine_Translator/saved_model_zip/saved_model_en_es"
    target_directory = "../Neural_Machine_Translator/saved_model/"

    # print(os.listdir(zip_file_path))


    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        command = f"cat {zip_file_path}.z* > {zip_file_path}.zip"
    else:
        command = f"copy /b {zip_file_path}.z* > {zip_file_path}.zip"
    subprocess.call(command, shell=True)
    print('here')
    # Unzip the file
    if platform.system() == 'Linux' or platform.system() == 'Darwin':
        subprocess.call(['unzip', f'{zip_file_path}', '-d', f'{target_directory}'])
    else:
        print('here')
        if not os.path.exists(target_directory):
            os.makedirs(target_directory)
        subprocess.call(['powershell', f'Expand-Archive -Path "{zip_file_path}.zip" -DestinationPath "{target_directory}"'])
        print('done')

    # zip_file_path = "../Neural_Machine_Translator/saved_model_zip/saved_model_en_es.zip"
    # # en-es
    # with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    #     zip_ref.extractall("../Neural_Machine_Translator/saved_model/")
    # zip_file_path = "../Neural_Machine_Translator/saved_model_zip_es_en/saved_model_en_es.zip"
    # # es-en
    # with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
    #     zip_ref.extractall("../Neural_Machine_Translator/saved_model_en_es/")



if __name__ == "__main__":
    print('running')
    main()
