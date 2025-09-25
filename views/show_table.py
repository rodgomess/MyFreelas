import pandas as pd
import streamlit as st
from datetime import date, timedelta
from views.helper import display_text

def show_table(supabase):

    df  = pd.DataFrame(supabase.read())

    if df.empty:
        display_text('Nenhum dado encontrado')
        return
    df["inserted_at"] = pd.to_datetime(df["inserted_at"], errors="coerce", utc=True)

    # ---- UI de filtros (apenas front-end)
    with st.expander("🔎 Filtros", expanded=True):
        c1, c2, c3, c4 = st.columns([2, 2, 2, 2])

        # 1) Busca textual (aplica em title/description/proposal)
        with c1:
            q = st.text_input("Buscar", placeholder="palavra no título/descrição/proposta...").strip()

        # 2) Filtro por decisão do agente
        with c2:
            decisions = ["favoravel", "não favoravel"]
            sel_decision = st.multiselect("Decisão (agente)", decisions, default=[])

        # 3) Filtro por decisão do usuário
        with c3:
            user_opts = ["ACCEPTED", "DENIED", "Sem Decisão"]
            sel_user = st.multiselect("Decisão (usuário)", user_opts, default=[])

        # 4) Site (pelo domínio do link)
        with c4:
            sites = sorted([s for s in df["website"].unique() if s])
            sel_sites = st.multiselect("Site", sites, default=[])

        c5, c6 = st.columns([2, 2])

        with c6:
            only_empty_proposal = st.checkbox("Somente sem proposta")
        with c5:
            preset = st.selectbox("Período", ["Todos", "Hoje", "Últimos 7 dias", "Últimos 30 dias", "Personalizado"])

        if preset == "Personalizado":
            # valores padrão: de min(data) até hoje
            min_date = df["inserted_at"].dropna().min().date() if df["inserted_at"].notna().any() else date.today()
            max_date = df["inserted_at"].dropna().max().date() if df["inserted_at"].notna().any() else date.today()
            d1, d2 = st.date_input("Intervalo (inclui o dia final)", value=(min_date, max_date))
            start_date, end_date = d1, d2
        elif preset == "Hoje":
            start_date = end_date = date.today()
        elif preset == "Últimos 7 dias":
            end_date = date.today()
            start_date = end_date - timedelta(days=6)
        elif preset == "Últimos 30 dias":
            end_date = date.today()
            start_date = end_date - timedelta(days=29)
        else:
            start_date = end_date = None  # "Todos"
        # ---- Aplica filtros
        mask = pd.Series(True, index=df.index)

    if q:
        q_low = q.lower()
        mask &= (
            df["title"].fillna("").str.lower().str.contains(q_low)
            | df["description"].fillna("").str.lower().str.contains(q_low)
            | df["proposal"].fillna("").str.lower().str.contains(q_low)
        )

    if sel_decision:
        mask &= df["decision"].isin(sel_decision)

    if sel_user:
        # normaliza "Sem Decisão"
        ud_norm = df["user_decision"].fillna("Sem Decisão").replace({"": "Sem Decisão"})
        mask &= ud_norm.isin(sel_user)

    if sel_sites:
        mask &= df["website"].isin(sel_sites)

    if only_empty_proposal:
        mask &= df["proposal"].isna() | (df["proposal"].astype(str).str.strip() == "")
    
    if start_date and end_date:
        # converte para limites datetime (incluir dia final inteiro)
        start_ts = pd.to_datetime(pd.Timestamp(start_date), utc=True)
        end_ts = pd.to_datetime(pd.Timestamp(end_date) + pd.Timedelta(days=1), utc=True)  # +1 dia no limite superior
        mask &= df["inserted_at"].between(start_ts, end_ts, inclusive="left")

    df_filtered = df.loc[mask].copy()

    st.caption(f"Mostrando {len(df_filtered)} de {len(df)} registros")
    st.dataframe(
        df_filtered,
        use_container_width=True,
        hide_index=True,
    )


    if st.button("🗑️ Apagar base de dados"):
        st.session_state["open_delete_dialog"] = True

    @st.dialog("⚠️ Confirmar exclusão por intervalo de datas")

    def delete_dialog():
        st.markdown(
            """
            **Atenção:** Esta ação é **irreversível**.  
            Os registros dentro do intervalo selecionado serão **apagados permanentemente**.
            """
        )
        # limites sugeridos pelo próprio DF
        if df["inserted_at"].notna().any():
            min_d = df["inserted_at"].min().date()
            max_d = df["inserted_at"].max().date()
        else:
            min_d = max_d = date.today()

        d1, d2 = st.date_input(
            "Intervalo de datas (inclui o dia final)",
            value=(min_d, max_d),
            min_value=min_d,
            max_value=max_d
        )

        st.divider()
        col1, col2 = st.columns(2)
        with col1:
            acknowledge = st.checkbox("Estou ciente de que não há como desfazer.")
        with col2:
            confirm_text = st.text_input('Digite **APAGAR** para confirmar:', placeholder="APAGAR")

        # (Opcional) prévia de quantidade a excluir
        try:
            preview_mask = df["inserted_at"].between(
                pd.to_datetime(d1).tz_localize("UTC"),
                pd.to_datetime(d2 + timedelta(days=1)).tz_localize("UTC"),
                inclusive="left"
            )
            st.caption(f"Registros que seriam deletados: **{preview_mask.sum()}**")
        except Exception:
            pass

        cA, cB = st.columns(2)
        with cA:
            if st.button("Cancelar"):
                st.rerun()
        with cB:
            disabled = not (acknowledge and confirm_text.strip().upper() == "APAGAR")
            if st.button("Confirmar exclusão", type="primary", disabled=disabled):
                # Chama seu client
                resp = supabase.delete_by_date_range(d1, d2)
                st.success("Registros apagados com sucesso.")
                st.session_state["open_delete_dialog"] = False
                st.rerun()

    # abre o pop-up se o flag estiver setado
    if st.session_state.get("open_delete_dialog"):
        st.session_state["open_delete_dialog"] = False
        delete_dialog()