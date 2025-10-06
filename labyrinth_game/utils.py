import labyrinth_game.constants as c
import math as m

commands = c.COMMANDS

def describe_current_room(game_state):
    room =  game_state['current_room']
    print("== ", room.upper())
    print(c.ROOMS[room]['description'])
    if c.ROOMS[room]['items']:
        print("Предметы: ", end='')
        print(*c.ROOMS[room]['items'], sep=', ')
    print("Выходы: ", end='')
    print(*c.ROOMS[room]['exits'].keys(), sep=', ')  
    if c.ROOMS[room]['puzzle']:
        print("Кажется, здесь есть загадка (используйте команду solve).")    
    

def solve_puzzle(game_state):
    room =  game_state['current_room']
    if c.ROOMS[room]['puzzle']:
        print(c.ROOMS[room]['puzzle'][0])
        print('У тебя 3 попытки')
        print('Ваш ответ: ')
        cnt = 0
        while cnt < 3:
            user_answer = input('--')
            cnt += 1
            if user_answer in c.ROOMS[room]['puzzle'][1]:
                print('Правильно!')
                c.ROOMS[room]['puzzle'] = None
                if c.AWARDS.get(room, None):                
                    print(f'Твоя награда: {c.AWARDS[room]}')
                    game_state['player_inventory'].append(c.AWARDS[room])
                break
            else:
                print('Неверно. Попробуйте снова.')
        else:
            print("Попытки закончены :(")
    else:
        print("Загадок здесь нет.")
                
def attempt_open_treasure(game_state):
    room =  game_state['current_room']
    if 'treasure chest' in c.ROOMS[room]['items']:
        if ('treasure key' in game_state['player_inventory'] or 
            'rusty key'in game_state['player_inventory']):
            print("Вы применяете ключ, и замок щёлкает. Сундук открыт!")
            c.ROOMS[room]['items'].remove('treasure chest')
            print("В сундуке сокровище! Вы победили!")
            game_state['game_over'] = True
        else:
            print("Сундук заперт. ... Ввести код? (да/нет)")
            answer = input("Твой ответ: ")
            match answer:
                case "да":
                    print(c.ROOMS[room]['puzzle'][0])
                    key_ = input("Введи код:")
                    if key_ == c.ROOMS[room]['puzzle'][1]:
                        print("Это успех!")
                        c.ROOMS[room]['items'].remove('treasure chest')
                        game_state['game_over'] = True
                    else:
                        print("Код неверный!")
                        trigger_trap(game_state)
                case "нет":
                    print("Вы отступаете от сундука.")
                
        
    else:
        print('Сундук уже открыт или отсутствует.')
        
        
def show_help(commands):
    print("\nДоступные команды:")
    for command, description in commands.items():
        # Форматируем команду с отступом в 16 символов слева
        print(f"{command:<16} - {description}")
    
 
def pseudo_random(seed, modulo):
    x = m.sin((seed * 1.9898)) * 43.5453
    return int(modulo * (x - m.floor(x)))
    
def trigger_trap(game_state):
    print("Ловушка активирована! Пол стал дрожать...")
    if game_state["player_inventory"]:
        ind = pseudo_random(game_state["steps_taken"], len(game_state["player_inventory"])) # noqa: E501
        print(f'Ты потеряла {game_state["player_inventory"].pop(ind)}')
    else:
        num = pseudo_random(0, 9)
        if num < 3:
            print("Ты получила урон... GAME OVER =( ")
            game_state["game_over"] = True
        else:
            print("Ты уцелела!")
            
            
def random_event(game_state):
    probability = pseudo_random(game_state["steps_taken"], 10)
    if probability > 0:
        event = pseudo_random(0, 2)
        match event:
            case 0:
                print("Ты нашла монетку")
                room = game_state['current_room']
                c.ROOMS[room]['items'].append("coin")
            case 1:
                print("Ты слышишь шорох")
                if 'sword' in game_state["player_inventory"]:
                    print("Ты отпугнула существо")
            case 2:
                room = game_state['current_room']
                if (room == 'trap_room' 
                    and 'torch' not in game_state["player_inventory"]):
                    print("Опасность!")
                    trigger_trap(game_state)
            
     
    
    
def check_user_command(user_command, game_state, func):
    if len(user_command) == 1:
        print("Введите команду полностью")
    else:             
        func(game_state, user_command[1])
