from rest_framework.filters import BaseFilterBackend
from django.db.models import Q


def build_query_from_dynamic(query: str) -> Q:
    operators = {'or', 'and', 'eq', 'ne', 'gt', 'lt'}
    priority = {'or': 1, 'and': 2, 'eq': 3, 'ne': 3, 'gt': 4, 'lt': 4}

    def tokenize(input_string: str):
        lowercase_string = input_string.lower()
        return lowercase_string.replace('(', ' ( ').replace(')', ' ) ').split()

    def build_query_from_tokens(tokens):
        stack = []
        output = []

        for token in tokens:
            if token in operators:
                while stack and stack[-1] in operators and priority[stack[-1]] >= priority[token]:
                    output.append(stack.pop())
                stack.append(token)
            elif token == '(':
                stack.append(token)
            elif token == ')':
                while stack and stack[-1] != '(':
                    output.append(stack.pop())
                stack.pop()
            else:
                output.append(token)
        while stack:
            output.append(stack.pop())

        return output

    def build_q_object_from_query(ordered_query):
        stack = []
        for token in ordered_query:
            if token in operators:
                element2 = stack.pop()
                element1 = stack.pop()
                if token == 'or':
                    stack.append(element1 | element2)
                elif token == 'and':
                    stack.append(element1 & element2)
                elif token == 'eq':
                    if isinstance(element2, str) and element1 == 'location':
                        stack.append(Q(**{element1 + '__icontains': element2}))
                        #   or __iexact
                    else:
                        stack.append(Q(**{element1: element2}))
                elif token == 'ne':
                    if isinstance(element2, str) and element1 == 'location':
                        stack.append(~Q(**{element1 + '__icontaints': element2}))
                    else:
                        stack.append(~Q(**{element1: element2}))
                elif token == 'gt':
                    stack.append(Q(**{element1 + '__gt': element2}))
                elif token == 'lt':
                    stack.append(Q(**{element1 + '__lt': element2}))
            else:
                stack.append(token)
        return stack[0]
    if query is not None:
        tokenized = tokenize(query)
        if tokenized.count('(') != tokenized.count(')'):
            raise ValueError("Unbalanced parentheses in the query")

        rpn_tokens = build_query_from_tokens(tokenized)
        q_object = build_q_object_from_query(rpn_tokens)
        return q_object


class DynamicFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        value = request.query_params.get("q")
        if value is not None:
            query = build_query_from_dynamic(value)
            return queryset.filter(query)
        else:
            return queryset
