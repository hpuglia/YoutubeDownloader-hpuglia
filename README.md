# 🎬 YouTube Downloader - Interface Gráfica com `yt-dlp`

![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)
![Flask](https://img.shields.io/badge/Flask-Web%20App-lightgrey?logo=flask)
![yt-dlp](https://img.shields.io/badge/yt--dlp-powered-orange?logo=youtube)
![Windows](https://img.shields.io/badge/.exe-Suportado-blue?logo=windows)
![License](https://img.shields.io/badge/Licença-MIT-green)

Este projeto oferece uma interface gráfica moderna, desenvolvida com **Flask**, para baixar vídeos do YouTube utilizando o poderoso `yt-dlp`. Ele conta com funcionalidades como:

- Status do download em tempo real  
- Título automático do vídeo  
- Botões úteis e intuitivos  
- Empacotamento em `.exe` para uso direto no Windows  

---

## 🔧 Requisitos

Para rodar o projeto no modo de desenvolvimento, você precisará de:

- Python 3.10 ou superior  
- pip (gerenciador de pacotes do Python)  
- Navegador moderno (Google Chrome, Firefox, etc.)  
- Extensão **Tampermonkey** instalada no navegador  

---

## 📦 Instalação e Configuração

1. Instale o [Python](https://www.python.org/downloads/) e o `pip`.  
2. No navegador Google Chrome, instale a extensão [Tampermonkey](https://www.tampermonkey.net/).  
3. Após instalar o Tampermonkey, adicione o script de integração com o YouTube:  
   👉 [`youtube-dl.user.js`](https://raw.githubusercontent.com/hpuglia/YoutubeDownloader-hpuglia/main/youtube-dl.user.js)

---

## ▶️ Como Utilizar

1. Execute o arquivo `yt_backend.exe` (ou `yt_backend.py` se estiver em modo desenvolvimento).  
2. Abra um vídeo no YouTube.  
3. Um botão azul aparecerá abaixo do player de vídeo. Clique nele para iniciar o download.  
4. O vídeo será enviado ao sistema `yt_backend`, onde você poderá:  
   - Ver o **status do download**  
   - Verificar ou alterar a **pasta de saída**  
   - Abrir a pasta diretamente após o download  

✅ Os vídeos são baixados sempre com a **melhor qualidade disponível**.

---

## 💜 Apoie este Projeto

Se este projeto foi útil para você, considere apoiar:  
🔗 [https://nubank.com.br/cobrar/na7j5/6847d4fc-4652-4c8c-9949-d499d2338b2a](https://nubank.com.br/cobrar/na7j5/6847d4fc-4652-4c8c-9949-d499d2338b2a)
