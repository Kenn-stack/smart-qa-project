import argparse
import json
import logging
import sys
from smart_qa.client import LLMClient
from smart_qa.helper import read_file, save_text_to_file
from configs.logging import setup_logging


llm_client = LLMClient()
setup_logging()
logger = logging.getLogger(__name__)

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to the text.")
    parser.add_argument("--save", help="Path to directory.")
    parser.add_argument("--clear-cache")
    
    args = parser.parse_args()
    return args
    
    
def read_multiline(prompt="Paste your text. Press Enter then Ctrl+D:  "):
    print(prompt)
    try:
        return sys.stdin.read().strip()
    except Exception:
        return ""



def summarize_caller(args):
    if args.file:
        # read_file = read_multiline("Would you like to read from file?:  [yes/no]  ")
        # if read_file == "yes":
        text = read_file(args.file)
        # else:
        #     text = read_multiline()

    else:
        text = read_multiline()
    if text:    
        response = llm_client.summarize(text)
        if args.save:
            save_text_to_file(args.save, response, "txt")
            return "Summary saved to file"
        return response
    return "No text was provided"
    
    
def ask_caller(args):
    if args.file:
        text = read_file(args.file)
    else:
        text = read_multiline("Paste text you would like to ask questions on. Press Enter then Ctrl+D:  ")
    
    if text:
        chat = llm_client.create_chat(text) 
        while True:
            question = input("Ask your question?  /[quit] : ")
            if question == "quit":
                break
            response = llm_client.ask(question, chat)
            print(response)
    else:
        return "No text was provided"


        
def extract_caller(args):
    if args.file:
        text = read_file(args.file)
    else:
        text = read_multiline("Paste text you would like to extract details from. Press Enter then Ctrl+D :  ")
        
    response = llm_client.extract_entities(text)
    if args.save:
        response = json.dumps(response)
        save_text_to_file(args.save, response, "json")
        return "Extracted details saved to file"
    return response
  
        
        

def main():
    args = get_args()
    while True:
        first_prompt = input("What would you like to do? [summarize | ask | extract] or [quit]:  ")
        if first_prompt == "quit":
            break
            
        elif first_prompt == "summarize":
            response = summarize_caller(args)
            print(response)
            continue
            
        elif first_prompt == "ask":
            ask_caller(args)
            continue
            
        elif first_prompt == "extract":
            response = extract_caller(args)
            print(response)
            continue

            
            
if __name__ == "__main__":
    main()
    