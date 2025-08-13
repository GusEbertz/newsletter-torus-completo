# Newsletter Torus Automações

Sistema completo de newsletter com frontend React e backend Flask, desenvolvido para captura e gerenciamento de emails de assinantes.

## 🚀 Características

- **Frontend React** com Tailwind CSS 4.0
- **Backend Flask** com API RESTful
- **Banco SQLite** para armazenamento
- **Validação robusta** de emails
- **Medidas de segurança** (rate limiting, sanitização)
- **Design responsivo** e moderno
- **CORS habilitado** para integração frontend-backend

## 📋 Pré-requisitos

- Python 3.11+
- Node.js 20+
- npm ou yarn

## 🛠️ Instalação e Configuração

### 1. Clonar/Extrair o projeto

```bash
# Se você recebeu um arquivo ZIP, extraia-o
unzip newsletter-torus.zip
cd newsletter-backend
```

### 2. Configurar o Backend (Flask)

```bash
# Ativar ambiente virtual
source venv/bin/activate

# Instalar dependências (já incluídas no venv)
pip install -r requirements.txt

# O banco SQLite será criado automaticamente na primeira execução
```

### 3. Executar a aplicação

```bash
# Dentro do diretório newsletter-backend
source venv/bin/activate
python src/main.py
```

A aplicação estará disponível em: `http://localhost:5000`

## 📁 Estrutura do Projeto

```
newsletter-backend/
├── venv/                    # Ambiente virtual Python
├── src/
│   ├── models/
│   │   └── subscriber.py    # Modelo de dados dos assinantes
│   ├── routes/
│   │   └── newsletter.py    # Rotas da API
│   ├── static/              # Arquivos do frontend React (buildados)
│   │   ├── index.html
│   │   └── assets/
│   ├── database/
│   │   └── app.db          # Banco SQLite (criado automaticamente)
│   └── main.py             # Arquivo principal do Flask
├── requirements.txt         # Dependências Python
└── README.md               # Esta documentação
```

## 🔌 API Endpoints

### POST /api/subscribe
Inscrever um novo email na newsletter.

**Corpo da requisição:**
```json
{
  "email": "usuario@exemplo.com"
}
```

**Respostas:**
- `201`: Inscrição realizada com sucesso
- `409`: Email já cadastrado
- `400`: Email inválido
- `429`: Rate limit excedido

### POST /api/unsubscribe
Cancelar inscrição de um email.

**Corpo da requisição:**
```json
{
  "email": "usuario@exemplo.com"
}
```

### GET /api/stats
Obter estatísticas básicas dos assinantes.

**Resposta:**
```json
{
  "active_subscribers": 150,
  "total_all_time": 200
}
```

## 🔒 Recursos de Segurança

- **Rate Limiting**: Máximo 5 tentativas por IP em 5 minutos
- **Validação de Email**: Regex rigoroso para formato de email
- **Sanitização**: Emails são limpos e convertidos para minúsculo
- **Prevenção de Duplicatas**: Verificação de emails já cadastrados
- **CORS Configurado**: Permite requisições do frontend

## 🎨 Frontend

O frontend foi desenvolvido em React com:
- **Tailwind CSS 4.0** para estilização
- **Validação em tempo real** de emails
- **Feedback visual** para o usuário
- **Design responsivo** para mobile e desktop
- **Loading states** durante requisições
- **Tratamento de erros** com mensagens amigáveis

## 🗄️ Banco de Dados

### Tabela: subscribers

| Campo | Tipo | Descrição |
|-------|------|-----------|
| id | INTEGER | Chave primária |
| email | VARCHAR(120) | Email do assinante (único) |
| subscribed_at | DATETIME | Data/hora da inscrição |
| is_active | BOOLEAN | Status da inscrição |
| ip_address | VARCHAR(45) | IP do assinante |

## 🚀 Deploy

Para deploy em produção:

1. **Configure um servidor WSGI** (Gunicorn, uWSGI)
2. **Use um servidor web** (Nginx, Apache) como proxy reverso
3. **Configure variáveis de ambiente** para produção
4. **Use um banco mais robusto** se necessário (PostgreSQL, MySQL)

Exemplo com Gunicorn:
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 src.main:app
```

## 🔧 Desenvolvimento

### Modificar o Frontend

Se precisar alterar o frontend:

1. Vá para o diretório original do React (`newsletter04/`)
2. Faça as alterações necessárias
3. Execute `npm run build`
4. Copie os arquivos de `dist/` para `newsletter-backend/src/static/`

### Adicionar Novos Endpoints

1. Crie novas rotas em `src/routes/newsletter.py`
2. Registre no `src/main.py` se necessário
3. Atualize a documentação

## 📞 Suporte

Para dúvidas ou suporte:
- Instagram: [@torusautomacoes](https://www.instagram.com/torusautomacoes)
- Email: contato@torusautomacoes.com

## 📄 Licença

Este projeto foi desenvolvido para Torus Automações. Todos os direitos reservados.

---

**Desenvolvido com ❤️ para Torus Automações**

