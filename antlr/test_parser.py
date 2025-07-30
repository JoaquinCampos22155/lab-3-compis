#!/usr/bin/env python3
import sys
from antlr4 import FileStream, CommonTokenStream
from generated.TerraformSubsetLexer import TerraformSubsetLexer
from generated.TerraformSubsetParser import TerraformSubsetParser


input_stream = FileStream("../terraform/main.tf")
lexer = TerraformSubsetLexer(input_stream)
tokens = CommonTokenStream(lexer)
parser = TerraformSubsetParser(tokens)


tree = parser.terraform()


tree_str = tree.toStringTree(recog=parser)
lines = tree_str.split()
print(" Árbol parse (fragmento):")
print(" ".join(lines[:20]), "…")
