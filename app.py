import streamlit as st

st.set_page_config(page_title="Simulador de Arrays", page_icon="🗄️", layout="wide")

# Inicialização do Array no Estado da Sessão (Session State)
if "TAMANHO" not in st.session_state:
    st.session_state.TAMANHO = 5
if "armario" not in st.session_state:
    st.session_state.armario = [None] * st.session_state.TAMANHO
if "destaque_idx" not in st.session_state:
    st.session_state.destaque_idx = None

st.title("🗄️ Simulador de Arrays (Analogia do Armário)")
st.markdown("Aprenda o conceito de **Arrays** manipulando gavetas virtuais:")

# Configuração Lateral (Sidebar)
st.sidebar.header("⚙️ Configurações")
novo_tamanho = st.sidebar.number_input(
    "Tamanho do Armário (Nº de Gavetas):", 
    min_value=1, 
    max_value=12, 
    value=st.session_state.TAMANHO
)

if novo_tamanho != st.session_state.TAMANHO:
    st.session_state.TAMANHO = novo_tamanho
    # Ajusta o array mantendo os itens existentes
    novo_armario = [None] * novo_tamanho
    for i in range(min(len(st.session_state.armario), novo_tamanho)):
        novo_armario[i] = st.session_state.armario[i]
    st.session_state.armario = novo_armario
    st.session_state.destaque_idx = None
    st.rerun()

# Painel de Operações
col_op, col_busca = st.columns(2)

with col_op:
    st.subheader("📥 Guardar / Esvaziar")
    idx_selecionado = st.selectbox(
        "Escolha a Gaveta (Índice):", 
        range(st.session_state.TAMANHO),
        format_func=lambda x: f"Gaveta {x}"
    )
    nome_item = st.text_input("Item:", placeholder="Ex: Meias, Livro...")
    
    col_btn1, col_btn2 = st.columns(2)
    with col_btn1:
        if st.button("Guardar", type="primary", use_container_width=True):
            if nome_item.strip():
                st.session_state.armario[idx_selecionado] = nome_item.strip()
                st.session_state.destaque_idx = None
                st.success(f"✅ '{nome_item}' guardado na Gaveta {idx_selecionado}.")
            else:
                st.warning("⚠️ Digite um nome para o item.")
    
    with col_btn2:
        if st.button("Esvaziar", use_container_width=True):
            if st.session_state.armario[idx_selecionado] is not None:
                removido = st.session_state.armario[idx_selecionado]
                st.session_state.armario[idx_selecionado] = None
                st.session_state.destaque_idx = None
                st.info(f"🗑️ '{removido}' removido da Gaveta {idx_selecionado}.")
            else:
                st.warning(f"Gaveta {idx_selecionado} já está vazia.")

with col_busca:
    st.subheader("🔍 Buscar no Armário")
    termo_busca = st.text_input("Buscar Item:", placeholder="O que você procura?")
    
    if st.button("Buscar Gaveta", use_container_width=True):
        termo = termo_busca.strip().lower()
        if termo:
            encontrado = None
            for i, item in enumerate(st.session_state.armario):
                if item and item.lower() == termo:
                    encontrado = i
                    break
            
            if encontrado is not None:
                st.session_state.destaque_idx = encontrado
                st.success(f"🔍 Item encontrado na **Gaveta {encontrado}**!")
            else:
                st.session_state.destaque_idx = None
                st.error("❌ Item não encontrado em nenhuma gaveta.")
        else:
            st.warning("⚠️ Digite algo para buscar.")

st.markdown("---")

# Visualização do Armário (Grade de Gavetas)
st.subheader("🖼️ Visualização do Armário")
cols = st.columns(st.session_state.TAMANHO)

for i in range(st.session_state.TAMANHO):
    item = st.session_state.armario[i]
    eh_destaque = (i == st.session_state.destaque_idx)
    
    border_color = "#ca8a04" if eh_destaque else ("#0284c7" if item else "#cbd5e1")
    bg_color = "#fef08a" if eh_destaque else ("#e0f2fe" if item else "#f8fafc")
    conteudo = f"**{item}**" if item else "<span style='color: #94a3b8;'>[ VAZIA ]</span>"
    
    with cols[i]:
        st.markdown(
            f"""
            <div style="background-color: {bg_color}; border: 2px solid {border_color}; 
                        border-radius: 8px; padding: 10px; text-align: center;">
                <div style="font-size: 11px; color: #64748b; font-weight: bold;">ÍNDICE {i}</div>
                <div style="font-size: 15px; margin-top: 5px;">{conteudo}</div>
            </div>
            """, 
            unsafe_allow_html=True
          )
