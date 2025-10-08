import labyrinth_game.constants as c
import labyrinth_game.player_actions as pa
import labyrinth_game.utils as u

game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
  }
  
def process_command(game_state, command):
    if (game_state['current_room'] == 'treasure_room' and 
        command == 'solve' or command == 'use treasure chest'):
        u.attempt_open_treasure(game_state)
    else:
        command = command.split(' ', 1)
        match command[0]:
            case "look":
                u.describe_current_room(game_state)
            case "use":
                u.check_user_command(command, game_state, pa.use_item)
            case "go":
                u.check_user_command(command, game_state, pa.move_player)
            case "north"|"east"|"south"|"west":
                pa.move_player(game_state, command[0])        
            case "take":
                u.check_user_command(command, game_state, pa.take_item)           
            case "solve":
                u.solve_puzzle(game_state)
            case "inventory":
                pa.show_inventory(game_state)
            case "quit"|"exit":
                print("Выход из игры.")
                game_state['game_over'] = True # Сигнал для завершения игры
            case "help":
                u.show_help(c.COMMANDS)
            case _:
                print("Такой команды нет")
            
    return True        
            
def main():
    """ main function """
    print("Добро пожаловать в Лабиринт сокровищ!")
    u.show_help(c.COMMANDS)
    u.describe_current_room(game_state)
    while not game_state['game_over']:
        command = pa.get_input()
        process_command(game_state, command)
    
if __name__ == "__main__":
    main()
