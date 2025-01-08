#!/bin/bash

# Dependências necessárias: jq

# Arquivos de saída
json_output="users_info.json"
csv_output="users_info.csv"

# Inicializar arquivos de saída
echo "[]" > $json_output
echo "UserName,UserId,Arn,CreateDate,LastLogin,Groups,Tags" > $csv_output

# Listar todos os usuários
users=$(aws iam list-users --query 'Users[*].UserName' --output text)

# Função para calcular dias desde o último login
calculate_days_since_login() {
    last_login_date=$1
    current_date=$(date -u +"%Y-%m-%dT%H:%M:%SZ")
    diff=$(( ( $(date -d "$current_date" +%s) - $(date -d "$last_login_date" +%s) ) / 86400 ))
    echo "$diff"
}

# Loop através de cada usuário
for user in $users; do
    # Obter detalhes do usuário
    user_info=$(aws iam get-user --user-name $user)

    # Extrair informações básicas
    user_name=$(echo $user_info | jq -r '.User.UserName')
    user_id=$(echo $user_info | jq -r '.User.UserId')
    arn=$(echo $user_info | jq -r '.User.Arn')
    create_date=$(echo $user_info | jq -r '.User.CreateDate')
    last_login=$(echo $user_info | jq -r '.User.PasswordLastUsed')

    if [ "$last_login" = "null" ]; then
        last_login="Nunca logado"
        days_since_login="N/A"
    else
        days_since_login=$(calculate_days_since_login $last_login)
        last_login="${last_login} (${days_since_login} dias atrás)"
    fi

    # Listar grupos para o usuário
    groups=$(aws iam list-groups-for-user --user-name $user --query 'Groups[*].GroupName' --output json)
    groups_list=$(echo $groups | jq -r '. | join(",")')

    # Listar tags para o usuário
    tags=$(aws iam list-user-tags --user-name $user --query 'Tags' --output json)
    tags_list=$(echo $tags | jq -r '.[] | "$$.Key):$$.Value)"' | paste -sd "," -)

    # Adicionar ao arquivo JSON
    jq ". += [{UserName: \"$user_name\", UserId: \"$user_id\", Arn: \"$arn\", CreateDate: \"$create_date\", LastLogin: \"$last_login\", Groups: $groups, Tags: $tags}]" $json_output > tmp.json && mv tmp.json $json_output

    # Adicionar ao arquivo CSV
    echo "$user_name,$user_id,$arn,$create_date,\"$last_login\",\"$groups_list\",\"$tags_list\"" >> $csv_output
done

echo "Informações dos usuários foram salvas em $json_output e $csv_output"

