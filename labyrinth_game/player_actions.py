import labyrinth_game.constants as c
import labyrinth_game.utils as u


def show_inventory(game_state):
    states = "Твой инвентарь: " + ', '.join(game_state['player_inventory']) if game_state['player_inventory'] else "Твой инвентарь пуст" # noqa: E501
    print(states)
    
    
def get_input(prompt="> "):
    try:
        user_input = input(prompt)
        return user_input
    except (KeyboardInterrupt, EOFError):
        print("\nВыход из игры.")
        return "quit" 
        
        
def move_player(game_state, direction):
    room = game_state['current_room']
    if direction in list(c.ROOMS[room]['exits'].keys()):
        new_room = c.ROOMS[room]['exits'][direction]
        if new_room == "treasure_room":
            if "rusty key" not in game_state["player_inventory"]:
                print("Дверь заперта. Нужен ключ, чтобы пройти дальше.")
            else:
                print("Вы используете найденный ключ, чтобы открыть путь в комнату сокровищ.") # noqa: E501
                game_state['current_room'] = new_room
                game_state['steps_taken'] += 1
                u.describe_current_room(game_state)
                u.random_event(game_state)
        else:
                game_state['current_room'] = new_room
                game_state['steps_taken'] += 1
                u.describe_current_room(game_state)
                u.random_event(game_state)
    else: 
        print("Нельзя пойти в этом направлении.")
        
def take_item(game_state, item_name):
    room = game_state['current_room']        
    if item_name in c.ROOMS[room]['items']:
        if c.ROOMS[room]['puzzle']:
            print(f'Ты не можешь взять {item_name}, пока не отгадаешь загадку')
        else:            
            game_state['player_inventory'].append(item_name)
            c.ROOMS[room]['items'].remove(item_name)
            print(f'Вы подняли: {item_name}')
        if item_name == "treasure chest":
            print("Ты не можешь взять сундук! Он слишком тяжелый")
    else: 
        print("Такого предмета здесь нет.")
        
def use_item(game_state, item_name):
    if item_name in game_state['player_inventory']:
        match item_name: 
            case 'torch':
                print('Стало светлее.')
            case 'sword':
                print('Ты стала увереннее')
            case 'bronze box':
                print('Открывается шкатулка')
                if 'rusty key' not in game_state['player_inventory']:
                    game_state['player_inventory'].append('rusty key')
                    print('rusty key добавлен в твой инвентарь')
                else:
                    print('Пусто')
            case _:
                print("Ты не знаешь, как использовать")
    else:
        print("У вас нет такого предмета.")
            
        
    
     
