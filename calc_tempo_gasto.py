def calcular_tempo(distancia, velocidade):
    if velocidade == 0:
        return "A velocidade não pode ser zero."
    
    tempo = distancia / velocidade
    return tempo

def main():
    try:
        distancia = float(input("Digite a distância em quilômetros: "))
        velocidade = float(input("Digite a velocidade em km/h: "))
        
        tempo = calcular_tempo(distancia, velocidade)
        
        if isinstance(tempo, str):
            print(tempo)
        else:
            print(f"Você vai gastar {tempo:.2f} horas para percorrer {distancia} km a uma velocidade de {velocidade} km/h.")
    except ValueError:
        print("Por favor, insira valores numéricos válidos.")

if __name__ == "__main__":
    main()
