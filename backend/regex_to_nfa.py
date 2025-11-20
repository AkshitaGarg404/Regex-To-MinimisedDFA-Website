from enum import Enum, auto
from abc import ABC, abstractmethod

#  Lexer 
class TokenType(Enum):   #Creating enum ... each member is represented by a constant value... done so that token identification becomes smooth... kyunki hrr jgh OR ko 0, STAR ko 1 likhna confusing ho jaaega... toh ENUM allows us to use them as userdefined values.
    OR = auto()
    STAR = auto()
    PLUS = auto()
    QUESTION_MARK = auto()
    OPEN_PAREN = auto()
    CLOSED_PAREN = auto()
    OPEN_SQUARE_BRACKET = auto()
    CLOSED_SQUARE_BRACKET = auto()
    DASH = auto()
    LITERAL = auto()

def getTypeToken(ch: str) -> TokenType:  #returns TokenType for each character .. argument is a character.. not string
    if ch == '|': return TokenType.OR
    elif ch == '*': return TokenType.STAR
    elif ch == '+': return TokenType.PLUS
    elif ch == '?': return TokenType.QUESTION_MARK
    elif ch == '(': return TokenType.OPEN_PAREN
    elif ch == ')': return TokenType.CLOSED_PAREN
    elif ch == '[': return TokenType.OPEN_SQUARE_BRACKET
    elif ch == ']': return TokenType.CLOSED_SQUARE_BRACKET
    elif ch == '-': return TokenType.DASH
    else: return TokenType.LITERAL

def getTokenValue(ttype: TokenType):   #get corresponding regex operator wrt TokenType Enum.. opposite of above function
    mapping = {                     #dictionary created... could have also used if..elif..else
        TokenType.OR: '|',
        TokenType.STAR: '*',
        TokenType.PLUS: '+',
        TokenType.QUESTION_MARK: '?',
        TokenType.OPEN_PAREN: '(',
        TokenType.CLOSED_PAREN: ')',
        TokenType.OPEN_SQUARE_BRACKET: '[',
        TokenType.CLOSED_SQUARE_BRACKET: ']',
        TokenType.DASH: '-',
    }
    return mapping.get(ttype, ttype)       #dict.get(key,default)... default is written in case of TokenType.literal

class Token:        #class Token clubs TokenType and its value
    def __init__(self, ttype: TokenType, content: str):   #cpp: Token(this, TokenType ttype, str content)
        self.ttype = ttype
        self.content = content
    def __repr__(self): return f"Token({self.ttype}, {self.content!r})"   #cpp: override << operator for cout
    #So whenever you print a token: it prints: Token(it's type, string) eg: Token(TokenType.OR, '|')


class regexLexer:       #Entire string is stored as attribute: regexStr and has a method that converts regexStr->Tokens
    def __init__(self, regexStr: str):   
        self.regexStr = regexStr
    def lexer(self):
        return [Token(getTypeToken(ch), ch) for ch in self.regexStr]   
        #returns a list of objects of Token class represented each character of regex



#Thus now... lexer phase is done and we have a list of all tokens with their type and content/value


#  AST 
class AstNode(ABC):         #AstNode inherits Abstract Base Class 
    @abstractmethod         #equivalent to pure virtual function in cpp
    def __init__(self): pass        #empty function to be overriden in derived classes


#now all nodes will inherit this Base Class

class OrAstNode(AstNode):
    def __init__(self, left, right): self.left, self.right = left, right

class SeqAstNode(AstNode):      #sequence:: (a|b)c → Seq(Or(a,b), c)
    def __init__(self, left, right): self.left, self.right = left, right

class StarAstNode(AstNode):
    def __init__(self, left): self.left = left

class PlusAstNode(AstNode):
    def __init__(self, left): self.left = left

class QuestionMarkAstNode(AstNode):
    def __init__(self, left): self.left = left

class LiteralCharacterAstNode(AstNode):         
    def __init__(self, char): self.char = char      #(self, char: str) also possible

class SquareBracketAstNode(AstNode):
    def __init__(self, clas): self.clas = clas       #set of chars  #(self, clas: set) also possible


