# coconuts é uma lista de cocos que cada macaco possui
coconuts: list[list[int]] = []
coconuts.append([178,84,1,111,159,22,54,132,201,51,44]) 
coconuts.append([80,82,10,83,98,31,56,84,53])
coconuts.append([65,194,35,132,191,202,62])
coconuts.append([121,10,162])
coconuts.append([16,110,125,113,35])
coconuts.append([120,25,20,134,166,100,157,159])


# distribui os cocos conforme a quantidade de pedras de acordo com os macacos indicados
def exchange_coconuts(monkey: int, even_monkey: int, odd_monkey: int):
    coconuts[even_monkey] += [num_rocks for num_rocks in coconuts[monkey] if num_rocks % 2 == 0]
    coconuts[odd_monkey] += [num_rocks for num_rocks in coconuts[monkey] if num_rocks % 2 == 1]
    coconuts[monkey] = []


# pega o indice do macaco e faz as trocas
def main():
    rounds: int = 100_000 #quantas vezes vai rodar
    exchanges: list[tuple[int, int, int]] = [(0,4,3), (1,0,5), (2,3,4), (3,0,4), (4,0,5), (5,2,0)] * rounds
    
    # [0] macaco que distribui cocos, [1] macaco que vai receber os pares, [3] macaco que vai receber os impares
    for _, exchange in enumerate(exchanges):
        exchange_coconuts(exchange[0], exchange[1], exchange[2])


if __name__ == "__main__":
    main()
    for monkey, _coconuts in enumerate(coconuts):
        #num do macaco e a lista de pedrinhas
        print(monkey, _coconuts)