from dataclasses import dataclass, field
from typing import Optional, List, Union


@dataclass
class Program:
    functions: List = field(default_factory=list)
    globals: List = field(default_factory=list)


@dataclass
class Stmt:
    pass


@dataclass
class FnDef(Stmt):
    name: str = ""
    params: List[str] = field(default_factory=list)
    body: List[Stmt] = field(default_factory=list)
    line: int = 0


@dataclass
class LetDecl(Stmt):
    name: str = ""
    mutable: bool = False
    initializer: Optional["Expr"] = None
    line: int = 0


@dataclass
class Assign(Stmt):
    name: str = ""
    value: Optional["Expr"] = None
    line: int = 0


@dataclass
class If(Stmt):
    condition: Optional["Expr"] = None
    then_body: List[Stmt] = field(default_factory=list)
    else_body: List[Stmt] = field(default_factory=list)
    line: int = 0


@dataclass
class Match(Stmt):
    expr: Optional["Expr"] = None
    arms: List["MatchArm"] = field(default_factory=list)
    line: int = 0


@dataclass
class MatchArm:
    value: int = 0
    body: List[Stmt] = field(default_factory=list)


@dataclass
class While(Stmt):
    condition: Optional["Expr"] = None
    body: List[Stmt] = field(default_factory=list)
    line: int = 0


@dataclass
class Return(Stmt):
    value: Optional["Expr"] = None
    line: int = 0


@dataclass
class ExprStmt(Stmt):
    expr: Optional["Expr"] = None
    line: int = 0


@dataclass
class Println(Stmt):
    format_str: str = ""
    args: List["Expr"] = field(default_factory=list)
    line: int = 0


@dataclass
class Use(Stmt):
    module: str = ""
    line: int = 0


@dataclass
class Block(Stmt):
    statements: List[Stmt] = field(default_factory=list)


@dataclass
class Expr:
    pass


@dataclass
class Integer(Expr):
    value: int = 0


@dataclass
class StringExpr(Expr):
    value: str = ""


@dataclass
class BoolExpr(Expr):
    value: bool = False


@dataclass
class Ident(Expr):
    name: str = ""


@dataclass
class Binary(Expr):
    op: str = ""
    left: Optional[Expr] = None
    right: Optional[Expr] = None


@dataclass
class Unary(Expr):
    op: str = ""
    operand: Optional[Expr] = None


@dataclass
class Call(Expr):
    callee: str = ""
    args: List[Expr] = field(default_factory=list)
