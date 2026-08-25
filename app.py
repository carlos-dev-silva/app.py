import streamlit as st
import pandas as pd
import io
import smtplib
from email.message import EmailMessage
from datetime import datetime

# 1. Configuração visual elegante (Off-White e tipografia sem serifa)
st.set_page_config(page_title="Emissão de Pedido", layout="centered")
st.markdown("""
    <style>
        .stApp {
            background-color: #FDFBF7; 
            font-family: 'Bahnschrift', 'Eurostile', sans-serif;
            color: #333333;
        }
        div[data-testid="stForm"] {
            background-color: #FFFFFF;
            border: 1px solid #E0E0E0;
            border-radius: 8px;
            padding: 20px;
            box-shadow: 0px 4px 6px rgba(0,0,0,0.05);
        }
    </style>
""", unsafe_allow_html=True)

# 2. Dados de exemplo (podem ser substituídos por listas completas)
clientes = ['10513 - ESTACAO SAUDE FARMACIA', '10514 - MERCADO CENTRAL']
produtos = [
    '8732089 - PANETTONE TOMMY FRUTAS 400G', 
    '8732090 - PANETTONE TOMMY GOTAS 400G',
    '8732094 - PANETTONE VISCONTI MAIS CHOCOLAT'
]

st.title("📦 Novo Pedido")

# 3. Construção do Formulário
with st.form("form_pedido"):
    vendedor = st.text_input("Seu Nome (Vendedor)")
    cliente = st.selectbox("Cliente", clientes)
    
    st.markdown("### Itens")
    col1, col2, col3 = st.columns([3, 1, 1])
    
    with col1:
        produto = st.selectbox("Produto", produtos)
    with col2:
        qtd = st.number_input("Qtd", min_value=1, step=1)
    with col3:
        unidade = st.selectbox("Unid.", ["CXS", "UNI"])
        
    submit = st.form_submit_button("Gerar e Enviar Pedido", type="primary")

# 4. Lógica ao clicar em enviar
if submit:
    if vendedor.strip() == "":
        st.warning("Por favor, preencha o nome do vendedor.")
    else:
        # Cria a estrutura de dados usando Pandas
        dados = {
            "Data_Pedido": [datetime.now().strftime("%d/%m/%Y %H:%M")],
            "Vendedor": [vendedor],
            "Cliente": [cliente.split(" - ")[1]],
            "Cod_Cliente": [cliente.split(" - ")[0]],
            "Cod_Produto": [produto.split(" - ")[0]],
            "Produto": [produto.split(" - ")[1]],
            "Quantidade": [qtd],
            "Unidade": [unidade]
        }
        df = pd.DataFrame(dados)
        
        # Gera o arquivo Excel em memória (sem salvar no disco)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Pedido')
        
        excel_data = buffer.getvalue()
        
        # 5. Configuração de Envio de E-mail
        # ATENÇÃO: Substitua pelos seus dados. Se usar Gmail, é necessário gerar uma "Senha de App".
        EMAIL_REMETENTE = "seu_email_robo@gmail.com"
        SENHA_APP = "sua_senha_de_app_gerada"
        EMAIL_DESTINO = "seu_email_pessoal@dominio.com"
        
        msg = EmailMessage()
        msg['Subject'] = f'Novo Pedido - {vendedor} - {cliente}'
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = EMAIL_DESTINO
        msg.set_content("Segue em anexo o arquivo Excel com o novo pedido.")
        
        # Anexa o arquivo Excel
        nome_arquivo = f"Pedido_{vendedor}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        msg.add_attachment(excel_data, maintype='application', 
                           subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                           filename=nome_arquivo)
        
        try:
            # Conecta ao servidor SMTP (Exemplo com Gmail)
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA_APP)
                smtp.send_message(msg)
            
            st.success("✅ Pedido enviado com sucesso! O coordenador já recebeu o arquivo.")
        except Exception as e:
            st.error(f"Erro ao enviar e-mail. Verifique as configurações. Detalhe: {e}")