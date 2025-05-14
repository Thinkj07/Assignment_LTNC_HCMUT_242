from StaticError import *
from Symbol import *
from functools import *

def is_identifier(s):
    if not s:
        return False
    if not 'a' <= s[0] <= 'z':
        return False
    return all('a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9' or c == '_' for c in s[1:])

def is_number_literal(s):
    return s.isdigit()

def is_string_literal(s):
    return s.startswith("'") and s.endswith("'") and all('a' <= c <= 'z' or 'A' <= c <= 'Z' or '0' <= c <= '9' or c == '_' for c in s[1:-1])

def get_value_type(value_str, scope_stack):
    if is_number_literal(value_str):
        return "number"
    elif is_string_literal(value_str):
        return "string"
    elif is_identifier(value_str):
        symbol_info = lookup_symbol(scope_stack, value_str)
        if symbol_info is None:
            raise Undeclared(f"Undeclared: {value_str}")
        return symbol_info[0].typ
    else:
        return None # Indicates invalid value format, should be handled upstream? Or TypeMismatch?
                     # Sticking to spec's value formats, this case implies an instruction parse error.


# Helper function to look up a symbol by name in the scope stack
# Searches from current scope backwards to global
# Returns (Symbol, level) if found, None otherwise
def lookup_symbol(scope_stack, name):
    def find_in_scopes(scopes_with_levels):
        if not scopes_with_levels:
            return None
        current_scope, current_level = scopes_with_levels[-1]
        found_list = [s for s in current_scope if s.name == name]

        if found_list:
            return (found_list[0], current_level)
        else:
            return find_in_scopes(scopes_with_levels[:-1])
    scopes_with_levels = [(scope_stack[i], i) for i in range(len(scope_stack))]
    return find_in_scopes(scopes_with_levels)


# Helper function to collect all visible symbols from current scope outwards for PRINT/RPRINT
# Returns a list of (Symbol, level) tuples
def collect_visible_symbols(scope_stack):
    def collect(scopes_with_levels, seen_names):
        if not scopes_with_levels:
            return []
        current_scope, current_level = scopes_with_levels[0]
        rest_scopes = scopes_with_levels[1:]
        newly_visible = [s for s in current_scope if s.name not in seen_names]
        new_seen = seen_names | {s.name for s in newly_visible}
        outer_visible = collect(rest_scopes, new_seen)
        return outer_visible + [(s, current_level) for s in newly_visible]
    scopes_with_levels = [(scope, level) for level, scope in enumerate(scope_stack)]
    scopes_from_inner_to_outer = list(reversed(scopes_with_levels))
    return collect(scopes_from_inner_to_outer, set())


# --- Command Handlers ---
# Each handler takes the current state (scope_stack, results, level) and command-specific arguments,
# returns the new state (scope_stack, new_results, new_level) or raises an exception.

def handle_insert(state, name, typ, instruction):
    scope_stack, results, level = state
    current_scope = scope_stack[-1]
    is_redeclared = any(s.name == name for s in current_scope)
    if is_redeclared:
        raise Redeclared(instruction)
    new_symbol = Symbol(name, typ)
    new_current_scope = current_scope + [new_symbol]
    new_scope_stack = scope_stack[:-1] + [new_current_scope] 
    new_results = results + ["success"] 
    return (new_scope_stack, new_results, level)

def handle_assign(state, name, value_str, instruction):
    scope_stack, results, level = state
    name_symbol_info = lookup_symbol(scope_stack, name)
    if name_symbol_info is None:
        raise Undeclared(instruction)
    name_symbol_type = name_symbol_info[0].typ
    try:
        value_type = get_value_type(value_str, scope_stack)
    except Undeclared as e:
        raise Undeclared(instruction) 
    if name_symbol_type != value_type:
        raise TypeMismatch(instruction)
    new_results = results + ["success"] 

    return (scope_stack, new_results, level) 

def handle_begin(state):
    scope_stack, results, level = state
    new_scope_stack = scope_stack + [[]]
    new_level = level + 1

    return (new_scope_stack, results, new_level) 

def handle_end(state, instruction):
    scope_stack, results, level = state
    if level == 0:
        raise UnknownBlock()
    new_scope_stack = scope_stack[:-1] 
    new_level = level - 1

    return (new_scope_stack, results, new_level) 