#Recursive Function for printing the AST... indent is used for making tree look better 
def print_ast(node, indent=0):
    pad = ' ' * indent
    if isinstance(node, OrAstNode):         #is instance checks that the object is instance of a class or not
        print(pad + 'OR'); print_ast(node.left, indent+2); print_ast(node.right, indent+2)
    elif isinstance(node, SeqAstNode):
        print(pad + 'SEQ'); print_ast(node.left, indent+2); print_ast(node.right, indent+2)
    elif isinstance(node, StarAstNode):
        print(pad + 'STAR'); print_ast(node.left, indent+2)
    elif isinstance(node, PlusAstNode):
        print(pad + 'PLUS'); print_ast(node.left, indent+2)
    elif isinstance(node, QuestionMarkAstNode):
        print(pad + 'QUESTION_MARK'); print_ast(node.left, indent+2)
    elif isinstance(node, LiteralCharacterAstNode):
        print(pad + f"LITERAL: {node.char}")
    elif isinstance(node, SquareBracketAstNode):
        print(pad + 'SQUARE_BRACKET')
        for ch in sorted(node.clas): print(' '*(indent+2) + f'CHARACTER: {ch}')
    else:
        raise ValueError('Invalid AST node type')
    

# Example: [a-c](e|f)g
"""
Regex:  
[a-c](e|f)g

Token stream: 
[
  Token(OPEN_SQUARE_BRACKET, '['),
  Token(LITERAL, 'a'),
  Token(DASH, '-'),
  Token(LITERAL, 'c'),
  Token(CLOSED_SQUARE_BRACKET, ']'),
  Token(OPEN_PAREN, '('),
  Token(LITERAL, 'e'),
  Token(OR, '|'),
  Token(LITERAL, 'f'),
  Token(CLOSED_PAREN, ')'),
  Token(LITERAL, 'g')
]

Parsing into AST:
[a-c]   is one AST node  → SquareBracketAstNode
(e|f)   is one AST node  → OrAstNode
g       is one AST node  → LiteralNode('g')


AST:
Seq(
    SquareBracketAstNode({'a','b','c'}),
    Seq(
        OrAstNode( Literal('e'), Literal('f') ),
        Literal('g')
    )
)
"""

