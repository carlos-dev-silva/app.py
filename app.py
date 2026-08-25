import streamlit as st
import pandas as pd
import io
import smtplib
from email.message import EmailMessage
from datetime import datetime

# 1. Configuração visual e CSS para alinhar perfeitamente no celular
st.set_page_config(page_title="Contagem de Panettone", layout="centered")
st.markdown("""
    <style>
        .stApp {
            background-color: #F8F9FA !important; 
            color: #212529 !important;
            font-family: 'Bahnschrift', 'Segoe UI', sans-serif;
        }
        
        .title-box {
            background-color: #FCF9F2;
            padding: 12px;
            border-radius: 6px;
            margin-bottom: 15px;
            text-align: center;
            border: 1px solid #EAE3D2;
        }
        .title-box h1 {
            margin: 0;
            font-size: 18px !important;
            color: #2C3338 !important;
        }

        /* Caixa de contorno limpa para o nome do produto (igualzinho à sua foto) */
        .produto-box {
            background-color: #FFFFFF;
            border: 1px solid #D6D8DB;
            border-radius: 6px;
            padding: 10px 12px;
            font-size: 11px;
            font-weight: bold;
            color: #333333;
            margin-bottom: 4px;
        }

        div[data-testid="stForm"] {
            border: none;
            padding: 0;
            background: transparent;
        }

        /* Compacta os inputs para remover espaçamentos verticais excedentes */
        div.row-widget.stHorizontal {
            gap: 8px !important;
        }

        /* Botão de envio vermelho */
        button[kind="primary"] {
            background-color: #FF4D4D !important;
            border-color: #FF4D4D !important;
            color: white !important;
            font-weight: bold;
            width: 100%;
            padding: 12px;
            border-radius: 6px;
            font-size: 15px;
            margin-top: 15px;
        }
    </style>
""", unsafe_allow_html=True)

# Título
st.markdown("""
    <div class="title-box">
        <h1>📦 Contagem de Panettone</h1>
    </div>
""", unsafe_allow_html=True)

# Lista fixa de produtos
produtos_fixos = [
    {"cod": "8732089", "desc": "PANETTONE TOMMY FRUTAS 400G"},
    {"cod": "8732090", "desc": "PANETTONE TOMMY GOTAS 400G"},
    {"cod": "8732091", "desc": "PANETTONE VISCONTI FRUTAS 400G"},
    {"cod": "8732092", "desc": "PANETTONE VISCONTI GOTAS 400G"},
    {"cod": "8732093", "desc": "PANETTONE VISCONTI TRUFADO 450G"},
    {"cod": "8732094", "desc": "PANETTONE VISCONTI MAIS CHOCOLAT"},
    {"cod": "8732095", "desc": "PANETTONE VISCONTI DOCE DE LEITE"},
    {"cod": "8732096", "desc": "PANETTONE VISCONTI FRUTAS 680G"},
    {"cod": "8732097", "desc": "PANETTONE VISCONTI GOTAS 680G"}
]

# 3. Construção do Formulário
with st.form("form_pedido"):
    
    cod_cliente = st.text_input("Código do Cliente")
    razao = st.text_input("Razão Social do Cliente")
        
    st.markdown("<p style='margin-top: 15px; font-weight: bold; color: #495057; font-size: 13px;'>Itens da Contagem:</p>", unsafe_allow_html=True)
    
    itens_pedido = []
    
    for i, prod in enumerate(produtos_fixos):
        # Caixa de texto estática simulando o container da sua imagem
        st.markdown(f"<div class='produto-box'>{prod['cod']} - {prod['desc']}</div>", unsafe_allow_html=True)
        
        # Colunas estritamente lado a lado para Qtd e Unidade
        col_qtd, col_unid = st.columns(2)
        
        with col_qtd:
            qtd_str = st.text_input(f"Qtd {i}", value="0", key=f"qtd_{i}", label_visibility="collapsed")
            
        with col_unid:
            unidade = st.selectbox(f"Unid {i}", ["CXS", "UNI"], key=f"unid_{i}", label_visibility="collapsed")
            
        # Espaçamento sutil entre os produtos
        st.markdown("<div style='margin-bottom: 12px;'></div>", unsafe_allow_html=True)
            
        try:
            qtd = int(qtd_str)
        except ValueError:
            qtd = 0
            
        if qtd > 0:
            itens_pedido.append({
                "Cod_Produto": prod["cod"],
                "Produto": prod["desc"],
                "Quantidade": qtd,
                "Unidade": unidade
            })
            
    submit = st.form_submit_button("Gerar e Enviar Pedido", type="primary")

# 4. Lógica de Envio de E-mail
if submit:
    if not cod_cliente or not razao:
        st.warning("Preencha o código do cliente e a razão social.")
    elif len(itens_pedido) == 0:
        st.warning("Insira a quantidade de pelo menos um produto.")
    else:
        dados_planilha = []
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        for item in itens_pedido:
            dados_planilha.append({
                "Data_Pedido": data_atual,
                "Cod_Cliente": cod_cliente,
                "Razao_Social": razao,
                "Cod_Produto": item["Cod_Produto"],
                "Produto": item["Produto"],
                "Quantidade": item["Quantidade"],
                "Unidade": item["Unidade"]
            })
            
        df = pd.DataFrame(dados_planilha)
        
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
            df.to_excel(writer, index=False, sheet_name='Pedido')
        
        excel_data = buffer.getvalue()
        
        EMAIL_REMETENTE = "seu_email_robo@gmail.com"
        SENHA_APP = "sua_senha_de_app_gerada"
        EMAIL_DESTINO = "seu_email_pessoal@dominio.com"
        
        msg = EmailMessage()
        msg['Subject'] = f'Contagem - Cliente: {cod_cliente} ({razao})'
        msg['From'] = EMAIL_REMETENTE
        msg['To'] = EMAIL_DESTINO
        msg.set_content(f"Segue em anexo a contagem com {len(itens_pedido)} produtos preenchidos.")
        
        nome_arquivo = f"Contagem_{cod_cliente}_{datetime.now().strftime('%Y%m%d_%H%M')}.xlsx"
        msg.add_attachment(excel_data, maintype='application', 
                           subtype='vnd.openxmlformats-officedocument.spreadsheetml.sheet', 
                           filename=nome_arquivo)
        
        try:
            with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
                smtp.login(EMAIL_REMETENTE, SENHA_APP)
                smtp.send_message(msg)
            
            st.success("✅ Contagem enviada com sucesso!")
        except Exception as e:
            st.error(f"Erro ao enviar e-mail. Detalhe: {e}")
