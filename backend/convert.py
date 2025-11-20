import os
from typing import Dict

from regex_to_nfa import (
    regex_to_tokens,
    parse_tokens_to_ast,
    thompson_construct_nfa,
)
from nfa_to_dfa import NFAtoDFAConverter
from minimize_dfa import DFAMinimizer
from graph_render import render_png, save_json

BASE_DIR = os.path.dirname(__file__)
OUTPUT_DIR = os.path.join(BASE_DIR, 'static', 'output')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_regex(regex: str, uid: str) -> Dict[str, str]:
    """Regex → NFA → DFA → MinDFA; renders PNG/JSON and returns URL paths."""
    # 1) Regex → Tokens → AST
    tokens = regex_to_tokens(regex)
    ast = parse_tokens_to_ast(tokens)

    # 2) AST → NFA (dict)
    nfa_dict = thompson_construct_nfa(ast)

    # 3) NFA → DFA (dict)
    dfa_obj = NFAtoDFAConverter(nfa_dict).convert()
    dfa_dict = dfa_obj.to_dict()

    # 4) Minimize DFA (dict)
    mindfa_dict = DFAMinimizer(dfa_dict).to_dict()

    # 5) Render PNGs
    nfa_png_path = os.path.join(OUTPUT_DIR, f"{uid}_nfa.png")
    dfa_png_path = os.path.join(OUTPUT_DIR, f"{uid}_dfa.png")
    mindfa_png_path = os.path.join(OUTPUT_DIR, f"{uid}_mindfa.png")

    render_png(nfa_dict, nfa_png_path, kind='nfa')
    render_png(dfa_dict, dfa_png_path, kind='dfa')
    render_png(mindfa_dict, mindfa_png_path, kind='dfa')

    # 6) Save JSONs
    nfa_json_path = os.path.join(OUTPUT_DIR, f"{uid}_nfa.json")
    dfa_json_path = os.path.join(OUTPUT_DIR, f"{uid}_dfa.json")
    mindfa_json_path = os.path.join(OUTPUT_DIR, f"{uid}_mindfa.json")

    save_json(nfa_dict, nfa_json_path)
    save_json(dfa_dict, dfa_json_path)
    save_json(mindfa_dict, mindfa_json_path)

    # 7) Response payload (frontend can store these URLs in localStorage)
    return {
        "id": uid,
        "regex": regex,
        "nfa_img": f"/static/output/{uid}_nfa.png",
        "dfa_img": f"/static/output/{uid}_dfa.png",
        "mindfa_img": f"/static/output/{uid}_mindfa.png",
        "nfa_json": f"/static/output/{uid}_nfa.json",
        "dfa_json": f"/static/output/{uid}_dfa.json",
        "mindfa_json": f"/static/output/{uid}_mindfa.json",
    }
