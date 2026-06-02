import os
import FreeSimpleGUI as sg
import yt_dlp

sg.theme('DefaultNoMoreNagging')

layout = [
    [sg.Text('Insira a URL do vídeo do YouTube:')],
    [sg.Input(key='-URL-', size=(50, 1))],
    [sg.Button('Download')]
]

window = sg.Window('Baixar Vídeo do YouTube', layout)

while True:
    event, values = window.read()
    if event == sg.WINDOW_CLOSED:
        break
    elif event == 'Download':
        url = values['-URL-']
        if not url.strip():
            sg.popup_error('Por favor, insira uma URL válida.', title='Erro')
            continue
        try:
            caminho_salvar = os.path.join(os.path.expanduser("~"), "Videos")
            if not os.path.exists(caminho_salvar):
                os.makedirs(caminho_salvar)

            # Configurações do yt-dlp para baixar um formato único (evita precisar do ffmpeg)
            ydl_opts = {
                'format': 'best[ext=mp4]/best',
                'outtmpl': os.path.join(caminho_salvar, '%(title)s.%(ext)s'),
                'quiet': True,
                'no_warnings': True,
            }

            # Mostra uma mensagem rápida indicando o início do download
            sg.popup_quick_message('Baixando o vídeo... Aguarde um momento.', background_color='#1c1c1c', text_color='white')

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                titulo = info.get('title', 'Vídeo')

            sg.popup(f'O vídeo "{titulo}" foi baixado com sucesso!', title='Download Concluído')
        except Exception as e:
            sg.popup_error(f'Ocorreu um erro durante o download:\n{str(e)}', title='Erro')

window.close()