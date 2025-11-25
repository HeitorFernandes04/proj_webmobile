# 📚 Plataforma de Cursos Online  
Projeto da disciplina de **Desenvolvimento Web Mobile**

Este projeto é uma **plataforma de curso online (LMS simples)** desenvolvida para a disciplina de Desenvolvimento Web Mobile.  
O sistema contempla:

- Backend em **Django** com **SQLite**
- Frontend web com **Django Templates + Bootstrap**
- Versão **mobile** em **Ionic** consumindo a API
- Implementação de **APIs REST** (Django REST Framework)
- **Autenticação** com login obrigatório para acesso à área do aluno
- **Testes automatizados** no backend (models, views e APIs)

---

## 🎯 Objetivo do Projeto

Criar uma plataforma onde um aluno possa:

1. Ver uma **página de vendas** do curso
2. **Cadastrar-se** na plataforma
3. **Realizar login**
4. Acessar uma **página de pagamento** e ativar seu plano
5. Navegar na **home da plataforma**, com:
   - Lista de **módulos do curso**
   - Progresso em cada módulo
6. Entrar em cada **módulo** e visualizar as **aulas**
7. Acessar a **página da aula em vídeo**, podendo:
   - Marcar aula como **concluída**
   - Atualizar seu **progresso** no módulo/curso
8. Acessar o **perfil**, visualizar informações da conta, plano e link para alterar senha

O **dono da plataforma** (administrador) consegue gerenciar todo o conteúdo pelo **Django Admin**:
- Cadastrar / editar / excluir cursos, módulos e aulas
- Definir planos de assinatura
- Acompanhar assinaturas dos alunos

---

## ✅ Requisitos da disciplina atendidos

- **Frontend Web**
  - Páginas públicas (landing / vendas, login, cadastro)
  - Páginas autenticadas (home, módulos, aulas, perfil, plano)
  - Layout usando **HTML + CSS + Bootstrap**

- **Backend**
  - Desenvolvido em **Django**
  - Modelagem de dados completa (usuários, cursos, módulos, aulas, assinaturas, progresso)

- **Banco de Dados**
  - Utilização de **SQLite** (padrão do Django, simples para desenvolvimento acadêmico)

- **Versão Mobile**
  - Aplicativo em **Ionic** consumindo a API da plataforma
  - Telas principais: login, lista de módulos, lista de aulas e visualização da aula

- **APIs**
  - Implementadas com **Django REST Framework**
  - Endpoints para autenticação, módulos, aulas, progresso, perfil e plano

- **Segurança / Required Login**
  - Áreas internas protegidas com `login_required` / permissões do DRF
  - Apenas usuários autenticados e com assinatura ativa acessam o conteúdo do curso

- **Testes**
  - Testes de:
    - Models (criação e relacionamento)
    - Views (proteção por login, fluxo de acesso)
    - APIs (status HTTP, autenticação, retorno de dados)

---

## 🧱 Arquitetura do Projeto

Estrutura sugerida do repositório:

```bash
plataforma-cursos-online/
│
├─ backend/                # Projeto Django
│  ├─ lms_project/         # Configurações principais do Django
│  ├─ accounts/            # App de usuários/autenticação
│  ├─ courses/             # App de cursos, módulos, aulas e progresso
│  ├─ billing/             # App de planos e assinaturas
│  ├─ api/                 # App com as APIs (DRF)
│  ├─ templates/           # Templates HTML (páginas web)
│  ├─ static/              # Arquivos estáticos (CSS, JS, imagens)
│  └─ manage.py
│
├─ mobile/                 # Projeto Ionic (versão mobile)
│  ├─ src/
│  └─ ...
│
└─ README.md


Projeto: Plataforma de Curso – Social Media 10x

Aluno: Heitor Fernandes Carrijo

Curso: Ciencia da computação

Disciplina: Desenvolvimento Web Mobile

Professor(a): Thiago Almeida
