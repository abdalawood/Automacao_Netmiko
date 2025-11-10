# Automação Cisco com Python (Flask + Netmiko)

![Python](https://img.shields.io/badge/Python-3.9%2B-blue)
![Flask](https://img.shields.io/badge/Flask-2.0%2B-green)
![Netmiko](https://img.shields.io/badge/Netmiko-4.0%2B-orange)

Interface web para **configurar e remover Loopbacks** em roteadores Cisco via SSH.

## Funcionalidades
- Criar Loopback com IP, máscara e descrição
- Remover Loopback com verificação
- Ver status com `show ip interface brief`

## Como usar
```bash
git clone https://github.com/abdalawood/Automacao_Netmiko.git
cd Automacao_Netmiko
cp .env.example .env
# Edite o .env com suas credenciais
pip install flask netmiko python-dotenv
python app.py