#  Parser 
class ParseRegex:
    def __init__(self, tokenStream):   
        self.tokenStream = tokenStream      #TokenStream= List of tokens that lexer outputs
        self.currToken = 0                  #keeps track of current index in Token Stream

    def parse(self):   #Entry Point for Parsing
        ast = self.parse_E()    #E is the root of grammer as regex is itself an expression
        if self.currToken < len(self.tokenStream):      #if after parsing E, A token is left .. 
            raise Exception("Unexpected token")         #then, that token is invalid and an exception
        return ast                              #Ast is returned for entire regex

    def parse_E(self):
        ast = self.parse_T()        #for an expression.. parse that particular term
        if self.match(TokenType.OR):    #if after parsing a term.. there is OR.. we need to attend it otherwise return ast till now
            left = ast      #left child= current ast
            right = self.parse_E()  #for right child .. parse the expression after OR
            ast = OrAstNode(left, right)    #Return the OR node
        return ast

    def parse_T(self): 
        ast = self.parse_C()  #For a term, Parse that particular component first
        if self.currToken < len(self.tokenStream):  #if a token is left
            ttype = self.tokenStream[self.currToken].ttype    #get the type of that token
            if ttype in (TokenType.LITERAL, TokenType.OPEN_PAREN, TokenType.OPEN_SQUARE_BRACKET):
                #if the token is a literal, [, (... then it means it is a sequence.
                left = ast  #current parsed component becomes left child
                right = self.parse_T()     #next parsed Term becomes right child
                ast = SeqAstNode(left, right)       #make a sequence node and return it
        return ast

    def parse_C(self):  #To parse each particular component
        if self.match(TokenType.LITERAL):   #if current component is a literal
            ast = LiteralCharacterAstNode(self.tokenStream[self.currToken - 1].content)
            #create a literal node for that literal.. (-1) because match increments the index
        elif self.match(TokenType.OPEN_PAREN): 
            #if current token is (... parse the expression inside it
            ast = self.parse_E()
            self.expect(TokenType.CLOSED_PAREN)  #after that expect )
        elif self.match(TokenType.OPEN_SQUARE_BRACKET):
             #if current token is [... parse the expression inside it
            clas = self.parse_L()   
            self.expect(TokenType.CLOSED_SQUARE_BRACKET)     #after that expect ]
            ast = SquareBracketAstNode(clas)        #make a square bracket node.. clas has a set of possible values
        else:
            raise Exception("Unexpected token while parsing C")
        

        #only after getting a valid component from above code.. check for quantifiers  
        #Quantifier nodes added to above ast's
        if self.match(TokenType.STAR):  
            ast = StarAstNode(ast)
        elif self.match(TokenType.PLUS):
            ast = PlusAstNode(ast)
        elif self.match(TokenType.QUESTION_MARK):
            ast = QuestionMarkAstNode(ast)
        return ast

    #finally parsing a literal
    def parse_L(self):
        clas = set()    #a set of possible values
        que = []    # a queue maintained for previously read characters
        while self.currToken < len(self.tokenStream):  
            ttype = self.tokenStream[self.currToken].ttype
            if ttype == TokenType.CLOSED_SQUARE_BRACKET: 
                break      #sequence has ended if ] is encountered so stop
            elif ttype == TokenType.LITERAL:
                ch = self.tokenStream[self.currToken].content
                clas.add(ch); que.append(ch)    #add that character to possible set(clas) and queue
            elif ttype == TokenType.DASH:
                #if it is a dash .. two possibilities .. dash is a literal.. dash is an operator
                if len(clas) == 0 or self.currToken + 1 == len(self.tokenStream) or self.tokenStream[self.currToken + 1].ttype == TokenType.CLOSED_SQUARE_BRACKET:
                    #all above reasons satisfy that dash is a literal
                    clas.add('-')
                else:
                    start = ord(que.pop())  #returns last element of the queue and ord gives its ASCII value
                    end = ord(self.tokenStream[self.currToken + 1].content) #currenlty self.currToken has dash so the end will be the next token after that
                    for i in range(start, end + 1): 
                        clas.add(chr(i))
                        #Adding all characters to the set
                    self.currToken += 1   #move on to end token a-c<-
            self.currToken += 1     #move on to the next token as current is parsed already
        return clas     #return the set of possible literals

    def match(self, ttype):         #Checks if current index token Type=== given Token type
        if self.currToken >= len(self.tokenStream): return False        #TokenStream has ended
        if self.tokenStream[self.currToken].ttype == ttype:     #go to the next token as current is already matched
            self.currToken += 1; return True
        return False

    #Resuable function for raising Token exceptions
    def expect(self, ttype):
        if not self.match(ttype):
            raise Exception("Expected token", getTokenValue(ttype))

#  Thompson (AST to NFA) 

"""
Example for NFA:
{
    starting_state = "A"
    final_state = "B"
    states = {
    "A": {"a": ["B"], "": ["C"]},   # A --a--> B, A --epsilon--> C
    "B": {"b": ["B"]},              # B --b--> B (self-loop)
    "C": {}                         # C has no outgoing transitions
    }
}
"""
class NFA:
    def __init__(self, starting_state, final_state, states):
        self.starting_state = starting_state
        self.final_state = final_state
        self.states = states #map which describes transitions
        self._dect = {}     #used to map state names -> numeric IDs (stringified later).(cpp unordered map)
        self._index = 0    #is the next numeric id to assign.


    #function for assigning numeric ids to each state
    def _state_to_number(self, state):  
        if state not in self._dect: #if there is already an id for that state.. no need to assign a new one
            self._dect[state] = self._index; self._index += 1 #if not assign an index
        return str(self._dect[state])       #string is returned for that id

    def to_dict(self): #produces a serializable dictionary representation (suitable for JSON) where states are replaced by numeric string IDs and epsilon transitions are labeled "epsilon".
        #create starting state for that nfa and assign a numeric id to it.
        nfa_dict = {'startingState': self._state_to_number(self.starting_state)}
        #map.items() gives both key value pairs of self.states
        for state_name, state in self.states.items():
            #state_name= that state 
            #state = all transitions from that state
            transitions = {}
            for symbol, next_states in state.items():
                #symbol gives what is taking us to the next state
                #next_states give which state is symbol taking us to
                key = 'epsilon' if symbol == '' else symbol
                transitions[key] = [self._state_to_number(ns) for ns in next_states]
            nfa_dict[self._state_to_number(state_name)] = {
                'isTerminatingState': self._state_to_number(state_name) == self._state_to_number(self.final_state),
                **transitions
            }
        return nfa_dict

