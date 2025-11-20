# DFA Minimization via partition refinement

class DFAMinimizer:
    def __init__(self, dfa_dict: dict):
        self.states = [s for s in dfa_dict.keys() if s != 'startingState']
        self.start_state = dfa_dict['startingState']

        # Build alphabet from transition keys (excluding metadata)
        alphabet = set()
        for s in self.states:
            for k in dfa_dict[s].keys():
                if k != 'isTerminatingState':
                    alphabet.add(k)
        self.alphabet = sorted(alphabet)

        self.accept_states = set([s for s in self.states if dfa_dict[s].get('isTerminatingState')])
        self.reject_states = set(self.states) - self.accept_states
        self.partition = self._partition(dfa_dict)
        self.old_dfa_dict = dfa_dict

    def _partition(self, dfa_dict):
        # Start with accepting vs. rejecting
        partition = [self.accept_states.copy(), self.reject_states.copy()]

        while True:
            group_to_idx = {}
            for i, grp in enumerate(partition):
                for st in grp:
                    group_to_idx[st] = i

            new_partition = []
            next_states = {}

            # Compute signature for each state
            for grp in partition:
                if not grp:
                    continue
                for st in grp:
                    sig = {}
                    for sym in self.alphabet:
                        if sym in dfa_dict[st]:
                            sig[sym] = group_to_idx[dfa_dict[st][sym]]
                        else:
                            sig[sym] = 'stuck'
                    next_states[st] = tuple(sorted(sig.items()))

            # Split by signature
            for grp in partition:
                if not grp:
                    continue
                buckets = {}
                for st in grp:
                    sig = next_states[st]
                    buckets.setdefault(sig, set()).add(st)
                for members in buckets.values():
                    new_partition.append(members)

            if new_partition == partition:
                break
            partition = new_partition
        return partition

    def to_dict(self) -> dict:
        # Map each old state to its partition index
        name_map = {}
        for i, grp in enumerate(self.partition):
            for st in grp:
                name_map[st] = i

        out = {"startingState": str(name_map[self.start_state])}
        # Initialize nodes
        for st in self.old_dfa_dict.keys():
            if st == 'startingState':
                continue
            idx = str(name_map[st])
            out.setdefault(idx, {"isTerminatingState": False})
            if self.old_dfa_dict[st].get("isTerminatingState"):
                out[idx]["isTerminatingState"] = True

        # Transitions
        for st in self.old_dfa_dict.keys():
            if st == 'startingState':
                continue
            s_idx = str(name_map[st])
            for sym in self.alphabet:
                if sym in self.old_dfa_dict[st]:
                    t_idx = str(name_map[self.old_dfa_dict[st][sym]])
                    out[s_idx][sym] = t_idx

        return out
