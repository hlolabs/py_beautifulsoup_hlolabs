import subprocess
import openpyxl
import json

# Configurar o caminho para o arquivo kubeconfig
kubeconfig = "k8s-prd-op.yaml"

# Comando para listar todos os namespaces
command = f"kubectl --kubeconfig={kubeconfig} get namespaces -o jsonpath='{{.items[*].metadata.name}}'"
namespaces = subprocess.check_output(command, shell=True).decode('utf-8').split()

# Função para obter detalhes de um namespace
def get_namespace_details(ns):
    details = {}
    
    try:
        # Obter recursos
        resources = subprocess.check_output(
            f"kubectl --kubeconfig={kubeconfig} get all -n {ns} -o json",
            shell=True
        ).decode('utf-8')
        details['resources'] = json.loads(resources).get('items', [])
    except subprocess.CalledProcessError as e:
        print(f"Erro ao obter recursos para o namespace {ns}: {e}")
        details['resources'] = []

    try:
        # Obter descrição do namespace
        description = subprocess.check_output(
            f"kubectl --kubeconfig={kubeconfig} describe namespace {ns}",
            shell=True
        ).decode('utf-8')
        details['description'] = description
    except subprocess.CalledProcessError as e:
        print(f"Erro ao obter descrição para o namespace {ns}: {e}")
        details['description'] = "Erro ao descrever o namespace."

    try:
        # Obter quotas de recursos
        resource_quotas = subprocess.check_output(
            f"kubectl --kubeconfig={kubeconfig} get resourcequotas -n {ns} -o json",
            shell=True
        ).decode('utf-8')
        details['resource_quotas'] = json.loads(resource_quotas).get('items', [])
    except subprocess.CalledProcessError as e:
        print(f"Erro ao obter quotas de recursos para o namespace {ns}: {e}")
        details['resource_quotas'] = []

    return details

# Inicializar a planilha Excel
wb = openpyxl.Workbook()
ws = wb.active
ws.title = "Namespace Details"
headers = ["Namespace", "Resource Kind", "Resource Name", "Creation Timestamp", "Description", "Resource Quotas"]
ws.append(headers)

# Coletar e adicionar os detalhes dos namespaces na planilha e JSON data
namespace_data = []

for ns in namespaces:
    print(f"Processando namespace: {ns}")
    ns_details = get_namespace_details(ns)
    if ns_details['resources'] or ns_details['description'] or ns_details['resource_quotas']:
        first_row = True
        for resource in ns_details['resources']:
            row = [
                ns,
                resource.get('kind'),
                resource.get('metadata', {}).get('name'),
                resource.get('metadata', {}).get('creationTimestamp')
            ]
            if first_row:
                row.append(ns_details.get('description', ''))
                row.append(json.dumps(ns_details.get('resource_quotas', [])))
                first_row = False
            else:
                row.append('')
                row.append('')
            ws.append(row)
        namespace_data.append({
            "namespace": ns,
            "details": ns_details
        })

# Salvar o arquivo Excel
wb.save("Namespace_Details.xlsx")

# Salvar os dados em JSON
with open("Namespace_Details.json", "w") as json_file:
    json.dump(namespace_data, json_file, indent=4)

print("Arquivos Namespace_Details.xlsx e Namespace_Details.json criados com sucesso.")
