# NFA → DFA conversion and DFA serialization

class DFA:
    def __init__(self, alphabet, states, start_state, accept_states, transition_function):
        self.alphabet = alphabet              # set[str] -- set of symbols the DFA accepts
        self.states = states                  # list[str] -- A list of DFA-state names
        self.start_state = start_state        # str
        self.accept_states = accept_states    # list[str]
        self.transition_function = transition_function  # dict[str, dict[str, str]] {q0: {a:q1, b:q2}, q1: {a:q2}} 
        self._name_map = {}     #storing state name->id mapping
        self._counter = 0       #to assign id's to states

    def run(self, input_string: str) -> bool:   #running a dfa to see if we can reach any accepting state for a string
        current_state = self.start_state
        for symbol in input_string:
            current_state = self.transition_function[current_state][symbol]
        return current_state in self.accept_states

    def _num(self, state: str) -> str:  #assigning an id to state or getting id of a pre-existing state
        if state not in self._name_map:
            self._name_map[state] = self._counter
            self._counter += 1
        return str(self._name_map[state])

    def to_dict(self) -> dict:      #serializes the DFA into a JSON-like structure.
        dfa_dict = {'startingState': self._num(self.start_state)}
        for state in self.states:
            if state == 'frozenset()':
                continue  # skip empty set representation
            dfa_dict[self._num(state)] = {"isTerminatingState": state in self.accept_states} #indicates whether current state is accepting or not
            for symbol in self.alphabet:    #for displaying all transitions
                nxt = self.transition_function.get(state, {}).get(symbol, "frozenset()")
                if nxt != "frozenset()":
                    dfa_dict[self._num(state)][symbol] = self._num(nxt)
        return dfa_dict

class NFAtoDFAConverter:
    def __init__(self, nfa: dict):
        self.nfa = nfa
        #{
            # "startingState": "S1",
            # "S1": { "a": ["S2"], "epsilon": ["S3"] },
            # "S2": { "b": ["S1"] },
            # "S3": { "isTerminatingState": True }
        #}

    
    # For every state q ∈ S, collect all NFA transitions on symbol a
    #Move(S, a) = union of all destinations q --a--> ?
    def move(self, states, symbol):
        out = set()
        for s in states:
            if s in self.nfa:
                for nxt in self.nfa[s].get(symbol, []):
                    out.add(nxt)
        return frozenset(out)

    # Because NFA may later go through ε-moves, take ε-closure:
    #DFA_transition(S, a) = ε-closure(Move(S, a))
    def epsilon_closure(self, states):
        closure = set(states)   #Start the closure with the given input states.
        #The ε-closure(q) is: all states reachable from q using only ε-transitions, including q itself
        stack = list(states)    #stack is used to DFS or BFS through epsilon transitions.
        while stack:
            s = stack.pop() #checking for each state in MOVE set
            if s in self.nfa:
                for nxt in self.nfa[s].get('epsilon', []): #Looking for epsilon links
                    if nxt not in closure:
                        closure.add(nxt)    #add that to closure and stack too for future checks
                        stack.append(nxt)
        return frozenset(closure)   #return frozenset
    
    # This new set of states becomes a new DFA state, if not already created.


    def convert(self) -> DFA:
        alphabet = set()
        for state_dict in self.nfa.values(): #nfa is stored as a dictionary.. so nfa.values gives starting state and dictionaries of transitions from each state..
            #"S1",
            # { "a": ["S2"], "epsilon": ["S3"] },
            # { "b": ["S1"] },
            # { "isTerminatingState": True }
            if isinstance(state_dict, dict):
                for sym in state_dict.keys():
                    if sym not in ("epsilon", "isTerminatingState"):
                        alphabet.add(sym)   #adding only symbols to alphabet

        start = self.epsilon_closure([self.nfa['startingState']]) #epsilon closure of starting state
        #each epsilon closure becomes a dfa state .. till no new states are found
        dfa_states = [start]    
        #A DFA state S is accepting if: S contains any accepting NFA state
        dfa_accept_states = []
        dfa_tf = {}
        # Add that DFA state to queue
        queue = [start]

        #continue till queue is empty .. ie no new state is found
        while queue:
            curr = queue.pop(0)
            for sym in alphabet:
                #finding all nodes reachable from current node using "sym" symbol.. including epsilon transitions
                mv = self.move(curr, sym)
                cl = self.epsilon_closure(mv)

                #that becomes new dfa state
                if cl not in dfa_states:
                    dfa_states.append(cl)
                    queue.append(cl)
                
                #storing this new transiton for curr-> newly discovered node.. dfa_transition function
                dfa_tf.setdefault(str(curr), {})
                dfa_tf[str(curr)][sym] = str(cl)

            #if any of the participating state is final in NFA.. it will be final of DFA too
            if any((s in self.nfa and self.nfa[s].get('isTerminatingState', False)) for s in curr):
                if str(curr) not in dfa_accept_states:
                    dfa_accept_states.append(str(curr))

        
        #adding everything to DFA constructor
        states_str = [str(s) for s in dfa_states]
        start_str = str(start)
        dfa_accept_states_str = [str(s) for s in dfa_accept_states]
        dfa_tf_str = {str(k): {sym: str(v) for sym, v in trans.items()} for k, trans in dfa_tf.items()}

        return DFA(alphabet, states_str, start_str, dfa_accept_states_str, dfa_tf_str)
