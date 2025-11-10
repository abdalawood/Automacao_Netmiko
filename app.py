from flask import Flask, render_template, request, render_template_string
from netmiko import ConnectHandler
from dotenv import load_dotenv
import os

# Carrega variáveis do .env
load_dotenv()

app = Flask(__name__)

# Configurações do dispositivo via .env (SEGURANÇA)
CISCO_DEVICE = {
    'device_type': 'cisco_ios',
    'host': os.getenv('ROUTER_IP'),
    'username': os.getenv('ROUTER_USER'),
    'password': os.getenv('ROUTER_PASS'),
    'secret': os.getenv('ROUTER_PASS'),  # para enable
    'port': 22, 
    'timeout': 15
}

# --- Rota 1: Página Inicial ---
@app.route('/')
def home():
    return render_template('form.html')

# --- Rota 2: Configurar Loopback ---
@app.route('/configurar', methods=['POST'])
def configurar_loopback():
    loopback_id = request.form['loopback_id']
    loopback_ip = request.form['loopback_ip']
    loopback_mask = request.form['loopback_mask']
    loopback_desc = request.form['loopback_desc']

    commands_to_send = [
        f'interface loopback {loopback_id}',
        f'description {loopback_desc}',
        f'ip address {loopback_ip} {loopback_mask}'
    ]

    try:
        net_connect = ConnectHandler(**CISCO_DEVICE)
        net_connect.enable()
        output_config = net_connect.send_config_set(commands_to_send)
        output_verify = net_connect.send_command(f"show running-config interface loopback {loopback_id}")
        net_connect.disconnect()

        resultado = f"Sucesso! Loopback {loopback_id} configurada."
        detalhes = f"""
            <h3>Configuração Aplicada:</h3>
            <pre>{output_verify}</pre>
            <h3>Log de Comandos:</h3>
            <pre>{output_config}</pre>
        """

    except Exception as e:
        resultado = "Erro na configuração. Verifique IP, credenciais ou SSH."
        detalhes = f"<pre>{str(e)}</pre>"

    return render_template_string(f"""
        <h1>Resultado</h1>
        <p style='color: green;'>{resultado}</p>
        {detalhes}
        <p><a href='/'>Voltar</a></p>
    """)

# --- Rota 3: Formulário de Remoção ---
@app.route('/remover')
def remover_form():
    return render_template('remove_form.html')

# --- Rota 4: Processar Remoção ---
@app.route('/remover_loopback', methods=['POST'])
def remover_loopback():
    loopback_id = request.form['loopback_id_remover']

    if not loopback_id.isdigit():
        return "Erro: ID deve ser numérico."

    commands_to_send = [f'no interface loopback {loopback_id}']

    try:
        net_connect = ConnectHandler(**CISCO_DEVICE)
        net_connect.enable()
        output_config = net_connect.send_config_set(commands_to_send)
        
        # Verifica se foi removida
        verify = net_connect.send_command(f"show running-config interface loopback {loopback_id}")
        net_connect.disconnect()

        if "Invalid" in verify or len(verify.strip()) < 50:
            resultado = f"Sucesso! Loopback {loopback_id} removida."
        else:
            resultado = f"Atenção! Loopback {loopback_id} ainda existe."

        detalhes = f"""
            <h3>Comandos Enviados:</h3>
            <pre>{output_config}</pre>
            <h3>Verificação:</h3>
            <pre>{verify}</pre>
        """

    except Exception as e:
        resultado = "Erro na remoção."
        detalhes = f"<pre>{str(e)}</pre>"

    return render_template_string(f"""
        <h1>Resultado da Remoção</h1>
        <p style='color: {"green" if "Sucesso" in resultado else "red"};'>{resultado}</p>
        {detalhes}
        <hr>
        <p>
            <a href='/'>Configurar</a> | 
            <a href='/remover'>Remover Outra</a> | 
            <a href='/status'>Ver Status</a>
        </p>
    """)

# --- Rota 5: Status do Roteador ---
@app.route('/status')
def status():
    try:
        net_connect = ConnectHandler(**CISCO_DEVICE)
        output = net_connect.send_command('show ip interface brief')
        net_connect.disconnect()
        return render_template('status.html', status_output=output)
    except Exception as e:
        error = f"Erro: {e}"
        return render_template('status.html', status_output=error)

# --- Inicia o servidor ---
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)