class ThompsonConstruction:
    def __init__(self, ast): self.ast = ast

    def construct(self):
        s, f, states = self._construct_from_ast(self.ast)
        return NFA(s, f, states)

    def _construct_from_ast(self, node):
        if isinstance(node, LiteralCharacterAstNode):
            # start --a--> final
            s = object(); f = object()      # s=start state.... f=final state (both are diff unique objects)
            return s, f, {s: {node.char: {f}}, f: {'': set()}}     # s --char--> f
            #returns start,final and states.. {start --char--> final, final --epsilon--> empty set}

        elif isinstance(node, PlusAstNode):     #A+
            # start --epsilon--> a --epsilon--> final
            #       <--epsilon--
            sub_s, sub_f, sub_states = self._construct_from_ast(node.left)  #build nfa for A
            s = object(); f = object()  #unique start and final states
            states = { s: {'': {sub_s}}, **sub_states, sub_f: {'': {s, f}}, f: {'': set()} }
            # {start --epsilon--> a's start, all transitions from A NFA, from final state of A's NFA --epsilon--> start&final, final--epsilon--> empty set}
            return s, f, states

        elif isinstance(node, QuestionMarkAstNode):  #A?
            # start --epsilon--> a --epsilon--> final
            #      ------------epsilon--------->
            sub_s, sub_f, sub_states = self._construct_from_ast(node.left) #build nfa for A
            s = object(); f = object()
            states = { s: {'': {sub_s, f}}, **sub_states, sub_f: {'': {f}}, f: {'': set()} }
            #{start--epsilon--> start of A's NFA or final(select once or never), all Transitions of A's NFA, final state of A's NFA--epsilon-->final, final--epsilon--> empty set}
            return s, f, states

        elif isinstance(node, SeqAstNode): #ab
            # a --epsilon--> b
            l_s, l_f, l_states = self._construct_from_ast(node.left) #a's NFA
            r_s, r_f, r_states = self._construct_from_ast(node.right) #b's NFA
            states = { **l_states, **r_states, l_f: {'': {r_s}} }
            # all transitions of A , B, final state of A --epsilon--> final state of B
            return l_s, r_f, states

        elif isinstance(node, OrAstNode): #a|b 
            # start --epsilon--> a --epsilon--> final
            #       --epsilon--> b --epsilon-->
            l_s, l_f, l_states = self._construct_from_ast(node.left)
            r_s, r_f, r_states = self._construct_from_ast(node.right)
            s = object(); f = object()
            states = { s: {'': {l_s, r_s}}, **l_states, **r_states, l_f: {'': {f}}, r_f: {'': {f}}, f: {'': set()} }
            #all above states added
            return s, f, states

        elif isinstance(node, StarAstNode): #a*
            #      -----------epsilon------------>
            # start --epsilon--> a --epsilon--> final
            #       <--epsilon--
            sub_s, sub_f, sub_states = self._construct_from_ast(node.left)
            s = object(); f = object()
            states = { s: {'': {sub_s, f}}, **sub_states, sub_f: {'': {s, f}}, f: {'': set()} }
            #all above states added
            return s, f, states

        elif isinstance(node, SquareBracketAstNode): #[abc]
            # start--a--> final
            #      --b-->
            #      --c-->
            s = object(); f = object()
            states = { s: {ch: {f} for ch in node.clas}, f: {'': set()} }
            return s, f, states

        else:
            raise ValueError("Unknown AST node type in Thompson construction")

# -------- Public helpers (used by convert.py) --------
def regex_to_tokens(regex: str):
    return regexLexer(regex).lexer()

def parse_tokens_to_ast(tokens):
    return ParseRegex(tokens).parse()

def thompson_construct_nfa(ast) -> dict:
    return ThompsonConstruction(ast).construct().to_dict()


