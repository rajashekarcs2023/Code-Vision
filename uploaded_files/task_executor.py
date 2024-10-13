import logging
from agent.llm import llm_inference
from agent.clients.external_rag_client import call_external_rag
from agent.clients.pinecone_client import search_relevant_context
from datetime import datetime

# Configure logging
log_filename = f"task_execution_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
logging.basicConfig(filename=log_filename, level=logging.INFO, format='%(asctime)s - %(message)s')
logging.basicConfig(filename='task_execution.log', level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

async def execute_task(template, company: str, pdf_content:str, technology: str, industry: str, region: str, time_range: str, user_id: str, file_id: str):
    logging.info(f"Starting task execution for company: {company}")

    # Internal RAG
    internal_rag = ""
    if template['RAG']['internal']['query'] is not None:
        internal_rag_prompt = template['RAG']['internal']['query'].replace('{Company Name}', company).replace('{technology}', technology).replace('{industry}', industry).replace('{region}', region).replace('{time_range}', time_range)
        internal_rag = await search_relevant_context(user_id, file_id, internal_rag_prompt)
        logging.info(f"Relevant Context from pinecone: {internal_rag}")

    if template['RAG']['internal']['query'] is not None and internal_rag == "":
        internal_rag = pdf_content

    logging.info(f"Internal RAG: {internal_rag}")

    # External RAG
    external_rag = ""
    if template['RAG']['external']['query'] is not None:
        external_rag_prompt = template['RAG']['external']['query'].replace('{Company Name}', company).replace('{Technology}', technology).replace('{Industry}', industry).replace('{Region}', region).replace('{Time Range}', time_range)
        external_rag = await call_external_rag(prompt=external_rag_prompt)

    logging.info(f"External RAG: {external_rag}")

    # Create final prompt
    prompt_company_name = template['task_input'].replace('{Company Name}', company).replace('{Technology}', technology).replace('{Industry}', industry).replace('{Region}', region).replace('{Time Range}', time_range)

    prompt_internal_rag = prompt_company_name.replace('{Internal Rag}', internal_rag)
    final_prompt = prompt_internal_rag.replace('{External Rag}', external_rag)

    system_instruction_final = template['system_instruction'].replace('{Company Name}', company).replace('{Technology}', technology).replace('{Industry}', industry).replace('{Region}', region).replace('{Time Range}', time_range)

    logging.info(f"Final prompt: {final_prompt}")

    # LLM inference
    res = await llm_inference(
        message=final_prompt,
        model_name=template['inference_parameters']['model'],
        api_key="",
        system_instruction=system_instruction_final,
        max_tokens=template['inference_parameters']['max_output_tokens'],
        temperature=template['inference_parameters']['temperature']
    )

    logging.info(f"LLM inference result: {res}")

    return res