import streamlit as st
import pandas as pd
import io
import smtplib
from email.message import EmailMessage
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO
# ============================================================

st.set_page_config(
    page_title="Contagem de Panettone",
    page_icon="📦",
    layout="centered"
)


# ============================================================
# CSS
# ============================================================

st.markdown("""
<style>

    .stApp {
        background: #F5F6F8 !important;
        color: #212529 !important;
        font-family: Arial, sans-serif !important;
    }

    /* ESPAÇAMENTO AMPLIADO NO TOPO PARA DESCOLAR DA BARRA DO STREAMLIT */
    .block-container {
        max-width: 620px !important;
        padding: 55px 12px 30px 12px !important;
    }

    /* MARGEM SUPERIOR DO TÍTULO */
    .titulo {
        background: #FCF9F2;
        border: 1px solid #E8E0D0;
        border-radius: 7px;
        padding: 12px;
        text-align: center;
        margin-top: 20px;
        margin-bottom: 16px;
    }

    .titulo h1 {
        margin: 0 !important;
        padding: 0 !important;
        font-size: 18px !important;
        color: #30353A !important;
        font-weight: 700 !important;
    }

    div[data-testid="stTextInput"] {
        margin-bottom: 8px !important;
    }

    div[data-testid="stTextInput"] label {
        font-size: 12px !important;
        font-weight: 600 !important;
        color: #495057 !important;
    }

    div[data-testid="stTextInput"] input {
        height: 40px !important;
        min-height: 40px !important;
        border-radius: 6px !important;
        border: 1px solid #CED4DA !important;
        font-size: 13px !important;
        padding: 8px 10px !important;
        box-sizing: border-box !important;
    }

    .itens-titulo {
        margin-top: 14px;
        margin-bottom: 7px;
        font-size: 13px;
        font-weight: 700;
        color: #495057;
    }

    .produto {
        width: 100%;
        box-sizing: border-box;
        background: #FFFFFF;
        border: 1px solid #D6D8DB;
        border-radius: 6px;
        padding: 9px 11px;
        margin-top: 5px;
        margin-bottom: 3px;
        font-size: 11px;
        line-height: 1.3;
        color: #333333;
        font-weight: 600;
        overflow: hidden;
    }

    div[class*="st-key-produto_linha_"] {
        display: grid !important;
        grid-template-columns: minmax(0, 1fr) minmax(0, 1fr) !important;
        column-gap: 6px !important;
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
        box-sizing: border-box !important;
    }

    div[class*="st-key-produto_linha_"] > div {
        min-width: 0 !important;
        width: 100% !important;
        box-sizing: border-box !important;
    }

    div[class*="st-key-produto_linha_"] div[data-testid="stTextInput"] {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[class*="st-key-produto_linha_"] div[data-testid="stTextInput"] label {
        display: none !important;
    }

    div[class*="st-key-produto_linha_"] div[data-testid="stTextInput"] input {
        width: 100% !important;
        height: 40px !important;
        min-height: 40px !important;
        box-sizing: border-box !important;
        background: #EEF1F4 !important;
        border: 1px solid #DDE1E5 !important;
        border-radius: 5px !important;
        color: #333333 !important;
        font-size: 13px !important;
        padding: 8px 10px !important;
    }

    div[class*="st-key-produto_linha_"] div[data-testid="stSelectbox"] {
        width: 100% !important;
        margin: 0 !important;
        padding: 0 !important;
    }

    div[class*="st-key-produto_linha_"] div[data-testid="stSelectbox"] label {
        display: none !important;
    }

    div[class*="st-key-produto_linha_"] div[data-baseweb="select"] {
        width: 100% !important;
        height: 40px !important;
        min-height: 40px !important;
    }

    div[class*="st-key-produto_linha_"] div[data-baseweb="select"] > div {
        height: 40px !important;
        min-height: 40px !important;
        box-sizing: border-box !important;
        background: #EEF1F4 !important;
        border: 1px solid #DDE1E5 !important;
        border-radius: 5px !important;
        font-size: 13px !important;
        color: #333333 !important;
    }

    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }

    .espaco-produto {
        height: 11px;
    }

    button[kind="primary"] {
        width: 100% !important;
        min-height: 46px !important;
        margin-top: 10px !important;
        border-radius: 6px !important;
        background: #FF4D4D !important;
        border: 1px solid #FF4D4D !important;
        color: white !important;
        font-size: 15px !important;
        font-weight: 700 !important;
    }

    button[kind="primary"]:hover {
        background: #E94343 !important;
        border-color: #E94343 !important;
    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# TÍTULO
# ============================================================

st.markdown("""
<div class="titulo">
    <h1>📦 Contagem de Panettone</h1>
</div>
""", unsafe_allow_html=True)


# ============================================================
# PRODUTOS
# ============================================================

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


# ============================================================
# FORMULÁRIO
# ============================================================

with st.form("form_pedido"):

    cod_cliente = st.text_input(
        "Código do Cliente",
        placeholder="Digite o código"
    )

    razao = st.text_input(
        "Razão Social do Cliente",
        placeholder="Digite a razão social"
    )

    st.markdown(
        "<div class='itens-titulo'>Itens da Contagem:</div>",
        unsafe_allow_html=True
    )

    itens_pedido = []

    for i, prod in enumerate(produtos_fixos):

        st.markdown(
            f"""
            <div class="produto">
                {prod["cod"]} - {prod["desc"]}
            </div>
            """,
            unsafe_allow_html=True
        )

        linha = st.container(
            key=f"produto_linha_{i}"
        )

        with linha:
            qtd_str = st.text_input(
                f"Quantidade {i}",
                value="0",
                key=f"qtd_{i}",
                label_visibility="collapsed"
            )

            unidade = st.selectbox(
                f"Unidade {i}",
                ["CXS", "UNI"],
                key=f"unid_{i}",
                label_visibility="collapsed"
            )

        try:
            qtd = int(qtd_str)
        except (ValueError, TypeError):
            qtd = 0

        if qtd > 0:
            itens_pedido.append({
                "Cod_Produto": prod["cod"],
                "Produto": prod["desc"],
                "Quantidade": qtd,
                "Unidade": unidade
            })

        st.markdown(
            "<div class='espaco-produto'></div>",
            unsafe_allow_html=True
        )

    submit = st.form_submit_button(
        "Gerar e Enviar Pedido",
        type="primary",
        use_container_width=True
    )


# ============================================================
# ENVIO
# ============================================================

if submit:

    if not cod_cliente or not razao:
        st.warning("⚠️ Preencha o código do cliente e a razão social.")

    elif len(itens_pedido) == 0:
        st.warning("⚠️ Insira a quantidade de pelo menos um produto.")

    else:
        data_atual = datetime.now().strftime("%d/%m/%Y %H:%M")

        dados_planilha = []

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

        with pd.ExcelWriter(
            buffer,
            engine="openpyxl"
        ) as writer:
            df.to_excel(
                writer,
                index=False,
                sheet_name="Pedido"
            )

        excel_data = buffer.getvalue()

        EMAIL_REMETENTE = "seu_email_robo@gmail.com"
        SENHA_APP = "sua_senha_de_app_gerada"
        EMAIL_DESTINO = "seu_email_pessoal@dominio.com"

        msg = EmailMessage()

        msg["Subject"] = (
            f"Contagem - Cliente: "
            f"{cod_cliente} ({razao})"
        )

        msg["From"] = EMAIL_REMETENTE
        msg["To"] = EMAIL_DESTINO

        msg.set_content(
            f"""
Segue em anexo a contagem.

Código do Cliente: {cod_cliente}

Razão Social: {razao}

Produtos preenchidos: {len(itens_pedido)}

Data: {data_atual}
"""
        )

        nome_arquivo = (
            f"Contagem_"
            f"{cod_cliente}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M')}"
            f".xlsx"
        )

        msg.add_attachment(
            excel_data,
            maintype="application",
            subtype=(
                "vnd.openxmlformats-officedocument"
                ".spreadsheetml.sheet"
            ),
            filename=nome_arquivo
        )

        try:
            with smtplib.SMTP_SSL(
                "smtp.gmail.com",
                465
            ) as smtp:
                smtp.login(
                    EMAIL_REMETENTE,
                    SENHA_APP
                )
                smtp.send_message(msg)

            st.success("✅ Contagem enviada com sucesso!")

        except Exception as e:
            st.error(
                f"❌ Erro ao enviar e-mail.\n\n"
                f"Detalhe: {e}"
            )
