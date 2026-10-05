# sus-df-tracker

**MOTIVAÇÃO:** Na espera de uma cirurgia pelo SUS do Distrito Federal, cansei de entrar no site do [Ministério Público do Distrito Federal e Territórios](https://www.mpdft.mp.br/acompanhamento-sus-df/) para acompanhar minha posição na fila dos procedimentos pré-operatórios. Tendo em vista as visitas repetitivas ao site, pensei em transformar o procedimento em um pequeno projeto de treino para algumas funcionalidades em Python. 

## Sobre o Projeto
O `sus-df-tracker` é um script simples de automação que realiza consultas (`request`) no portal do MPDFT utilizando o número do Cartão Nacional de Saúde (CNS) específico direto na aplicação, salva o histórico das posições em arquivo e gera gráficos de evolução temporal.

## Ferramentas
#### Python
* Pandas
* Matplotlib
* Requests

## Desafios e Limitações
* Ausência de Acesso Oficial à API / Histórico: Por não haver acesso claro à documentação ou acesso oficial de desenvolvedor para a API do MPDFT, a plataforma retorna apenas a posição atual no momento da requisição.

**Solução Adotada (Persistência em Arquivo)**: Como a API não fornece o histórico passado da fila, a estratégia do projeto é realizar consultas periódicas e salvar os resultados localmente em um arquivo de texto (historico.txt). Dessa forma, o histórico é construído gradualmente ao longo do tempo para permitir a geração dos gráficos de evolução. 

**Solução Alternativa (Persistência em Banco de Dados)**: Mais trabalhosa e exigente em relação à consumo de recursos, mas igualmente interessante. 

## Funcionalidades que faltam ser implementadas
- [ ] Limpeza de dados (evitar valores repetidos) 
- [x] Gráfico com múltiplos procedimentos

---

#### Isenção de Responsabilidade (Disclaimer)
Este projeto foi desenvolvido exclusivamente para fins educacionais e de uso pessoal. Não possui vínculo oficial com o Ministério Público do Distrito Federal e Territórios (MPDFT) nem com a Secretaria de Saúde do DF (SES-DF). Respeita os termos de uso da plataforma original e evita fazer requisições em alta frequência para não sobrecarregar os servidores públicos.
