# 🤖 EngBot – Sistema Django

Este é o repositório oficial do **EngBot**, um sistema web desenvolvido com Django para automatizar tarefas de engenharia e geração de relatórios técnicos.

---

## 📁 Clonar o projeto

```bash
git clone https://github.com/keventapi/engbot.git
cd engbot
```

---

## 🐍 Criar ambiente virtual

### 🔹 Windows

```bash
python -m venv venv
```

### 🔹 Linux

```bash
python3 -m venv venv
```

---

## 🚀 Ativar o ambiente virtual

### 🔹 Windows (PowerShell)

```bash
.env\Scripts\Activate.ps1
```

### 🔹 Linux/macOS

```bash
source venv/bin/activate
```

---

## 📦 Instalar dependências

Certifique-se de estar na pasta onde está o `requirements.txt`, então rode:

```bash
pip install -r requirements.txt
```

---

## ⚙️ Rodar o projeto Django

### 🔹 Windows

```bash
cd nome_do_projeto
python manage.py migrate
python manage.py runserver
```

### 🔹 Linux

```bash
cd nome_do_projeto
python3 manage.py migrate
python3 manage.py runserver
```

---

## 🌐 Acessar a aplicação

Abra no navegador:

```
http://127.0.0.1:8000/chat/111
```
