import subprocess
import sys

def main():
    # Lista de scripts na mesma pasta
    scripts = [
        "helloworld.py",
        "calculadora_basica.py"
    ]

    while True:
        print("\nSelecione um script para executar:")
        for i, script in enumerate(scripts, 1):
            print(f"{i}. {script}")

        try:
            script_choice = int(input("Digite o número do script (ou 0 para sair): "))

            if script_choice == 0:
                print("Saindo...")
                break

            if 1 <= script_choice <= len(scripts):
                script_to_run = scripts[script_choice - 1]
                subprocess.run([sys.executable, script_to_run])
            else:
                print("Escolha inválida!")
        except ValueError:
            print("Entrada inválida! Digite um número.")

if __name__ == "__main__":
    main()
