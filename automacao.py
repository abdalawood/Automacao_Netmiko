from netmiko import ConnectHandler

# --- 1. Dados de Conexão (Fixo) ---
cisco_device = {
    'device_type': 'cisco_ios',
    'host': '192.168.180.129', # O IP do seu vIOS
    'username': 'netmiko',
    'password': 'cisco',
    'port': 22, 
    'timeout': 15 
}

# --- 2. Coletar Dados da Caixa de Diálogo (Entrada do Usuário) ---
print("\n--- Configuração Interativa da Loopback ---")
loopback_id = input("Digite o Número da Loopback (ex: 100): ")
loopback_ip = input("Digite o Endereço IP (ex: 192.168.255.1): ")
loopback_mask = input("Digite a Máscara de Sub-rede (ex: 255.255.255.255): ")
loopback_desc = input("Digite a Descrição (ex: GERENCIAMENTO_NOVO): ")
print("---------------------------------------------------\n")

# --- 3. Criar a Lista de Comandos Dinamicamente ---
commands_to_send = [
    f'interface loopback {loopback_id}',
    f'description {loopback_desc}',
    f'ip address {loopback_ip} {loopback_mask}',
    'end'
]

# --- 4. Bloco de Execução (Try/Except) ---
print("Tentando conectar e enviar comandos...") 

try:
    net_connect = ConnectHandler(**cisco_device)
    print("✅ Conexão SSH bem-sucedida! Enviando comandos de configuração...")

    # Envia a lista de comandos criada dinamicamente
    output = net_connect.send_config_set(commands_to_send)
    
    # Comando de verificação para o Loopback configurado
    verify_command = f"show running-config interface loopback {loopback_id}"
    verify_output = net_connect.send_command(verify_command)

    print("\n--- Resultado da Automação (Retorno do Roteador) ---")
    print(verify_output) # Exibe a configuração da nova Loopback
    
    net_connect.disconnect()
    print("\n✅ Automação FINALIZADA e conexão fechada. Verifique o roteador.")

except Exception as e:
    print(f"\n❌ ERRO FATAL: {e}")