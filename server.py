from flask import Flask, request, send_from_directory
import subprocess
import atexit

import os
import signal


app = Flask(__name__, static_folder='.', static_url_path='')

# ===== NOVO: controle visual do cursor =====

def set_remote_cursor():
    try:
        subprocess.run([
            "gsettings", "set",
            "org.gnome.desktop.interface",
            "cursor-size", "48"
        ], check=False)

        subprocess.run([
            "gsettings", "set",
            "org.gnome.desktop.interface",
            "cursor-theme", "Bibata-Modern-Amber"
        ], check=False)

        print("[CURSOR] Cursor REMOTO ativado (grande e colorido)")
    except Exception as e:
        print(f"[ERRO] ao ativar cursor remoto: {e}")

def restore_cursor():
    try:
        subprocess.run([
            "gsettings", "set",
            "org.gnome.desktop.interface",
            "cursor-size", "24"
        ], check=False)

        subprocess.run([
            "gsettings", "set",
            "org.gnome.desktop.interface",
            "cursor-theme", "Yaru"
        ], check=False)

        print("[CURSOR] Cursor restaurado para padrão")
    except Exception as e:
        print(f"[ERRO] ao restaurar cursor: {e}")


# ===== ROTAS ORIGINAIS (INALTERADAS) =====

@app.route('/')
def home():
    print("Acessaram a página principal 🔍")
    return send_from_directory('.', 'index.html')

@app.route('/move', methods=['POST'])
def move_mouse():
    data = request.get_json()
    dx = int(data.get('dx', 0))
    dy = int(data.get('dy', 0))
    print(f"[MOUSE] dx={dx}, dy={dy}")
    try:
        subprocess.run(['xdotool', 'mousemove_relative', '--', str(dx), str(dy)], check=True)
    except Exception as e:
        print(f"[ERRO] movimento mouse: {e}")
    return 'Movimento executado'

@app.route('/key', methods=['POST'])
def press_key():
    data = request.get_json()
    key = data.get('key', '')
    print(f"[TECLADO] Tecla recebida: {key}")
    try:
        if key == ' ':
            subprocess.run(['ydotool', 'type', ' '], check=True)
        elif key.lower() == 'enter':
            subprocess.run(['ydotool', 'key', 'KEY_ENTER'], check=True)
        elif key.lower() == 'backspace':
            subprocess.run(['ydotool', 'key', 'KEY_BACKSPACE'], check=True)
        else:
            subprocess.run(['ydotool', 'type', key], check=True)
    except Exception as e:
        print(f"[ERRO] ao digitar: {e}")
    return f'Tecla {key} enviada'

@app.route('/position')
def get_position():
    try:
        pos = subprocess.run(['ydotool', 'mouse-location'], capture_output=True, text=True, check=True)
        print(f"[POSIÇÃO] {pos.stdout.strip()}")
        return pos.stdout.strip()
    except Exception as e:
        print(f"[ERRO] posição mouse: {e}")
        return 'Erro'

@app.route('/click', methods=['POST'])
def click_mouse():
    subprocess.run(['ydotool', 'click', '1'])
    return 'Clique simples'

@app.route('/doubleclick', methods=['POST'])
def double_click():
    subprocess.run(['ydotool', 'click', '1'])
    subprocess.run(['ydotool', 'click', '1'])
    return 'Duplo clique'

@app.route('/rightclick', methods=['POST'])
def right_click():
    subprocess.run(['ydotool', 'click', '3'])
    return 'Botão direito'

@app.route('/shutdown', methods=['POST'])
def shutdown():
    print("[SERVER] Encerramento solicitado via web")

    restore_cursor()  # volta cursor ao normal

    os.kill(os.getpid(), signal.SIGINT)
    return 'Servidor encerrando'


if __name__ == '__main__':
    set_remote_cursor()
    atexit.register(restore_cursor)
    app.run(host='0.0.0.0', port=9876, debug=False, use_reloader=False)



