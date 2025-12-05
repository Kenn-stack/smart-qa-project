import argparse
import json
from smart_qa.client import LLMClient
from smart_qa.helper import read_file, save_text_to_file


#           -  _  =  +
llm_client = LLMClient()

def get_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", help="Path to the text.")
    parser.add_argument("--save", help="Path to directory.")
    parser.add_argument("--clear-cache", help="Path to the text.")
    
    args = parser.parse_args()
    return args



def summarize_caller(args):
    if args.file:
        text = read_file(args.file)
    else:
        text = input("Text you would like to summarize? :  ")
        
    response = llm_client.summarize(text)
    if args.save:
        save_text_to_file(args.save, response, "txt")
        return "Summary saved to file"
    return response
    
    
def ask_caller(args):
    if args.file:
        text = read_file(args.file)
    else:
        text = input("Text you would like to ask questions on? :  ")
     
    while True:
        question = input("Ask your question?  /[quit] : ")
        if question == "quit":
           break
        response = llm_client.summarize(text)
        print(response)

        
def extract_caller(args):
    if args.file:
        text = read_file(args.file)
    else:
        text = input("Text you would like to extract details from? :  ")
        
    response = llm_client.extract_entities(text)
    if args.save:
        response = json.dumps(response)
        save_text_to_file(args.save, response, "json")
        return "Extracted details saved to file"
    return response
  
        
        

def main():
    args = get_args()
    while True:
        first_prompt = input("What would you like to do? [summarize | ask | extract] or [quit]")
        if first_prompt == "quit":
            break
            
        elif first_prompt == "summarize":
            response = summarize_caller(args)
            print(response)
            
        elif first_prompt == "ask":
            ask_caller(args)
            
        elif first_prompt == "extract":
            response = summarize_caller(args)
            print(response)

            
            
    