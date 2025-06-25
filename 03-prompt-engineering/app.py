import pymupdf
import streamlit as st
from scripts import AI_Utilities

# Inicializar estado da sessão
if "cv_content" not in st.session_state:
    st.session_state["cv_content"] = ""
if "evaluation" not in st.session_state:
    st.session_state["evaluation"] = None
if "evaluation_report" not in st.session_state:
    st.session_state["evaluation_report"] = None
if "suggestions" not in st.session_state:
    st.session_state["suggestions"] = None
if "generate_clicked" not in st.session_state:
    st.session_state["generate_clicked"] = False
if "ai_utilities" not in st.session_state:
    st.session_state["ai_utilities"] = (
        AI_Utilities()
    )  # Armazenar instância das Utilidades de IA

SUCCESS_SCORE = 85
FAILURE_SCORE = 45

st.set_page_config(
    page_title="Analisador de Currículo e Vaga com IA",
    page_icon="👩🏻‍💻",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        "Report a bug": "https://github.com/vivekpathania/ai-experiments/issues"
    },
)

st.title("Analisador de Currículo e Vaga com IA")
st.caption("Otimize seu processo de contratação ou aprimore seu currículo com IA.")

container = st.container(border=False)

with st.sidebar:
    mode = st.radio("Selecionar Modo", ["Contratação", "Candidato"])

    uploaded_jd_file = st.file_uploader("Enviar Descrição da Vaga (PDF)", key="jd")
    uploaded_cv_file = st.file_uploader("Enviar Currículo do Candidato (PDF)", key="cv")
    submitted = st.button(
        "Avaliar Compatibilidade" if mode == "Contratação" else "Analisar Currículo"
    )

# Lógica Principal da Aplicação
if submitted:
    if not st.session_state.get("ai_utilities"):
        st.error("Utilidades de IA não inicializadas. Verifique sua chave de API.")
    elif not uploaded_jd_file or not uploaded_cv_file:
        st.error("Tanto a Descrição da Vaga quanto o Currículo são obrigatórios.")
    else:
        st.session_state["ai_utilities"] = (
            AI_Utilities()
        )  # Garantir que as Utilidades de IA estejam inicializadas
        st.session_state["suggestions"] = None
        container.empty()
        try:
            # Extrair conteúdo do PDF e armazenar no estado da sessão
            with pymupdf.open(stream=uploaded_jd_file.read(), filetype="pdf") as pdf:
                jd_content = "\n\n".join(page.get_text("text") for page in pdf)

            with pymupdf.open(stream=uploaded_cv_file.read(), filetype="pdf") as pdf:
                cv_content = "\n\n".join(page.get_text("text") for page in pdf)
                st.session_state["cv_content"] = cv_content

            if mode == "Contratação":
                evaluation = st.session_state["ai_utilities"].evaluate(
                    jd_content, cv_content, False
                )
                container.write(evaluation)
            else:
                with st.spinner("Processando avaliação..."):
                    evaluation_json = st.session_state["ai_utilities"].evaluate(
                        jd_content, cv_content, True
                    )
                st.session_state["evaluation"] = evaluation_json
                score = evaluation_json.get("overall_score", 0)
                gaps = evaluation_json.get("gaps", [])
                if gaps:
                    eval_report = st.session_state[
                        "ai_utilities"
                    ].json_to_markdown_report(evaluation_json)
                    with st.spinner("Gerando sugestões..."):
                        suggestions = st.session_state[
                            "ai_utilities"
                        ].generate_suggestions(",".join(gaps))
                    st.session_state["suggestions"] = suggestions
                    st.session_state["evaluation_report"] = eval_report
                else:
                    st.session_state["suggestions"] = (
                        "Nenhuma lacuna encontrada. Seu currículo está alinhado!"
                    )

        except Exception as e:
            st.error(f"Erro ao processar arquivos: {e}")

# Fluxo de Trabalho do Modo Candidato
if mode == "Candidato" and st.session_state.get("evaluation"):
    score = st.session_state["evaluation"].get("overall_score", 0)

    if score >= SUCCESS_SCORE:
        container.success(
            "Parabéns! Seu currículo está bem alinhado com a Descrição da Vaga. Nenhuma melhoria adicional é necessária."
        )
        container.write(st.session_state["evaluation_report"])
    elif FAILURE_SCORE <= score < SUCCESS_SCORE:
        container.warning(
            "Seu currículo tem alinhamento moderado. Considere estas melhorias:"
        )
        container.markdown("### Relatório")
        container.write(st.session_state["evaluation_report"])
        container.markdown("### Sugestões de Melhoria")
        st.session_state["suggestions"] = container.text_area(
            "Revise as melhorias sugeridas para aprimorar seu currículo. Você também pode adicionar seus próprios pontos ou sugestões para refinar ainda mais sua candidatura.",
            value=st.session_state["suggestions"],
            disabled=score < FAILURE_SCORE,
        )
        generate_clicked = container.button("Gerar Currículo Melhorado")
        if generate_clicked:
            st.session_state["generate_clicked"] = True
    else:
        container.error(
            "Seu currículo não atende aos requisitos da vaga. Considere refiná-lo ainda mais ou candidatar-se a vagas com qualificações correspondentes."
        )
        container.markdown("### Relatório")
        container.write(st.session_state["evaluation_report"])
        container.markdown("### Sugestões de Melhoria")
        container.text_area(
            "Revise as sugestões.",
            value=st.session_state["suggestions"],
            disabled=True,
        )


# Lidar com Geração de Currículo
if st.session_state.get("generate_clicked"):
    container.empty()
    try:
        if st.session_state["evaluation"] and st.session_state["suggestions"]:
            with st.spinner("Gerando seu currículo atualizado..."):
                updated_cv = st.session_state["ai_utilities"].rewrite_cv(
                    st.session_state["cv_content"],
                    st.session_state["suggestions"],
                    st.session_state["evaluation"].get("jd_summary", ""),
                )

            container.markdown("### Currículo Atualizado")
            container.code(updated_cv, language="markdown")
            st.download_button(
                "Baixar Currículo Melhorado",
                data=updated_cv,
                file_name="curriculo_aprimorado.md",
                mime="text/markdown",
            )
            st.session_state["generate_clicked"] = False  # Resetar estado
        else:
            st.error("Dados ausentes para reescrita do currículo.")
    except Exception as e:
        st.error(f"Erro ao gerar currículo: {e}")
