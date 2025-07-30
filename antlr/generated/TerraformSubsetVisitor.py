# Generated from TerraformSubset.g4 by ANTLR 4.13.1
from antlr4 import *
if "." in __name__:
    from .TerraformSubsetParser import TerraformSubsetParser
else:
    from TerraformSubsetParser import TerraformSubsetParser

# This class defines a complete generic visitor for a parse tree produced by TerraformSubsetParser.

class TerraformSubsetVisitor(ParseTreeVisitor):

    # Visit a parse tree produced by TerraformSubsetParser#terraform.
    def visitTerraform(self, ctx:TerraformSubsetParser.TerraformContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TerraformSubsetParser#block.
    def visitBlock(self, ctx:TerraformSubsetParser.BlockContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TerraformSubsetParser#provider.
    def visitProvider(self, ctx:TerraformSubsetParser.ProviderContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TerraformSubsetParser#resource.
    def visitResource(self, ctx:TerraformSubsetParser.ResourceContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TerraformSubsetParser#variable.
    def visitVariable(self, ctx:TerraformSubsetParser.VariableContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TerraformSubsetParser#output.
    def visitOutput(self, ctx:TerraformSubsetParser.OutputContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TerraformSubsetParser#body.
    def visitBody(self, ctx:TerraformSubsetParser.BodyContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TerraformSubsetParser#keyValue.
    def visitKeyValue(self, ctx:TerraformSubsetParser.KeyValueContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TerraformSubsetParser#expr.
    def visitExpr(self, ctx:TerraformSubsetParser.ExprContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by TerraformSubsetParser#reference.
    def visitReference(self, ctx:TerraformSubsetParser.ReferenceContext):
        return self.visitChildren(ctx)



del TerraformSubsetParser