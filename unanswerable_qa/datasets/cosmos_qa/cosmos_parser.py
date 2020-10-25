# -*- coding: utf-8 -*-
"""
Created on Fri Oct 23 09:49:58 2020

@author: nickg
"""

import csv
import json

def is_entry_unanswerable(entry):
    cosmos_nei_str = "None of the above choices"
    correct_answer = entry["answer"+str(entry["label"])]
    return cosmos_nei_str in correct_answer

def convert_data_entry(entry):
    entry['Context'] = entry.pop('context')
    entry['Question'] = entry.pop('question')
    entry['Reasoning type'] = "Unanswerable"
    entry['Choices'] = {}
    entry['Choices']['A'] = entry.pop('answer0')
    entry['Choices']['B'] = entry.pop('answer1')
    entry['Choices']['C'] = entry.pop('answer2')
    entry['Choices']['D'] = entry.pop('answer3')
    entry['Answer'] = chr(int(entry["label"])+65)
    del entry['id']
    del entry['label']
    
def parse_cosmos_qa_from_csv(input_csv_path, output_json_path):
    unanswerable_dict = {}
    unanswerable_dicts = []
    cosmos_nei_str = "None of the above choices"
    quail_nei_str = "not enough information"
    
    # CSV files are structured as:
    #   id, context, question, answer0, answer1, answer2, answer3, label
    with open(input_csv_path, mode='r', encoding="utf8") as csv_file:
        csv_reader = csv.DictReader(csv_file)
        for entry in csv_reader:
            correct_answer_key = "answer"+str(entry["label"])
            if cosmos_nei_str in entry[correct_answer_key]:
                # Replace with quail nei string instance
                entry[correct_answer_key] = quail_nei_str
                convert_data_entry(entry)
                unanswerable_dicts.append(entry)
                #unanswerable_dict[entry["id"]] = entry
    
    with open(output_json_path, 'w') as json_file:
        json.dump(unanswerable_dicts, json_file)
        
def parse_cosmos_qa_from_jsonl(input_jsonl_path, output_json_path):
    unanswerable_dict = {}
    
    with open(input_jsonl_path, 'r') as jsonl_file:
        json_list = list(jsonl_file)

        for json_str in json_list:
            entry = json.loads(json_str)
            if is_entry_unanswerable(entry):
                unanswerable_dict[entry["id'"]] = entry
                
    with open(output_json_path, 'w') as json_file:
        json.dump(unanswerable_dict, json_file)
                
parse_cosmos_qa_from_csv('cosmos_qa_valid.csv', 'cosmos_qa_valid_unanswerable.json')
parse_cosmos_qa_from_csv('cosmos_qa_train.csv', 'cosmos_qa_train_unanswerable.json')