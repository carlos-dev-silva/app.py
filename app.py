import streamlit as st
import pandas as pd
import io
import smtplib
from email.message import EmailMessage
from datetime import datetime


# ============================================================
# CONFIGURAÇÃO DA PÁGINA
# ============================================================

st.set_page_config(
    page_title="Contagem de Panettone",
    page_icon="📦",
    layout="centered",
    initial_sidebar_state="collapsed"
)


# ============================================================
# CSS - VISUAL MOBILE
# ============================================================

st.markdown("""
<style>

    /* ========================================================
       CONFIGURAÇÃO GERAL
       ======================================================== */

    .stApp {
        background-color: #F8F9FA !important;
        color: #212529 !important;
        font-family: 'Segoe UI', Arial, sans-serif;
    }

    .block-container {
        padding-top: 15px !important;
        padding-bottom: 20px !important;
        padding-left: 10px !important;
        padding-right: 10px !important;
        max-width: 600px !important;
    }


    /* ========================================================
       TÍTULO
       ======================================================== */

    .title-box {
        background-color: #FCF9F2;
        padding: 10px;
        border-radius: 6px;
        margin-bottom: 15px;
        text-align: center;
        border: 1px solid #EAE3D2;
    }

    .title-box h1 {
        margin: 0;
        font-size: 18px !important;
        color: #2C3338 !important;
        font-weight: 700;
    }


    /* ========================================================
       CAMPOS CLIENTE
       ======================================================== */

    div[data-testid="stTextInput"] {
        margin-bottom: 5px !important;
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


    /* ========================================================
       TEXTO "ITENS DA CONTAGEM"
       ======================================================== */

    .itens-titulo {
        margin-top: 15px;
        margin-bottom: 8px;
        font-weight: bold;
        color: #495057;
        font-size: 13px;
    }


    /* ========================================================
       PRODUTO
       ======================================================== */

    .produto-box {
        background-color: #FFFFFF;
        border: 1px solid #D6D8DB;
        border-radius: 6px;
        padding: 10px 12px;
        font-size: 11px;
        font-weight: 600;
        color: #333333;
        margin-bottom: 3px;
        line-height: 1.3;
        box-sizing: border-box;
        width: 100%;
    }


    /* ========================================================
       COLUNAS - FORÇA QTD + UNIDADE LADO A LADO
       ======================================================== */

    div[data-testid="stHorizontalBlock"] {
        display: flex !important;
        flex-direction: row !important;
        flex-wrap: nowrap !important;
        gap: 6px !important;
        width: 100% !important;
        align-items: stretch !important;
    }

    div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
        min-width: 0 !important;
        width: 50% !important;
        flex: 1 1 50% !important;
        padding: 0 !important;
    }


    /* ========================================================
       INPUT DE QUANTIDADE
       ======================================================== */

    div[data-testid="stHorizontalBlock"] div[data-testid="stTextInput"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="stTextInput"] label {
        display: none !important;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="stTextInput"] input {
        width: 100% !important;
        height: 40px !important;
        min-height: 40px !important;
        box-sizing: border-box !important;

        background-color: #F1F3F5 !important;
        border: 1px solid #E0E3E6 !important;
        border-radius: 5px !important;

        font-size: 13px !important;
        color: #333333 !important;

        padding: 8px 10px !important;
    }


    /* ========================================================
       SELECTBOX - UNIDADE
       ======================================================== */

    div[data-testid="stHorizontalBlock"] div[data-testid="stSelectbox"] {
        margin: 0 !important;
        padding: 0 !important;
    }

    div[data-testid="stHorizontalBlock"] div[data-testid="stSelectbox"] label {
        display: none !important;
    }

    div[data-testid="stHorizontalBlock"] div[data-baseweb="select"] {
        width: 100% !important;
        min-height: 40px !important;
        height: 40px !important;
    }

    div[data-testid="stHorizontalBlock"] div[data-baseweb="select"] > div {
        min-height: 40px !important;
        height: 40px !important;

        background-color: #F1F3F5 !important;
        border: 1px solid #E0E3E6 !important;
        border-radius: 5px !important;

        font-size: 13px !important;
        color: #333333 !important;
    }


    /* ========================================================
       FORMULÁRIO
       ======================================================== */

    div[data-testid="stForm"] {
        border: none !important;
        padding: 0 !important;
        background: transparent !important;
    }


    /* ========================================================
       ESPAÇAMENTO ENTRE PRODUTOS
       ======================================================== */

    .produto-espaco {
        height: 12px;
    }


    /* ========================================================
       BOTÃO
       ======================================================== */

    button[kind="primary"] {
        background-color: #FF4D4D !important;
        border-color: #FF4D4D !important;
        color: white !important;
        font-weight: bold !important;
        width: 100% !important;
        min-height: 46px !important;
        padding: 10px !important;
        border-radius: 6px !important;
        font-size: 15px !important;
        margin-top: 12px !important;
    }

    button[kind="primary"]:hover {
        background-color: #E63946 !important;
        border-color: #E63946 !important;
    }


    /* ========================================================
       MENSAGENS
       ======================================================== */

    div[data-testid="stAlert"] {
        font-size: 13px !important;
        border-radius: 6px !important;
    }


    /* ========================================================
       MOBILE
       ======================================================== */

    @media (max-width: 600px) {

        .block-container {
            padding-left: 8px !important;
            padding-right: 8px !important;
            padding-top: 10px !important;
        }

        .title-box {
            margin-bottom: 12px;
        }

        .title-box h1 {
            font-size: 17px !important;
        }

        .produto-box {
            font-size: 10.5px !important;
            padding: 9px 10px !important;
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 5px !important;
        }

        div[data-testid="stHorizontalBlock"] input,
        div[data-testid="stHorizontalBlock"] [data-baseweb="select"] {
            font-size: 12px !important;
        }

    }

</style>
""", unsafe_allow_html=True)


