import json
import os

def save_json(obj: dict, filename: str):
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(obj, f, indent=2)

def render_png(fa_dict: dict, out_path: str, kind: str = 'nfa'):
    """Render finite automata dict to PNG using graphviz (if available).
    kind: 'nfa' or 'dfa'
    """
    try:
        import graphviz
    except Exception as e:
        # If graphviz isn't available, write a simple text file note.
        txt = out_path.rsplit('.', 1)[0] + ".txt"
        with open(txt, "w", encoding="utf-8") as f:
            f.write("Graphviz not installed. Expected to render: " + os.path.basename(out_path))
        return

    dot = graphviz.Digraph(comment=kind.upper())

    # invisible starting helper
    dot.node('startingStateH', 'startingStateH', style='invis')

    # nodes
    start = fa_dict.get('startingState')
    for key, data in fa_dict.items():
        if key == 'startingState':
            continue
        shape = 'doublecircle' if data.get('isTerminatingState') else 'circle'
        dot.node(key, key, shape=shape)

    # edges
    for key, data in fa_dict.items():
        if key == 'startingState':
            continue
        for symbol, nxt in data.items():
            if symbol == 'isTerminatingState':
                continue
            if isinstance(nxt, list):  # NFA
                for target in nxt:
                    label = 'ε' if symbol == 'epsilon' else symbol
                    dot.edge(key, target, label=label)
            else:  # DFA
                dot.edge(key, nxt, label=symbol)

    if start is not None:
        dot.edge('startingStateH', start)

    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    dot.format = 'png'
    dot.render(out_path, cleanup=True)
