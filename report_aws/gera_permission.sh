#!/bin/bash

# Dependências necessárias: jq

# Arquivos de saída
json_output="users_permissions.json"
csv_output="users_permissions.csv"

# Inicializar arquivos de saída
echo "[]" > $json_output
echo "UserName,Policies,Groups" > $csv_output

# Listar todos os usuários
users=$(aws iam list-users --query 'Users[*].UserName' --output text)

# Função para obter políticas anexadas diretamente ao usuário
get_user_policies() {
    user_name=$1
    user_policies=$(aws iam list-attached-user-policies --user-name $user_name --query 'AttachedPolicies[*].PolicyName' --output text | tr '\n' ',')
    echo $user_policies
}

# Função para obter políticas anexadas aos grupos do usuário
get_group_policies() {
    user_name=$1
    groups=$(aws iam list-groups-for-user --user-name $user_name --query 'Groups[*].GroupName' --output text)
    group_policies=""
    for group in $groups; do
        policies=$(aws iam list-attached-group-policies --group-name $group --query 'AttachedPolicies[*].PolicyName' --output text | tr '\n' ',')
        group_policies+="$group: $policies; "
    done
    echo $group_policies
}

# Loop através de cada usuário
for user in $users; do
    echo "Processando usuário: $user"

    # Obter políticas anexadas diretamente ao usuário
    user_policies=$(get_user_policies $user)
    if [ -z "$user_policies" ]; then
        user_policies="Nenhuma"
    fi

    # Obter políticas anexadas aos grupos do usuário
    group_policies=$(get_group_policies $user)
    if [ -z "$group_policies" ]; then
        group_policies="Nenhuma"
    fi

    # Adicionar ao arquivo JSON
    jq ". += [{UserName: \"$user\", Policies: \"$user_policies\", Groups: \"$group_policies\"}]" $json_output > tmp.json && mv tmp.json $json_output

    # Adicionar ao arquivo CSV
    echo "$user,\"$user_policies\",\"$group_policies\"" >> $csv_output
done

echo "Informações de permissões dos usuários foram salvas em $json_output e $csv_output"

