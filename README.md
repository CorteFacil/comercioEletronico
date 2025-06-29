# Hackathon - Análise de Debate

## Como rodar o projeto em qualquer computador

### 1. Instale o Python 3.10 ou superior

### 2. Instale as dependências do projeto
Abra o terminal na pasta do projeto e execute:

```
pip install -r requirements.txt
```

### 3. Instale o ffmpeg (necessário para o Whisper)
- Baixe o ffmpeg em: https://www.gyan.dev/ffmpeg/builds/ffmpeg-release-essentials.zip
- Extraia o arquivo e adicione o caminho `C:\ffmpeg\bin` à variável de ambiente PATH do Windows.
- Teste no terminal: `ffmpeg -version`

### 4. Rode cada etapa do projeto

- **Baixar áudio do YouTube:**
  ```
  python baixar_audio.py
  ```
- **Transcrever áudio:**
  ```
  python transcrever_whisper.py
  ```
- **Separar falas por candidato:**
  ```
  python separar_falas.py
  ```
- **Gerar nuvem de palavras:**
  ```
  python gerar_nuvem.py
  ```
- **Abrir dashboard interativo (Streamlit):**
  ```
  streamlit run app_dashboard.py
  ```
- **Abrir dashboard profissional (Dash):**
  ```
  python dashboard_dash.py
  ```

Pronto! O projeto estará funcionando em qualquer computador seguindo esses passos.

---

### Dependências utilizadas

- yt-dlp
- openai-whisper
- ffmpeg-python
- streamlit
- wordcloud
- matplotlib
- dash
- dash-bootstrap-components
- plotly
- pandas
- numpy
- pillow
- nltk

Certifique-se de rodar `pip install -r requirements.txt` para instalar todas as dependências.
#   c o m e r c i o E l e t r o n i c o  
 