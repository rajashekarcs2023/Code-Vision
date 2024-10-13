import io
import asyncio
import logging
import json
import os
from datetime import datetime
from agent.template_runner import template_runner
from agent.data_extraction import download_and_extract_pdf_from_s3
from helpers.generate_file_suffix import generate_file_suffix
from helpers.prompts import get_concatenate_prompt
from helpers.s3 import upload_file_to_s3
from agent.llm import llm_inference
from helpers.utils import process_markdown_references

async def execute(template_list, company: str, kb_location: list, user_id, model_name: str, max_tokens: int, id: str, technology: str, industry: str, region: str, time_range: str):
    try:
        pdf_content = ""

        tasks = [
            template_runner(template_path, company, pdf_content=pdf_content, technology=technology, industry=industry, region=region, time_range=time_range, user_id=user_id, file_ids=kb_location)
            for template_path in template_list
        ]
        results = await asyncio.gather(*tasks)
        os.makedirs('results_logs', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_report_filename = f"results_logs/results_{user_id}_{timestamp}.json"
        with open(full_report_filename, 'w', encoding='utf-8') as f:
            json.dump({"results": results}, f, indent=2)
        logging.info(f"Full processed report written to {full_report_filename}")

        processed_results = [process_markdown_references(result) for result in results]
        os.makedirs('procresults_logs', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_report_filename = f"procresults_logs/procresults_{user_id}_{timestamp}.json"
        with open(full_report_filename, 'w', encoding='utf-8') as f:
            json.dump({"procresults": processed_results}, f, indent=2)
        logging.info(f"Full processed report written to {full_report_filename}")

        processed_report = "\n\n".join(results)

        # Log the processed_report content
        logging.info(f"Processed Report for user {user_id} created")

        # Write the processed_report to a JSON file
        os.makedirs('processed_report_logs', exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        full_report_filename = f"processed_report_logs/processed_report_{user_id}_{timestamp}.json"
        with open(full_report_filename, 'w', encoding='utf-8') as f:
            json.dump({"processed_report": processed_report}, f, indent=2)
        logging.info(f"Full processed report written to {full_report_filename}")

        #concatenate, concatenate_sys = get_concatenate_prompt(processed_report)
        
        '''combined_document = await llm_inference(
            message=concatenate,
            model_name=model_name,
            api_key="",
            system_instruction=concatenate_sys,
            max_tokens=max_tokens,
            temperature=0.1
        )'''

        suffix = generate_file_suffix(user_id)
        file_stream = io.BytesIO(processed_report.encode('utf-8'))
        return upload_file_to_s3(file_stream, f"{user_id}/generated_docs/{id}/generated-doc-{suffix}.md")

    except Exception as e:
        logging.error(f"Error in execute function: {str(e)}")
        raise