# ============================================================
# TÍTULO
# ============================================================

st.markdown("""
<div class="title-box">
    <h1>📦 Contagem de Panettone</h1>
</div>
""", unsafe_allow_html=True)


# ============================================================
# LISTA FIXA DE PRODUTOS
# ============================================================

produtos_fixos = [
    {
        "cod": "8732089",
        "desc": "PANETTONE TOMMY FRUTAS 400G"
    },
    {
        "cod": "8732090",
        "desc": "PANETTONE TOMMY GOTAS 400G"
    },
    {
        "cod": "8732091",
        "desc": "PANETTONE VISCONTI FRUTAS 400G"
    },
    {
        "cod": "8732092",
        "desc": "PANETTONE VISCONTI GOTAS 400G"
    },
    {
        "cod": "8732093",
        "desc": "PANETTONE VISCONTI TRUFADO 450G"
    },
    {
        "cod": "8732094",
        "desc": "PANETTONE VISCONTI MAIS CHOCOLAT"
    },
    {
        "cod": "8732095",
        "desc": "PANETTONE VISCONTI DOCE DE LEITE"
    },
    {
        "cod": "8732096",
        "desc": "PANETTONE VISCONTI FRUTAS 680G"
    },
    {
        "cod": "8732097",
        "desc": "PANETTONE VISCONTI GOTAS 680G"
    }
]


# ============================================================
# FORMULÁRIO
# ============================================================

with st.form("form_pedido"):

    # --------------------------------------------------------
    # DADOS DO CLIENTE
    # --------------------------------------------------------

    cod_cliente = st.text_input(
        "Código do Cliente",
        placeholder="Digite o código do cliente"
    )

    razao = st.text_input(
        "Razão Social do Cliente",
        placeholder="Digite a razão social"
    )


    # --------------------------------------------------------
    # TÍTULO DOS PRODUTOS
    # --------------------------------------------------------

    st.markdown(
        "<div class='itens-titulo'>Itens da Contagem:</div>",
        unsafe_allow_html=True
    )


    # Lista que receberá os produtos preenchidos
    itens_pedido = []


    # --------------------------------------------------------
    # PRODUTOS
    # --------------------------------------------------------

    for i, prod in enumerate(produtos_fixos):

        # Caixa do produto
        st.markdown(
            f"""
            <div class="produto-box">
                {prod['cod']} - {prod['desc']}
            </div>
            """,
            unsafe_allow_html=True
        )


        # ----------------------------------------------------
        # QUANTIDADE + UNIDADE
        # SEMPRE LADO A LADO
        # ----------------------------------------------------

        col_qtd, col_unid = st.columns(
            [1, 1],
            gap="small"
        )


        # ----------------------------------------------------
        # QUANTIDADE
        # ----------------------------------------------------

        with col_qtd:

            qtd_str = st.text_input(
                f"Qtd {i}",
                value="0",
                key=f"qtd_{i}",
                label_visibility="collapsed"
            )


        # ----------------------------------------------------
        # UNIDADE
        # ----------------------------------------------------

        with col_unid:

            unidade = st.selectbox(
                f"Unid {i}",
                ["CXS", "UNI"],
                key=f"unid_{i}",
                label_visibility="collapsed"
            )


        # ----------------------------------------------------
        # CONVERTE QUANTIDADE
        # ----------------------------------------------------

        try:
            qtd = int(qtd_str)
        except (ValueError, TypeError):
            qtd = 0


        # ----------------------------------------------------
        # ADICIONA SOMENTE PRODUTOS COM QUANTIDADE
        # ----------------------------------------------------

        if qtd > 0:

            itens_pedido.append({
                "Cod_Produto": prod["cod"],
                "Produto": prod["desc"],
                "Quantidade": qtd,
                "Unidade": unidade
            })


        # Espaçamento
        st.markdown(
            "<div class='produto-espaco'></div>",
            unsafe_allow_html=True
        )


    # ========================================================
    # BOTÃO
    # ========================================================

    submit = st.form_submit_button(
        "Gerar e Enviar Pedido",
        type="primary",
        use_container_width=True
    )


