
from fileDbc import FileDbc
from fileTrc import FileTrc

import pprint

def decryp(tramCan):
    
   
    fileDbc = FileDbc("./WEENAV.dbc")
    fileTrc = FileTrc(tramCan)

    allData = fileTrc.find_data(fileDbc.getDataStruct(), fileDbc.getData())  # Extract data from the TRC file at initialization

    idManquants = fileTrc.getIdManquant()
    if len(idManquants) > 0:
        print(f"\033[91mAttention, {len(idManquants)} ID manquants dans le fichier DBC, veuillez vérifier le fichier DBC.\033[0m")
        print("ID manquants dans le fichier DBC:")
        print([f"{elem:X}" for elem in fileTrc.getIdManquant()])

    print(allData)

    return allData

