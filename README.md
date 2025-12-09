# Hand Geometry Detector 🖐️

Detector de formas geométricas usando as mãos em tempo real com OpenCV e CVZone.

## 📋 Descrição

Este projeto usa visão computacional para detectar suas mãos através da webcam e identificar formas geométricas formadas pelos dedos indicadores e polegares de ambas as mãos.

## 🎯 Formas Detectadas

O sistema identifica automaticamente as seguintes formas geométricas:

- **🟩 QUADRADO** - Todos os lados iguais + ângulos de 90°
- **🟦 RETÂNGULO** - Lados opostos iguais + ângulos de 90°
- **💎 LOSANGO** - Todos os lados iguais + ângulos diferentes de 90°
- **🔷 PARALELOGRAMO** - Lados opostos iguais + ângulos diferentes de 90°
- **📐 TRAPÉZIO** - Apenas um par de lados paralelos
- **🔺 TRIÂNGULO** - Um dos lados muito pequeno (forma colapsada)
- **⬡ PENTÁGONO** - Forma irregular com variação moderada

## 🚀 Como Rodar

### 1. Pré-requisitos

- Python 3.10 (recomendado)
- Webcam funcionando

### 2. Criar ambiente virtual (venv)

```powershell
# Criar venv com Python 3.10
py -3.10 -m venv .venv

# Ativar o venv (PowerShell)
.\.venv\Scripts\Activate.ps1
```

Se der erro de política de execução:
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

### 3. Instalar dependências

```powershell
pip install -r requirements.txt
```

### 4. Executar o programa

```powershell
python main.py
```

Ou diretamente pelo executável do venv:
```powershell
.\.venv\Scripts\python.exe main.py
```

### 5. Usar o detector

1. Coloque ambas as mãos na frente da câmera
2. Use os dedos **polegar** e **indicador** de cada mão para formar formas
3. O sistema detectará automaticamente a forma geométrica
4. Pressione **'q'** para sair

## 📦 Dependências

- `opencv-python` - Processamento de imagem e captura de vídeo
- `cvzone` - Detecção de mãos facilitada
- `mediapipe` - Engine de detecção de landmarks das mãos

## 🎨 Visualização

O programa mostra em tempo real:
- **Linhas verdes** conectando os dedos indicadores
- **Linhas vermelhas** conectando os polegares
- **Linhas cinzas** conectando polegar-indicador da mesma mão
- **Medidas dos 4 lados** do quadrilátero formado (L1, L2, L3, L4)
- **Nome da forma detectada** em destaque com cor correspondente

## 🛠️ Estrutura do Projeto

```
HandDetector/
├── main.py          # Código principal
├── requirements.txt # Dependências
├── README.md        # Este arquivo
└── .venv/           # Ambiente virtual (não commitar)
```

## 📝 Notas

- O detector funciona melhor com boa iluminação
- Mantenha as mãos a uma distância razoável da câmera (50-100cm)
- As formas não precisam ser perfeitas - há tolerância de ~20% nas medidas
- O sistema analisa ângulos e proporções reais dos 4 pontos formados pelos dedos

## 🤝 Contribuindo

Sinta-se livre para abrir issues ou pull requests com melhorias!

## 📄 Licença

MIT License - Use livremente!

---

**Desenvolvido com ❤️ usando Python, OpenCV e CVZone**
