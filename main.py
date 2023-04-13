import os
import sys
import time
import numpy as np
from contextlib import contextmanager
from concurrent.futures import ThreadPoolExecutor, as_completed


EVEN_MONKEY: int = 0
ODD_MONKEY: int = 1
EVEN_COCONUTS: int = 2
ODD_COCONUTS: int = 3


@contextmanager
def timeit_context(name):
    start_time = time.time()
    yield
    elapsed_time = time.time() - start_time
    print(f'[{name}] finished in {int(elapsed_time * 1000)} ms')


def main(test_cases_folder_path, test_case):
    rounds: int = 0
    exchanges: list[list[int]] = []

    # parse file
    with open(test_cases_folder_path + "\\" + test_case, "r") as file: #adding the directory path plus the file name
        for line in file:
            aux = line.strip().split(' ') #split by space
            
            if "Fazer" in line:
                rounds = int(aux[1])
                continue
            
            even_monkey = int(aux[aux.index('par') + 2]) #catch the even values ​​being sent to another monkey ex: "Macaco 0 par -> 43"
            odd_monkey = int(aux[aux.index('impar') + 2]) #catch the odd values ​​being sent to another monkey ex: "impar -> 25"
            
            #make an array with the rocks, taking from +3 positions after the ":"
            coconuts = np.array([int(rocks) for rocks in aux[aux.index(':') + 3:]])
            odd_filter = coconuts % 2 == 1 #get odd values ​​from array
            even_filter = coconuts % 2 == 0 #get the even values ​​from the array
            
            exchanges.append([even_monkey, odd_monkey, len(coconuts[even_filter]), len(coconuts[odd_filter])]) #make an append with even_monkey, odd_monkey and the size of odd_filter and even_filter
    
    # exchange coconuts
    with timeit_context(test_cases_folder_path + "\\" + test_case):
        for round in range(rounds): 
            monkey = round % len(exchanges) #monkey gets the exchange size mod

            #receive the exchanges with the exchanges mod with odd_monkey = 1 or even_monkey = 0
            odd_monkey = exchanges[monkey][ODD_MONKEY] 
            even_monkey = exchanges[monkey][EVEN_MONKEY]
            
            #takes the exchange, with the new values ​​of odd_monkey and even_monkey and increments them
            exchanges[odd_monkey][ODD_COCONUTS] += exchanges[monkey][ODD_COCONUTS] 
            exchanges[even_monkey][EVEN_COCONUTS] += exchanges[monkey][EVEN_COCONUTS]

            #reset the exchanges
            exchanges[monkey][ODD_COCONUTS] = 0
            exchanges[monkey][EVEN_COCONUTS] = 0

    # get the monkey with most coconuts
    winner_monkey = 0
    _max = 0
    for monkey, exchange in enumerate(exchanges):
        if _max < exchange[EVEN_COCONUTS] + exchange[ODD_COCONUTS]: 
            _max = exchange[EVEN_COCONUTS] + exchange[ODD_COCONUTS] 
            winner_monkey = monkey

    return f"Rodadas {rounds} -> Macaco {winner_monkey} : {_max}\n"


if __name__ == "__main__":
    
    results: list[str] = []
    test_cases_folder_path: str = sys.argv[1]
    
    
    #creates an instance runner that will empty threads immediately upon completion.
    with ThreadPoolExecutor() as executor:
        threads = []
        for index, test_case in enumerate(os.listdir(test_cases_folder_path)):
            #Each call to submit returns a Thread instance which is stored in the threads list.
            thread = executor.submit(main, test_cases_folder_path, test_case)
            threads.append(thread)

        #waits for each test_cases_folder_path call to complete for append in results
        for thread in as_completed(threads):
            results.append(thread.result())
    
    #create the file with the results
    with open("results.txt", "w") as file:
        for result in results:
            file.write(result)
