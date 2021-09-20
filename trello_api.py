import sys 
import requests    
base_url = "https://api.trello.com/1/{}" 
auth_params = {    
    'key': "KEY",    
    'token': "TOKEN", }
board_id = "ID"    
    
def read():      
    # Получим данные всех колонок на доске:      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Теперь выведем название каждой колонки и всех заданий, которые к ней относятся:      
    for column in column_data:        
        # Получим данные всех задач в колонке и перечислим все названия      
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()      
        print(column['name'], len(task_data))  
        if not task_data:      
            print('\t' + 'Нет задач!')      
            continue      
        for task in task_data:      
            print('\t' + task['name'])    
    
def create(name, column_name):      
    # Получим данные всех колонок на доске      
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()      
      
    # Переберём данные обо всех колонках, пока не найдём ту колонку, которая нам нужна      
    for column in column_data:      
        if column['name'] == column_name:      
            # Создадим задачу с именем _name_ в найденной колонке      
            requests.post(base_url.format('cards'), data={'name': name, 'idList': column['id'], **auth_params})      
            break
    
def create_column(column_name):
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': column_name, 'id': board_id, **auth_params})

def move(name, current_column, column_name):    
    # Получим данные всех колонок на доске    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()    
        
    cur_col_id = None
    for column in column_data:
        if current_column == column['name']:
            cur_col_id = column['id']
            break

    # Среди всех колонок нужно найти задачу по имени и получить её id    
    task_id = None   

    # Подсчет заданий именем name 
    task_count = 0

    # Получаем json текущей колонки
    column_tasks = requests.get(base_url.format('lists') + '/' + cur_col_id + '/cards', params=auth_params).json()    


    for task in column_tasks:    
        if task['name'] == name:    
            task_id = task['id']    
            task_count += 1

    # Если в колонке больше одного элемента с одним именем
    if task_count > 1:
        # Выводим колонку с их индексами
        print(current_column)
        i = 0
        for task in column_tasks:      
            i += 1
            print('   {} '.format(i) + task['name'])

        # Вводим индекс
        number = int(input("Введите номер задачи: "))
        
        i = 0
        for task in column_tasks:
            i += 1

            # Если имя и индекс совпадают
            # Записываем его id
            if task['name'] == name and i == number:    
                task_id = task['id']   
                break

       
    # Теперь, когда у нас есть id задачи, которую мы хотим переместить    
    # Переберём данные обо всех колонках, пока не найдём ту, в которую мы будем перемещать задачу    
    for column in column_data:    
        if column['name'] == column_name:    
            # И выполним запрос к API для перемещения задачи в нужную колонку    
            requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})    
            break    
    
if __name__ == "__main__":    
    if len(sys.argv) <= 2:    
        read()    
    elif sys.argv[1] == 'create':    
        create(sys.argv[2], sys.argv[3])    
    elif sys.argv[1] == 'move':    
        move(sys.argv[2], sys.argv[3], sys.argv[4])  
    elif sys.argv[1] == 'create_column':
        create_column(sys.argv[2])