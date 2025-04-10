from operator import index
from webbrowser import Error

import pandas as pd

from Project.pars_info import parsinfo


#Добавляет данные человека в таблицу
#Register = True
#join = [login,fio,class]
def register(join):
    dtb = parsinfo('D:\PyCharm Community Edition 2024.2\LDOD\Project\Истинная инфа.xlsx')
    backup_data = {"Логин":[],'ФИО':[],'Класс':[],'Register':[],'Очки':[]}

    for i in dtb:
        if i[0] == join[0] or i[1] == join[1]:
            #нужно выдать ошибку "попытка повторной регистрации"
            return False
    dtb += join+[True,0]
    
    for i in dtb:
        backup_data['Логин'] = backup_data['Логин'] + [i[0]]
        backup_data['ФИО'] = backup_data['ФИО'] + [i[1]]
        backup_data['Класс'] = backup_data['Класс'] + [i[2]]
        backup_data['Register'] = backup_data['Register'] + [i[3]]
        backup_data['Очки'] = backup_data['Очки'] + [i[4]]
        
    backup_data = pd.DataFrame(backup_data)
    backup_data.to_excel('D:\PyCharm Community Edition 2024.2\LDOD\Project\Истинная инфа.xlsx', index=False)
 
  
#Проверяет зарегистрирован человек или нет
#Если да то возвращает -1 если нет то меняет true на false и возвращяет его индекс
def cheakreg(fio): 
    dtb = parsinfo('D:\PyCharm Community Edition 2024.2\LDOD\Project\Истинная инфа.xlsx')
    print(dtb)
    for i in range(len(dtb)):
        if dtb[i][1] == fio:
            if dtb[i][3] == True:
                return -1
            else:
                dtb[i][3] = 'False'
                backup_data = {"Логин":[],'ФИО':[],'Класс':[],'Register':[],'Очки':[]}

                for j in dtb:
                    backup_data['Логин'] = backup_data['Логин'] + [j[0]]
                    backup_data['ФИО'] = backup_data['ФИО'] + [j[1]]
                    backup_data['Класс'] = backup_data['Класс'] + [j[2]]
                    backup_data['Register'] = backup_data['Register'] + [j[3]]
                    backup_data['Очки'] = backup_data['Очки'] + [j[4]]

                backup_data = pd.DataFrame(backup_data)
                backup_data.to_excel('D:\PyCharm Community Edition 2024.2\LDOD\Project\Истинная инфа.xlsx', index=False)
                return dtb
        else:
            print(123)

cheakreg('ЛюосеваД')