def handle_lookup(state, name, instruction):
    scope_stack, results, level = state
    symbol_info = lookup_symbol(scope_stack, name)

    if symbol_info is None:
        raise Undeclared(instruction)
    else:
        found_level = symbol_info[1]
        new_results = results + [str(found_level)] 
        return (scope_stack, new_results, level) 

def handle_print(state):
    scope_stack, results, level = state
    visible_symbols = collect_visible_symbols(scope_stack)
    formatted = [f"{s.name}//{lvl}" for s, lvl in visible_symbols]
    rprint_output = " ".join(formatted)
    return (scope_stack, results + [rprint_output], level)

def handle_rprint(state):
    scope_stack, results, level = state
    visible_symbols = collect_visible_symbols(scope_stack)
    visible_symbols_ordered = reversed(visible_symbols)
    formatted = [f"{s.name}//{lvl}" for s, lvl in visible_symbols_ordered]
    print_output = " ".join(formatted)
    return (scope_stack, results + [print_output], level)


# --- Main Simulation Function ---

def simulate(list_of_commands):
    initial_state = ([[]], [], 0)
    def process_command(state, instruction):
        parts = instruction.strip().split(" ", 2)
        command_type = parts[0]

        try:
            if command_type == "INSERT":
                if len(parts) != 3:
                    raise InvalidInstruction(instruction)
                name = parts[1]
                typ = parts[2]
                if not is_identifier(name) or (typ != "number" and typ != "string"):
                     raise InvalidInstruction(instruction) 

                return handle_insert(state, name, typ, instruction)

            elif command_type == "ASSIGN":
                if len(parts) != 3:
                     raise InvalidInstruction(instruction)
                name = parts[1]
                value_str = parts[2]
                if not is_identifier(name):
                    raise InvalidInstruction(instruction) # Invalid identifier format
                return handle_assign(state, name, value_str, instruction)

            elif command_type == "BEGIN":
                if len(parts) != 1:
                     raise InvalidInstruction(instruction)
                return handle_begin(state)

            elif command_type == "END":
                if len(parts) != 1:
                     raise InvalidInstruction(instruction)
                return handle_end(state, instruction)

            elif command_type == "LOOKUP":
                if len(parts) != 2:
                     raise InvalidInstruction(instruction)
                if not is_identifier(name):
                    raise InvalidInstruction(instruction) # Invalid identifier format
                return handle_lookup(state, name, instruction)

            elif command_type == "PRINT":
                if len(parts) != 1:
                     raise InvalidInstruction(instruction)
                return handle_print(state)

            elif command_type == "RPRINT":
                if len(parts) != 1:
                     raise InvalidInstruction(instruction)
                return handle_rprint(state)

            else:
                raise InvalidInstruction(instruction)

        except StaticError as e:
            raise e
    final_state = reduce(process_command, list_of_commands, initial_state)
    final_symbol_table, final_results, final_level = final_state
    if final_level > 0:
        raise UnclosedBlock(final_level)
    return final_results

import unittest
from TestUtils import TestUtils


class TestSymbolTable(unittest.TestCase):
    def test_0(self):
        input = ["INSERT a1 number", "INSERT b2 string"]
        expected = ["success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 100))

    def test_1(self):
        input = ["INSERT x number", "INSERT y string", "INSERT x string"]
        expected = ["Redeclared: INSERT x string"]

        self.assertTrue(TestUtils.check(input, expected, 101))

    def test_2(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "ASSIGN x 15",
            "ASSIGN y 17",
            "ASSIGN x 'abc'",
        ]
        expected = ["TypeMismatch: ASSIGN y 17"]

        self.assertTrue(TestUtils.check(input, expected, 102))

    def test_3(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "BEGIN",
            "INSERT y string",
            "END",
            "END",
        ]
        expected = ["success", "success", "success", "success"]

        self.assertTrue(TestUtils.check(input, expected, 103))

    def test_4(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "LOOKUP x",
            "LOOKUP y",
            "END",
        ]
        expected = ["success", "success", "success", "1", "0"]

        self.assertTrue(TestUtils.check(input, expected, 104))

    def test_5(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "PRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "y//0 x//1 z//1"]

        self.assertTrue(TestUtils.check(input, expected, 105))

    def test_6(self):
        input = [
            "INSERT x number",
            "INSERT y string",
            "BEGIN",
            "INSERT x number",
            "INSERT z number",
            "RPRINT",
            "END",
        ]
        expected = ["success", "success", "success", "success", "z//1 x//1 y//0"]

        self.assertTrue(TestUtils.check(input, expected, 106))
