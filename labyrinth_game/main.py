#!/usr/bin/env python3
from labyrinth_game.constants import *
from labyrinth_game.player_actions import *
from labyrinth_game.utils import *
import math as m

game_state = {
        'player_inventory': [], # Инвентарь игрока
        'current_room': 'entrance', # Текущая комната
        'game_over': False, # Значения окончания игры
        'steps_taken': 0 # Количество шагов
  }
  
def process_command(game_state, command):
    if (game_state['current_room'] == 'treasure_room') and (command == 'solve' or command == 'use treasure chest'):
        attempt_open_treasure(game_state)
    else:
        command = command.split(' ', 1)
        match command[0]:
            case "look":
                describe_current_room(game_state)
            case "use":
                check_user_command(command, game_state, use_item)
            case "go":
                check_user_command(command, game_state, move_player)
            case "north"|"east"|"south"|"west":
                move_player(game_state, command[0])        
            case "take":
                check_user_command(command, game_state, take_item)           
            case "solve":
                solve_puzzle(game_state)
            case "inventory":
                show_inventory(game_state)
            case "quit"|"exit":
                print("Выход из игры.")
                game_state['game_over'] = True # Сигнал для завершения игры
            case "help":
                show_help(COMMANDS)
            case _:
                print("Такой команды нет")
            
    return True        
            

def main():
    """ main function """
    print("Добро пожаловать в Лабиринт сокровищ!")
    show_help(COMMANDS)
    describe_current_room(game_state)
    while not game_state['game_over']:
        command = get_input()
        process_command(game_state, command)
    
if __name__ == "__main__":
    main()
