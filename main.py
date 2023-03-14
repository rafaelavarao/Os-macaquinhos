import os
import sys


rounds: int = 0
coconuts: list[list[int]] = []
exchanges: list[tuple[int, int, int]] = []


# distribui os cocos conforme a quantidade de pedras de acordo com os macacos indicados
def exchange_coconuts(monkey: int, even_monkey: int, odd_monkey: int):
    coconuts[even_monkey] += [num_rocks for num_rocks in coconuts[monkey] if num_rocks % 2 == 0]
    coconuts[odd_monkey] += [num_rocks for num_rocks in coconuts[monkey] if num_rocks % 2 == 1]
    coconuts[monkey] = []


def main():    
    # [0] macaco que distribui cocos, [1] macaco que vai receber os pares, [3] macaco que vai receber os impares
    for round in range(rounds):
        monkey = round % len(exchanges) # [0 - 5] modulo acessa o index
        even_monkey, odd_monkey = exchanges[monkey]
        exchange_coconuts(monkey, even_monkey, odd_monkey)


if __name__ == "__main__":
    test_cases_folder_path: str = sys.argv[1] #le o diretorio de casos de teste da linha de comando
    for test_case in os.listdir(test_cases_folder_path): # lista os arq do diretorio
        with open(test_cases_folder_path + "\\" + test_case, "r") as file: #juntando o caminho do diretorio mais o nome do arq
            for line in file:
                aux = line.strip().split(' ') #splitando por espaço
                
                if "Fazer" in line:
                    rounds = int(aux[1])
                    continue
                
                even_monkey = int(aux[aux.index('par') + 2])
                odd_monkey = int(aux[aux.index('impar') + 2])
                exchanges.append([even_monkey, odd_monkey])
                
                _coconuts = [int(rocks) for rocks in aux[aux.index(':') + 3:]]
                coconuts.append(_coconuts)
    
        main()
        winner_monkey = 0
        _max = 0
        for monkey, _coconuts in enumerate(coconuts):
            if _max < len(_coconuts):
                _max = len(_coconuts)
                winner_monkey = monkey
            
        with open("resultados.txt", "a") as file:
            file.write(f"Rodadas {rounds} -> Macaco {winner_monkey} : {_max}\n")

        rounds = 0
        coconuts = []
        exchanges = []
