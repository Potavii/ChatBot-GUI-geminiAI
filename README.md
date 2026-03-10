*GEMINI CHATBOT DESKTOP*
 
*Descrição*
Este é um assistente virtual desktop desenvolvido em Python, que integra a interface gráfica moderna do Tkinter com a inteligência artificial de ponta do Google Gemini. O objetivo é oferecer uma experiência de chat fluida e inteligente diretamente no sistema operacional.

*Funcionalidades*
IA Generativa: Respostas em tempo real integradas via API oficial.

Interface Moderna: UI construída com Tkinter, suportando Dark/Light mode.

Processamento Assíncrono: Uso de Multithreading para evitar o congelamento da interface durante as requisições à API.

Gestão de Ambiente: Segurança das chaves de API utilizando variáveis de ambiente (.env).

*Tecnologias Utilizadas*
Python 3.x

Tkinter: Interface gráfica de usuário.

Google Generative AI SDK: Integração com o modelo Gemini.

Threading: Gerenciamento de concorrência.

*Como Instalar e Rodar*
Clone o repositório.

Instale as dependências:
*No terminal*
pip install -r requirements.txt

*pegue sua API KEY DO Gemini em https://aistudio.google.com/app/api-keys*
*Crie um arquivo .env na raiz do projeto e adicione sua chave:*
O que escrever no .env
GEMINI_API_KEY=sua_chave_aqui
Execute o projeto:

*Para executar o prjeto*
python main.py
