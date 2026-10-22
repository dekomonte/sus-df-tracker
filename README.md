# :hospital: sus-df-tracker

![Status](https://img.shields.io/badge/Status-Em_Desenvolvimento-yellow?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.8+-blue?style=for-the-badge&logo=python&logoColor=white)

**MOTIVAÇÃO:** Na espera de uma cirurgia pelo SUS do Distrito Federal, cansei de entrar no site do [Ministério Público do Distrito Federal e Territórios](https://www.mpdft.mp.br/acompanhamento-sus-df/) para acompanhar minha posição na fila dos procedimentos pré-operatórios. Tendo em vista as visitas repetitivas ao site, pensei em transformar o procedimento em um pequeno projeto de treino para algumas funcionalidades em Python. 

## :bulb: Sobre 
O `sus-df-tracker` é um script simples de automação que realiza consultas via `requests` no portal do MPDFT utilizando o número do Cartão Nacional de Saúde (CNS) específico direto na aplicação, salva o histórico das posições em arquivo e gera gráficos de evolução temporal.

## :computer: Como executar

No terminal no seu diretório local, rode o comando: <br>
```bash
git clone https://github.com/dekomonte/sus-df-tracker.git
``` 

Vá para o diretório do projeto: <br>
```bash
cd sus-df-tracker
```

Instale as dependências do projeto: <br>
```bash
pip install -r requirements.txt
```

Execute o script: <br>
```bash
python fila_sus.py
```

## :wrench: :hammer: Tecnologias e Ferramentas

- **Linguagem:** Python
- **Bibliotecas:**
  - `requests` — Requisições HTTP para consulta dos dados.
  - `pandas` — Manipulação e estruturação do histórico.
  - `matplotlib` — Geração dos gráficos de evolução temporal.
- **Apoio de IA:** Google Gemini & Microsoft Copilot (auxílio na construção e otimização do código).

## Desafios e Limitações
* Falta de Acesso Oficial à API: por não haver acesso oficial à documentação da API do MPDFT, a plataforma retorna apenas a posição atual no momento da requisição. Problema: execução do código manualmente. 

**Solução Adotada (Persistência em Arquivo)**<br>
 A estratégia do projeto é realizar consultas periódicas e salvar os resultados localmente em um arquivo de texto (`historico.txt`). Dessa forma, o histórico é construído gradualmente ao longo do tempo para permitir a geração dos gráficos de evolução. 

**Solução Alternativa (Persistência em Banco de Dados)**<br>
 Mais trabalhosa e exigente em relação à consumo de recursos, mas igualmente interessante. 

## Melhorias Futuras
- [ ] Limpeza de dados (evitar valores repetidos) 
- [x] Gráfico com múltiplos procedimentos
- [ ] Automação de execução periódica (GitHub Actions ou Agendador de Tarefas)
- [ ] Log com erros

---

#### Isenção de Responsabilidade (Disclaimer)
Este projeto foi desenvolvido exclusivamente para fins educacionais e de uso pessoal. Não possui vínculo oficial com o Ministério Público do Distrito Federal e Territórios (MPDFT) nem com a Secretaria de Saúde do DF (SES-DF). Respeita os termos de uso da plataforma original e evita fazer requisições em alta frequência para não sobrecarregar os servidores públicos.
