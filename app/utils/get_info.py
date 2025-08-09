import json
from typing import List, Set, Dict


def read_interviews(meta_path: str = "data/input_meta.txt"):
    with open(meta_path, "r", encoding="utf-8") as file:
        for line in file:
            line = line.strip()
            if line:
                filepath, company, industry = line.split(",")
                yield (filepath, company, industry)

def get_industries(meta_path: str = "data/input_meta.txt") -> Set[str]:
    return {industry for _, _, industry in read_interviews(meta_path)}

def get_companies(meta_path: str = "data/input_meta.txt") -> Set[str]:
    return {company for _, company, _ in read_interviews(meta_path)}

def get_hypotheses(hypotheses_path: str = "data/hypotheses.json") -> Dict[str, List]:
    with open(hypotheses_path, "r", encoding="utf-8") as file:
        return json.load(file)
