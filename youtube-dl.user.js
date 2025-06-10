// ==UserScript==
// @name         YouTube Downloader - HPuglia
// @namespace    http://tampermonkey.net/
// @version      1.2
// @description  Baixar vídeo do YouTube via backend local com barra de progresso
// @author       Henrique Puglia
// @match        https://www.youtube.com/watch*
// @grant        GM_xmlhttpRequest
// @connect      127.0.0.1
// @license      MIT
// @homepage     https://github.com/hpuglia/YoutubeDownloader-hpuglia
// @supportURL   https://github.com/hpuglia/YoutubeDownloader-hpuglia/issues
// @updateURL    https://raw.githubusercontent.com/hpuglia/YoutubeDownloader-hpuglia/main/youtube-dl.user.js
// @downloadURL  https://raw.githubusercontent.com/hpuglia/YoutubeDownloader-hpuglia/main/youtube-dl.user.js
// ==/UserScript==

(function () {
    'use strict';

    function createModal() {
        let modal = document.createElement('div');
        modal.id = 'yt-dl-status';
        modal.style = `
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            color: white;
            padding: 15px 20px;
            border-radius: 10px;
            z-index: 9999;
            font-family: sans-serif;
            font-size: 14px;
        `;
        modal.textContent = '⏳ Iniciando download...';
        document.body.appendChild(modal);
    }

    function updateModal(text) {
        let modal = document.getElementById('yt-dl-status');
        if (modal) modal.textContent = text;
    }

    function removeModal() {
        let modal = document.getElementById('yt-dl-status');
        if (modal) modal.remove();
    }

    function createDownloadButton() {
        if (document.getElementById('yt-local-download')) return;

        const button = document.createElement('button');
        button.id = 'yt-local-download';
        button.textContent = '⬇️ Baixar Vídeo';
        button.style = `
            padding: 10px 20px;
            background: #007aff;
            color: white;
            font-size: 14px;
            border: none;
            border-radius: 10px;
            margin-left: 10px;
            cursor: pointer;
        `;

        button.onclick = function () {
            const videoUrl = window.location.href;
            createModal();

            GM_xmlhttpRequest({
                method: "GET",
                url: `http://127.0.0.1:5000/download?url=${encodeURIComponent(videoUrl)}`,
                onload: function (response) {
                    const json = JSON.parse(response.responseText);
                    const id = encodeURIComponent(json.id);

                    let interval = setInterval(() => {
                        GM_xmlhttpRequest({
                            method: "GET",
                            url: `http://127.0.0.1:5000/status?id=${id}`,
                            onload: function (res) {
                                const stat = JSON.parse(res.responseText).status;
                                updateModal(`📥 ${stat}`);
                                if (stat.includes("Concluído")) {
                                    clearInterval(interval);
                                    setTimeout(removeModal, 3000);
                                }
                            }
                        });
                    }, 2000);
                },
                onerror: function (err) {
                    updateModal("❌ Erro ao conectar com backend.");
                    console.error(err);
                    setTimeout(removeModal, 4000);
                }
            });
        };

        const target = document.querySelector('#top-level-buttons-computed');
        if (target) target.appendChild(button);
    }

    const observer = new MutationObserver(createDownloadButton);
    observer.observe(document.body, { childList: true, subtree: true });
})();
