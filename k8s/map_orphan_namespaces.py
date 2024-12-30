import subprocess
import openpyxl

# Configurar o caminho para o arquivo kubeconfig
kubeconfig = "k8s-prd-op.yaml"

# Comando para listar namespaces
command = f"kubectl --kubeconfig={kubeconfig} get namespaces -o jsonpath='{{.items[*].metadata.name}}'"

# Executar o comando e obter a saída
namespaces = subprocess.check_output(command, shell=True).decode('utf-8').split()

# Inicializar a planilha Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Namespaces Órfãos"
ws.append(["Namespace"])

# Verificar recursos em cada namespace e adicionar órfãos na planilha
for ns in namespaces:
    resources_command = f"kubectl --kubeconfig={kubeconfig} get all -n {ns} --no-headers"
    resources = subprocess.check_output(resources_command, shell=True).decode('utf-8')
    if not resources:
        ws.append([ns])

# Salvar o arquivo Excel
wb.save("Namespaces_Orfaos.xlsx")

print("Arquivo Namespaces_Orfaos.xlsx criado com sucesso.")

