from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnableParallel
from prompts import Prompts
import re


class AI_Utilities:
    def __init__(self):
        """Inicializar LLM Ollama com modelo configurado"""
        self.llm = ChatOllama(model="mistral:latest", temperature=0)

    def __create_chain(self, llm, system_prompt, human_prompt):
        """Construir template de prompt Langchain para avaliação LLM"""
        template = ChatPromptTemplate(
            [
                ("system", system_prompt),
                ("human", human_prompt),
            ]
        )
        return template | llm | StrOutputParser()

    def evaluate(self, jd_content, cv_content, candiateMode):
        """Avaliar Vaga vs Currículo usando processamento de cadeia paralela"""

        # Criar cadeias de análise
        jd_chain = self.__create_chain(
            self.llm, Prompts.JD_PARSING_SYSTEM_PROMPT, Prompts.JD_PARSING_PROMPT
        )
        cv_chain = self.__create_chain(
            self.llm,
            Prompts.RESUME_PARSING_SYSTEM_PROMPT,
            Prompts.RESUME_PARSING_PROMPT,
        )

        # Executar análise paralela
        parallel = RunnableParallel(jd_summary=jd_chain, cv_summary=cv_chain)
        parsed_data = parallel.invoke(
            {"jd_content": jd_content, "cv_content": cv_content}
        )

        # Avaliar dados analisados
        if candiateMode:
            evaluation_chain = self.__create_chain(
                self.llm,
                Prompts.EVALUATION_SYSTEM_PROMPT_JSON,
                Prompts.EVALUATION_PROMPT_JSON,
            )

            json_output = evaluation_chain.invoke(
                {
                    "jd_summary": parsed_data["jd_summary"],
                    "resume_summary": parsed_data["cv_summary"],
                }
            )
            cleanJson = self.__clean_json_string(json_output)
            try:
                import json

                evaluation = json.loads(cleanJson)
                evaluation["jd_summary"] = parsed_data["jd_summary"]
            except json.JSONDecodeError:
                evaluation = {}

            return evaluation
        else:
            evaluation_chain = self.__create_chain(
                self.llm, Prompts.EVALUATION_SYSTEM_PROMPT, Prompts.EVALUATION_PROMPT
            )

            return evaluation_chain.invoke(
                {
                    "jd_summary": parsed_data["jd_summary"],
                    "resume_summary": parsed_data["cv_summary"],
                }
            )

    def generate_suggestions(self, gaps):
        """Gerar sugestões acionáveis de melhoria do currículo"""

        suggestions_chain = self.__create_chain(
            self.llm,
            Prompts.SUGGESTIONS_SYSTEM_PROMPT,
            Prompts.SUGGESTIONS_HUMAN_PROMPT,
        )

        return suggestions_chain.invoke({"gaps": gaps})

    def rewrite_cv(self, cv_content, suggestions, job_requirements):
        cv_chain = self.__create_chain(
            self.llm, Prompts.CV_REWRITE_SYSTEM_PROMPT, Prompts.CV_REWRITE_HUMAN_PROMPT
        )

        return cv_chain.invoke(
            {
                "original_cv": cv_content,
                "suggestions": suggestions,
                "job_requirements": job_requirements,
            }
        )

    def json_to_markdown_report(self, json_eval):
        # Construir a seção de pontos positivos
        # positives = json_eval.get("positives", [])
        # positives_block = (
        #     "- " + "\n- ".join(positives) if positives else
        #     "- Nenhuma correspondência encontrada"
        # )

        # Construir a seção de lacunas
        gaps = json_eval.get("gaps", [])
        gaps_block = "- " + "\n- ".join(gaps) if gaps else "- Nenhuma lacuna detectada"

        return f"""
    **Título da Vaga:** {json_eval.get("job_title", "N/A")}  
    **Pontuação Geral de Compatibilidade:** {json_eval.get("overall_score", "N/A")} 
     
**Lacunas:**
{gaps_block}
    """

    def __clean_json_string(self, json_string):
        pattern = r"^```json\s*(.*?)\s*```$"
        cleaned_string = re.sub(pattern, r"\1", json_string, flags=re.DOTALL)
        return cleaned_string.strip()