# ============================================================
# PROCESSAMENTO DO PEDIDO
# ============================================================

if submit:

    # --------------------------------------------------------
    # VALIDAÇÃO DO CLIENTE
    # --------------------------------------------------------

    if not cod_cliente or not razao:

        st.warning(
            "⚠️ Preencha o código do cliente e a razão social."
        )


    # --------------------------------------------------------
    # VALIDAÇÃO DOS PRODUTOS
    # --------------------------------------------------------

    elif len(itens_pedido) == 0:

        st.warning(
            "⚠️ Insira a quantidade de pelo menos um produto."
        )


    # --------------------------------------------------------
    # GERA PEDIDO
    # --------------------------------------------------------

    else:

        dados_planilha = []

        data_atual = datetime.now().strftime(
            "%d/%m/%Y %H:%M"
        )


        # ----------------------------------------------------
        # MONTA DADOS DA PLANILHA
        # ----------------------------------------------------

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


        # ----------------------------------------------------
        # DATAFRAME
        # ----------------------------------------------------

        df = pd.DataFrame(dados_planilha)


        # ----------------------------------------------------
        # CRIA EXCEL NA MEMÓRIA
        # ----------------------------------------------------

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


        # ====================================================
        # CONFIGURAÇÃO DO E-MAIL
        # ====================================================
        #
        # IMPORTANTE:
        # Substitua os três valores abaixo.
        #
        # Para Gmail, use uma SENHA DE APP.
        # ====================================================

        EMAIL_REMETENTE = "seu_email_robo@gmail.com"

        SENHA_APP = "sua_senha_de_app_gerada"

        EMAIL_DESTINO = "seu_email_pessoal@dominio.com"


        # ----------------------------------------------------
        # MONTA E-MAIL
        # ----------------------------------------------------

        msg = EmailMessage()

        msg["Subject"] = (
            f"Contagem - Cliente: "
            f"{cod_cliente} ({razao})"
        )

        msg["From"] = EMAIL_REMETENTE

        msg["To"] = EMAIL_DESTINO


        msg.set_content(
            f"""
Segue em anexo a contagem do cliente.

Código do Cliente: {cod_cliente}

Razão Social: {razao}

Quantidade de produtos preenchidos: {len(itens_pedido)}

Data: {data_atual}
"""
        )


        # ----------------------------------------------------
        # NOME DO ARQUIVO
        # ----------------------------------------------------

        nome_arquivo = (
            f"Contagem_"
            f"{cod_cliente}_"
            f"{datetime.now().strftime('%Y%m%d_%H%M')}"
            f".xlsx"
        )


        # ----------------------------------------------------
        # ANEXA EXCEL
        # ----------------------------------------------------

        msg.add_attachment(
            excel_data,
            maintype="application",
            subtype=(
                "vnd.openxmlformats-officedocument"
                ".spreadsheetml.sheet"
            ),
            filename=nome_arquivo
        )


        # ====================================================
        # ENVIA E-MAIL
        # ====================================================

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


            # ------------------------------------------------
            # SUCESSO
            # ------------------------------------------------

            st.success(
                "✅ Contagem enviada com sucesso!"
            )


        except Exception as e:

            st.error(
                f"❌ Erro ao enviar e-mail.\n\n"
                f"Detalhe: {e}"
            )
