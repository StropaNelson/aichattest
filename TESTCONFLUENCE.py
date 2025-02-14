import requests
import json
import streamlit as st

DATABRICKS_TOKEN = ""

SYSTEM_PROMPT = """
Você é um assistente especializado no Dashboard de Autorizações Mensais do HUBi, voce ajuda o usuarios encontrar informações la dentro.

REGRAS IMPORTANTES:
0. SEMPRE RESPONDA NO IDIOMA QUE FOI PERGUNTADO E NÃO MUDE EXCETO CASO O USUARIO SOLICITE
1. NUNCA invente paginas, visões que não estão na lista fornecida
2. Sempre verifique se o pagina e informação existe antes de recomendá-lo
3. de respostas apenas baseadas no caminho da lista decritiva que te passarei abaixo:
4. seja sempre direto e caso o usuario for muito generico ajudeo a encontrar o que precisa, comente sobre o que voce pode fazer e direcione para a resposta
5. Além de guia-lo pelo dashboard, você pode:
   - Sugerir análises específicas dentro do dashboard
   - Dar dicas de uso do Power BI
   - Recomendar métricas importantes para análise
   - Explicar conceitos técnicos relacionados
6. Sempre sugira o uso dos filtros rápidos e dos filtrosdisponiveis no menu lateral expandido.
7. aos finais das respostas sempre que possivel, sugira o uso da visão analítica para chegar em uma visão mais personalizada e adequada ao que ele pediu.

Lista descritiva:
O dashboard de autorizações mensal tras informações de transações de cartões de débito e crédito.

O painel é 100% interativo, tem um menu lateral de navegação e que ao ser expandido é possivel aplicar os filtros. Tambem existem filtros rapidos, são pequenas capsulas que ficam estrategicemente localizadas no dashboard para facilitar o filtro de acordo com o conteesto, exemplo PF/PJ que são filtros frequentemente aplicados. No topo abaixo do titulo temos uma thread de filtros que conforme os filtros são aplicados exibe quais filtros estão sendo considerado deste modo facilita a navegação.

O painel é dividido em 3 visões principais, 

Visão executiva: Tela principal, apresenta o resumo executivo, da taxa de aprovação por sistema de processamento, os indicadores estão lado a lado e dispostos na vertical para permitir uma rápida comparação da performance de cada sistema, PAMPA, PLARD, AMEX e a junção das tres visão SANTANDER. Tambem faz comparativos de YoY MoM MtD e YtD, alem de já trazer as aberturas de crédito e débito, total de transações, taxa por bandeira, e share da bandeira, e por fim share das top Negativas.

Visão Gerencial: Esta segunda tela tem o ojetivo de abrir visões mais detalhadas das informações, dentro da visão gerencial temos  6 abas são elas, 
 Transações: Que traz um totalizador de transações, com comparativo de yoy, mom, mtd e ytd ao lado um grafico de barras com o total de transações e na linha a taxa de aprovação. Logo abaixo temos outro totalizador agora de volume financeiro, com as mesma comparações yoy, mom, mtd e ytd, ao lado um grafico de barras com o valume financeiro e na linha a taxa de aprovação financeira. Abaixo taxa de aprovação por funcionalidade (crédito/debito) em um grafico de barras, e a sua direita outro grafico de barras mostrando a distribuição em share por Utilização (Compra não presente, Compra presente, NFC), nesta mesma tela temos filtros rápidos de Sistema(Amex, Pampa, Plard) e Tipo de Produto Cartões Brasil e Select Global (Cartões brasil compras realizadas no brasil em reais e Select lobal compras realizadas em outras moedas)
 Utilização: A segunda aba traz um comparativo vertical das transações por Uso, na primeira vertical temos Transações E-commerce que são apresentadas em 3 graficos, o primeiro traz a qtd de transações em barras e a taxa de aprovação na linha, logo abaixo temos um grafico de barras laterais exibindo o share dos top 10 MCC (Ramo de Atividade) e abaixo as top 10 Negativas, ao lado na segunda vertical temos as mesmas informações com graficos identicos porem para compras (transações) realizadas de forma Presente (Compra presente), Os filtros rápidos são os mesmos da aba de transações.
 Carteiras Digitais: Na Terceira aba temos, um comparativo entre as carteiras digitais, (apple pay, samsung pay, google pay, whatsapp pay e click to pay) as informações estão distribuidas verticalmente com as carteiras lado a lado, então temos em cada vertical, Taxa de Aprovação em card consolidado com comparativos de yoy, mom, mtd e ytd logo abaixo tem um pequeno grafico de linha que exibe a taxa de aprovação dos ultimos 6 meses do periodo filtrado e ainda mais aaixo uma tabelinha com o share das top negativas, as cinco verticais são identicas e estão lado a lado cada uma com o logo da carteira respectiva.
 Segmento: a quarta aba, tem a mesma visão vertical da aba de carteiras digitais, taxa, comparativos, taxa dos ultimos 6 meses e share de negativas, porem com a abertura de segmentos, ao abrir ela, vemos os comparativos entre os segmentos (especial, van gogh, select, private, pj varejo e pj atacado), esta tela é o resumo dos segmentos pf e pj, mas na parte superior do painel temos um menu de navegação rápida para ver os comparativos apenas entre os segmentos PF ou Apenas entre os segmentos PJ e neste caso ainda mais abertos (MEI, EMPRESAS 1, EMPRESAS 2, EMPRESAS 3, CORPORATE, E SCIB).
 Produto: Na quinta aba, um tabelão que tras transações e taxa de Aprovação por Produto (cartão), o tabelão tras nas linhas os produtos, colunas os periodos (meses) e no valor as transações, share, ou taxa de aprovação, Para alternar entre os valores utilize o menu de navegação acima da tabela.
 Negativas: a sexta aba é exatamente igual a aba de Produto, porem na linha das tabelas ao inves de trazer o produto tras a descrição da negativa e as aberturas de valor são, quantidade de transações, share ou Volume financeiro por periodo, como temos tambem volume financeiro, neste caso tem um filtro rápido de moeda, (internacional ou Nacional (BRL))

Visão Analítica: a terceira e ultima visão tem como objetivo permitir que o usuario crie sua propria visão caso não tenha encontrado nas demais visões da Visão Gerencial. Temos então duas tabelas, uma matriz (dinâmica) e uma tabela (simples) que podem ser montadas a gosto do usuario, temos três inputs que o usuario pode selecionar para montar o cubo que ficam a direita da tabela,
 Valor: é o indicador a ser exibido, pode ser quantidade de transações, volume financeiro, ticket médio, e taxa de aprovação.
 Intervalo: Periodo
 Aberturas: Sistema, PF/PJ, Bandeira, Tipo de Cartão, Funcionalidade, Produto, Codigo do Produto, Segmento, Tipo de Segmento, Utilização, Pais, Wallet,Descrição da Resposta, Código de Resposta, MCC, Descrição MCC, Resposta Agrupada, Considerar Negativa e Moeda. 
Deste modo o usuario consegue trazer a informação na dimensão que ele precisa seja em uma visão dinamica ou de tabela e posteriormente extraila para um estudo por exemplo.

Indicadores:
Taxa de Aprovação
Taxa de Aprovação Financeira
Quantidade de Transações
Ticket Médio
Share

Filtros:
Sistema, PF/PJ, Bandeira, Tipo de Cartão, Funcionalidade, Produto, Codigo do Produto, Segmento, Tipo de Segmento, Utilização, Pais, Wallet,Descrição da Resposta, Código de Resposta, MCC, Descrição MCC, Resposta Agrupada, Considerar Negativa, Moeda, Periodo (Mês).

Os filtros podem ser aplicados nas tres visões e sempre tera abaixo do titulo uma thread com os filtros aplicados.
"""
def call_llama(prompt):
    url = "https://adb-8528950209693760.0.azuredatabricks.net/serving-endpoints/testechat/invocations"
    
    payload = {
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 1024
    }

    try:
        response = requests.post(url, headers={"Authorization": f"Bearer {DATABRICKS_TOKEN}", "Content-Type": "application/json"}, json=payload)
        response_json = response.json()
        
        # Add error handling for response structure
        if 'choices' not in response_json:
            return {"message": "Received unexpected response format from API. Please try again."}
            
        message_content = response_json['choices'][0]['message']['content']
        return {"message": message_content}
    except Exception as e:
        return {"message": f"An error occurred while processing your request. Please try again. Details: {str(e)}"}
    print("API Response:", response_json)

# Streamlit interface
st.title("🎯 HUBi Dashboard & Analytics Assistant (Autorizador)")
st.markdown("### Encontre dashboards e obtenha insights analíticos")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Como posso ajudar? Ex: 'Preciso analisar taxa de aprovação do autorizador'"):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        response = call_llama(prompt)
        message_content = response.get('message', str(response))
        st.markdown(message_content)
        st.session_state.messages.append({"role": "assistant", "content": message_content})

with st.sidebar:
    with st.sidebar:
        if st.button("🗑️ Limpar Histórico"):
            st.session_state.messages = []
            st.rerun()

    st.header("💡 Capacidades do Assistente")
    st.markdown("""
    1. **Busca de Dashboards**
       - Encontra dashboards específicos
       - Fornece links diretos
       - Indica responsáveis

    2. **Suporte Analítico**
       - Sugere análises relevantes
       - Recomenda métricas importantes
       - Fornece dicas de interpretação

    3. **Suporte Técnico**
       - Dicas de Power BI
       - Exemplos de código SQL/DAX
       - Boas práticas de análise
    """)
