# -*- coding: utf-8 -*-
"""
Gera o PDF de documentacao do projeto Meu Bairro (Global Solution 2026.2).

Edite APENAS as variaveis da secao CONFIGURACAO e rode:
    python docs/gerar_documentacao.py
O PDF sai em docs/Documentacao_MeuBairro.pdf
"""
import math
import os
import re

from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import (BaseDocTemplate, Flowable, Frame, KeepTogether, NextPageTemplate,
                                PageBreak, PageTemplate, Paragraph, Preformatted, Spacer, Table,
                                TableStyle)
from reportlab.platypus.tableofcontents import TableOfContents

# ============================ CONFIGURACAO ============================
PROJETO = "Meu Bairro"
SUBTITULO = "API REST para reportes urbanos e ranking de bairros"
INTEGRANTES = [  # (nome completo, RM)
    ("Leonardo Yukio Iwagoe Ribeiro", "RM562864"),
    ("Lucas Costa Zago", "RM562028"),
]
GITHUB = "https://github.com/Leoyukiio/GS-java"
DEPLOY = ""  # deixe vazio se nao houve deploy; preencha com a URL do Render quando existir
MOTIVO_SEM_DEPLOY = ("não realizado - a conta do Oracle da FIAP estava bloqueada (ORA-28000) até o fechamento "
                     "desta documentação")
# =====================================================================

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "Documentacao_MeuBairro.pdf")

WINE = colors.HexColor("#8B1038")
DARK = colors.HexColor("#222222")
GRAY = colors.HexColor("#666666")
LIGHT = colors.HexColor("#F6F1F3")
LINEC = colors.HexColor("#999999")
WHITE = colors.white

# ------------------------------- estilos -------------------------------
BODY = ParagraphStyle("Body", fontName="Helvetica", fontSize=9.5, leading=13.5, alignment=TA_JUSTIFY,
                      spaceAfter=5, textColor=DARK)
H1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=17, leading=21, textColor=WINE,
                    spaceBefore=0, spaceAfter=10)
H2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=12, leading=15, textColor=DARK,
                    spaceBefore=10, spaceAfter=5)
BUL = ParagraphStyle("Bul", parent=BODY, leftIndent=14, bulletIndent=3, spaceAfter=2, alignment=0)
SMALL = ParagraphStyle("Small", parent=BODY, fontSize=8, leading=10.5, alignment=0, spaceAfter=0)
CELL = ParagraphStyle("Cell", fontName="Helvetica", fontSize=8, leading=10, textColor=DARK)
CELLB = ParagraphStyle("CellB", parent=CELL, fontName="Helvetica-Bold")
CAP = ParagraphStyle("Cap", fontName="Helvetica-Oblique", fontSize=8.5, leading=11, textColor=GRAY,
                     alignment=TA_CENTER, spaceBefore=3, spaceAfter=8)
CODE = ParagraphStyle("Code", fontName="Courier", fontSize=8, leading=10, textColor=DARK,
                      backColor=LIGHT, borderPadding=5, leftIndent=4, rightIndent=4, spaceAfter=8)
CAPA_T = ParagraphStyle("CapaT", fontName="Helvetica-Bold", fontSize=34, leading=40, alignment=TA_CENTER,
                        textColor=WINE)
CAPA_S = ParagraphStyle("CapaS", fontName="Helvetica", fontSize=14, leading=19, alignment=TA_CENTER,
                        textColor=DARK)
CAPA_I = ParagraphStyle("CapaI", fontName="Helvetica", fontSize=10, leading=14, alignment=TA_CENTER,
                        textColor=GRAY)


# ---- acentuacao: o texto-fonte e escrito sem acentos; esta funcao restaura na hora de desenhar ----
_PALAVRAS = {
    "especificacao": "especificação", "solucao": "solução", "participacao": "participação",
    "informacao": "informação", "informacoes": "informações", "gestao": "gestão", "iluminacao": "iluminação",
    "localizacao": "localização", "tambem": "também", "relevancia": "relevância", "ocorrencia": "ocorrência",
    "usuario": "usuário", "usuarios": "usuários", "seguranca": "segurança", "servicos": "serviços",
    "criterio": "critério", "solicitacao": "solicitação", "confirmacao": "confirmação",
    "confirmacoes": "confirmações", "nao": "não", "avanca": "avança", "avancar": "avançar", "negocio": "negócio",
    "indice": "índice", "indices": "índices", "prototipo": "protótipo", "prototipos": "protótipos",
    "pagina": "página", "codigo": "código", "codigos": "códigos", "execucao": "execução",
    "instrucoes": "instruções", "versoes": "versões", "acessivel": "acessível", "publica": "pública",
    "publico": "público", "aplicacao": "aplicação", "descricao": "descrição", "documentacao": "documentação",
    "unico": "único", "unica": "única", "repositorio": "repositório", "restricoes": "restrições",
    "padrao": "padrão", "invalidos": "inválidos", "invalido": "inválido", "notacao": "notação",
    "primaria": "primária", "calcada": "calçada", "populacao": "população", "acoes": "ações",
    "metodo": "método", "dependencias": "dependências", "dominio": "domínio", "excecoes": "exceções",
    "visao": "visão", "posicao": "posição", "inicializacao": "inicialização", "variaveis": "variáveis",
    "comparavel": "comparável", "decisoes": "decisões", "proposito": "propósito", "validacao": "validação",
    "alteracao": "alteração", "edicao": "edição", "so": "só", "tecnologia": "tecnologia",
    "sao": "são", "situacao": "situação", "esta": "está", "cidadao": "cidadão", "extensivel": "extensível", "ultima": "última", "requisicao": "requisição", "requisicoes": "requisições", "regioes": "regiões", "exposicao": "exposição", "utilizando": "utilizando", "tatuape": "Tatuapé", "parametro": "parâmetro", "sera": "será",
}
for _k, _v in list(_PALAVRAS.items()):
    _PALAVRAS[_k.capitalize()] = _v.capitalize() if _k != "tatuape" else _v
_RE_PAL = re.compile(r"\b(" + "|".join(sorted(map(re.escape, _PALAVRAS), key=len, reverse=True)) + r")\b")
_RE_PROT = re.compile(r"(<font face=['\"]Courier['\"][^>]*>.*?</font>|<link .*?</link>)", re.S)


def acc(t):
    partes = _RE_PROT.split(t)
    for i in range(0, len(partes), 2):
        partes[i] = _RE_PAL.sub(lambda m: _PALAVRAS[m.group(1)], partes[i])
    return "".join(partes)


def P(t, s=BODY):
    return Paragraph(acc(t), s)


def bullets(items):
    return [Paragraph(acc(i), BUL, bulletText="•") for i in items]


def deploy_txt():
    return link(DEPLOY) if DEPLOY else MOTIVO_SEM_DEPLOY


def link(url):
    return '<link href="%s" color="#8B1038"><u>%s</u></link>' % (url, url)


# ---------------------------- primitivas de desenho ----------------------------
class Diagram(Flowable):
    def __init__(self, w, h, fn):
        super().__init__()
        self.width, self.height, self.fn = w, h, fn
        self.hAlign = "CENTER"

    def wrap(self, aw, ah):
        return self.width, self.height

    def draw(self):
        self.fn(self.canv)


def box(c, x, top, w, title, lines, stereo=None, head=WINE, fill=LIGHT, fs=6.8, lh=9):
    hh = 22 if stereo else 14
    h = hh + len(lines) * lh + 5
    y = top - h
    c.saveState()
    c.setFillColor(fill)
    c.setStrokeColor(DARK)
    c.setLineWidth(0.8)
    c.rect(x, y, w, h, fill=1, stroke=1)
    c.setFillColor(head)
    c.rect(x, top - hh, w, hh, fill=1, stroke=1)
    c.setFillColor(WHITE)
    if stereo:
        c.setFont("Helvetica-Oblique", 6)
        c.drawCentredString(x + w / 2, top - 8, "<<%s>>" % stereo)
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + w / 2, top - 18, title)
    else:
        c.setFont("Helvetica-Bold", 8)
        c.drawCentredString(x + w / 2, top - 10.5, title)
    c.setFillColor(DARK)
    c.setFont("Helvetica", fs)
    for i, l in enumerate(lines):
        c.drawString(x + 4, top - hh - lh * (i + 1) + 2.4, l)
    c.restoreState()
    return (x, y, w, h)


def top(r, f=0.5):
    return (r[0] + r[2] * f, r[1] + r[3])


def bottom(r, f=0.5):
    return (r[0] + r[2] * f, r[1])


def left(r, f=0.5):
    return (r[0], r[1] + r[3] * f)


def right(r, f=0.5):
    return (r[0] + r[2], r[1] + r[3] * f)


def poly(c, pts, dash=None, arrow=False, color=DARK, w=0.8):
    c.saveState()
    c.setStrokeColor(color)
    c.setFillColor(color)
    c.setLineWidth(w)
    if dash:
        c.setDash(*dash)
    p = c.beginPath()
    p.moveTo(*pts[0])
    for q in pts[1:]:
        p.lineTo(*q)
    c.drawPath(p, stroke=1, fill=0)
    if arrow:
        c.setDash()
        (x1, y1), (x2, y2) = pts[-2], pts[-1]
        a = math.atan2(y2 - y1, x2 - x1)
        L = 5
        pa = c.beginPath()
        pa.moveTo(x2, y2)
        pa.lineTo(x2 - L * math.cos(a - 0.4), y2 - L * math.sin(a - 0.4))
        pa.lineTo(x2 - L * math.cos(a + 0.4), y2 - L * math.sin(a + 0.4))
        pa.close()
        c.drawPath(pa, fill=1, stroke=0)
    c.restoreState()


def lbl(c, x, y, t, size=6.5, color=DARK, center=False):
    t = acc(t) if len(t) > 3 and " " in t else t
    c.saveState()
    c.setFillColor(color)
    c.setFont("Helvetica-Bold", size)
    if center:
        c.drawCentredString(x, y, t)
    else:
        c.drawString(x, y, t)
    c.restoreState()


# ------------------------------ DIAGRAMA 1: camadas ------------------------------
def desenha_camadas(c):
    W = 500
    ctrl = {
        "bairro": box(c, 0, 495, 115, "BairroController", [m + "()" for m in
                      ["criar", "listar", "detalhar", "atualizar", "remover", "indicadores",
                       "salvarIndicadores", "ranking"]], "controller"),
        "usuario": box(c, 128, 495, 115, "UsuarioController", [m + "()" for m in
                       ["criar", "listar", "buscar", "atualizar", "remover"]], "controller"),
        "reporte": box(c, 256, 495, 244, "ReporteController", [m + "()" for m in
                       ["criar", "listar", "buscar", "atualizar", "alterarStatus", "remover",
                        "votar", "votos", "removerVoto"]], "controller"),
    }
    bo = {
        "bairro": box(c, 0, 360, 115, "BairroBO", [m + "()" for m in
                      ["criar", "listar", "buscar", "atualizar", "remover", "buscarIndicadores",
                       "salvarIndicadores", "detalhar", "ranking", "calcularNota"]], "bo"),
        "usuario": box(c, 128, 360, 115, "UsuarioBO", [m + "()" for m in
                       ["criar", "listar", "buscar", "atualizar", "remover"]], "bo"),
        "reporte": box(c, 256, 360, 115, "ReporteBO", [m + "()" for m in
                       ["criar", "listar", "buscar", "atualizar", "alterarStatus", "remover"]], "bo"),
        "voto": box(c, 385, 360, 115, "VotoBO", [m + "()" for m in
                    ["votar", "listar", "removerVoto"]], "bo"),
    }
    xs = [0, 102, 204, 306, 408]
    dao = {
        "bairro": box(c, xs[0], 215, 92, "BairroDao", [m + "()" for m in
                      ["inserir", "listar", "buscarPorId", "existeNomeNaCidade", "atualizar",
                       "remover", "temDependentes"]], "dao"),
        "usuario": box(c, xs[1], 215, 92, "UsuarioDao", [m + "()" for m in
                       ["inserir", "listar", "buscarPorId", "existeEmail", "atualizar", "remover",
                        "temDependentes"]], "dao"),
        "indic": box(c, xs[2], 215, 92, "IndicadorBairroDao", [m + "()" for m in
                     ["buscarPorBairro", "listar", "salvar", "removerPorBairro"]], "dao"),
        "reporte": box(c, xs[3], 215, 92, "ReporteDao", [m + "()" for m in
                       ["inserir", "listar", "buscarPorId", "atualizarDados", "atualizarStatus",
                        "remover"]], "dao"),
        "voto": box(c, xs[4], 215, 92, "VotoDao", [m + "()" for m in
                    ["inserir", "buscarPorId", "listarPorReporte", "existe", "remover",
                     "removerPorReporte"]], "dao"),
    }
    db = box(c, 0, 95, W, "Oracle FIAP", ["tb_mb_bairro  |  tb_mb_usuario  |  tb_mb_reporte  |  "
                                           "tb_mb_voto  |  tb_mb_indicador_bairro"], None,
             head=DARK, fill=colors.HexColor("#EDEDED"))
    exc = box(c, 0, 52, W, "GlobalExceptionHandler (@RestControllerAdvice)",
              ["RecursoNaoEncontradoException -> 404   |   RegraNegocioException -> 422   |   "
               "ConflitoException -> 409",
               "Validação / JSON inválido / parâmetro inválido -> 400   |   Erro de banco -> 503   |   "
               "Demais erros -> 500",
               "Todas as respostas de erro seguem o formato ApiError."], "exception")

    g = colors.HexColor("#7A7A7A")

    def seta(a, b):
        poly(c, [a, b], arrow=True, color=g, w=0.6)

    seta(bottom(ctrl["bairro"]), top(bo["bairro"]))
    seta(bottom(ctrl["usuario"]), top(bo["usuario"]))
    seta(bottom(ctrl["reporte"], 0.25), top(bo["reporte"]))
    seta(bottom(ctrl["reporte"], 0.85), top(bo["voto"]))
    # BO -> DAO
    pares = [("bairro", "bairro"), ("bairro", "indic"),
             ("usuario", "usuario"), ("usuario", "bairro"),
             ("reporte", "reporte"), ("reporte", "voto"), ("reporte", "bairro"), ("reporte", "usuario"),
             ("voto", "voto"), ("voto", "reporte"), ("voto", "usuario")]
    for i, (b, d) in enumerate(pares):
        f1 = 0.2 + 0.6 * ((i % 4) / 3.0)
        seta(bottom(bo[b], f1), top(dao[d], 0.5))
    for d in dao.values():
        seta(bottom(d), top(db, (d[0] + d[2] / 2) / W))


# ------------------------------ DIAGRAMA 2: dominio ------------------------------
def desenha_dominio(c):
    bairro = box(c, 190, 470, 130, "Bairro", ["id: Long", "nome: String", "cidade: String", "uf: String",
                                              "populacao: Integer"])
    indic = box(c, 370, 470, 130, "IndicadorBairro", ["id: Long", "bairroId: Long",
                                                      "infraestrutura: BigDecimal", "seguranca: BigDecimal",
                                                      "servicos: BigDecimal", "lazer: BigDecimal"])
    usuario = box(c, 0, 350, 130, "Usuario", ["id: Long", "nome: String", "email: String",
                                              "perfil: Perfil", "bairroId: Long"])
    reporte = box(c, 190, 330, 130, "Reporte", ["id: Long", "usuarioId: Long", "bairroId: Long",
                                                "categoria: Categoria", "descricao: String",
                                                "latitude: Double", "longitude: Double",
                                                "status: Status", "criadoEm: LocalDateTime",
                                                "resolvidoEm: LocalDateTime", "votos: Integer"])
    resumo = box(c, 370, 330, 130, "BairroResumo", ["bairro: Bairro", "indicadores: IndicadorBairro",
                                                    "nota: BigDecimal", "posicao: Integer"])
    voto = box(c, 190, 150, 130, "Voto", ["id: Long", "reporteId: Long", "usuarioId: Long",
                                          "criadoEm: LocalDateTime"])
    categoria = box(c, 370, 240, 130, "Categoria", ["BURACO", "ILUMINACAO", "LIXO", "ALAGAMENTO", "OUTRO"],
                    "enumeration", head=GRAY)
    status = box(c, 370, 150, 130, "Status", ["ABERTO", "EM_ANDAMENTO", "RESOLVIDO"], "enumeration",
                 head=GRAY)
    perfil = box(c, 370, 85, 130, "Perfil", ["MORADOR", "ADMIN"], "enumeration", head=GRAY)

    # Bairro 1 - 0..* Usuario
    a = left(bairro, 0.55)
    poly(c, [a, (65, a[1]), top(usuario, 0.5)])
    lbl(c, a[0] - 8, a[1] + 3, "1")
    lbl(c, 69, top(usuario)[1] + 4, "0..*")
    # Bairro 1 - 0..* Reporte
    poly(c, [bottom(bairro, 0.5), top(reporte, 0.5)])
    lbl(c, 258, bairro[1] - 9, "1")
    lbl(c, 258, reporte[1] + reporte[3] + 3, "0..*")
    # Bairro 1 - 0..1 Indicador
    a, b = right(bairro, 0.55), left(indic, 0.55)
    poly(c, [a, b])
    lbl(c, a[0] + 3, a[1] + 3, "1")
    lbl(c, b[0] - 16, b[1] + 3, "0..1")
    # Usuario 1 - 0..* Reporte
    a, b = right(usuario, 0.45), left(reporte, 0.6)
    poly(c, [a, (155, a[1]), (155, b[1]), b])
    lbl(c, a[0] + 3, a[1] + 3, "1")
    lbl(c, b[0] - 20, b[1] + 3, "0..*")
    # Reporte 1 - 0..* Voto
    poly(c, [bottom(reporte, 0.5), top(voto, 0.5)])
    lbl(c, 258, reporte[1] - 9, "1")
    lbl(c, 258, voto[1] + voto[3] + 3, "0..*")
    # Usuario 1 - 0..* Voto
    a, b = bottom(usuario, 0.5), left(voto, 0.5)
    poly(c, [a, (a[0], b[1]), b])
    lbl(c, a[0] + 3, a[1] - 9, "1")
    lbl(c, b[0] - 20, b[1] + 3, "0..*")
    # BairroResumo agrega Bairro e Indicador (dependencia)
    poly(c, [top(resumo, 0.15), (top(resumo, 0.15)[0], 385), (310, 385), (310, bairro[1])],
         dash=(2, 2), arrow=True)
    poly(c, [top(resumo, 0.7), bottom(indic, 0.45)], dash=(2, 2), arrow=True)
    lbl(c, 405, 378, "usa", 6, GRAY)
    # enums
    a, b = right(reporte, 0.3), left(categoria, 0.5)
    poly(c, [a, b], dash=(2, 2), arrow=True)
    a, b = right(reporte, 0.12), left(status, 0.5)
    poly(c, [a, b], dash=(2, 2), arrow=True)
    a = bottom(usuario, 0.2)
    poly(c, [a, (a[0], 20), (345, 20), (345, perfil[1] + perfil[3] * 0.5), left(perfil, 0.5)],
         dash=(2, 2), arrow=True)
    lbl(c, 250, 24, "perfil", 6, GRAY)


# ------------------------------ DIAGRAMA 3: DER ------------------------------
def desenha_der(c):
    bairro = box(c, 180, 440, 140, "TB_MB_BAIRRO", ["PK  id_bairro  NUMBER", "nome  VARCHAR2(100)",
                                                    "cidade  VARCHAR2(100)", "uf  CHAR(2)",
                                                    "populacao  NUMBER(10)", "UK (nome, cidade)"],
                 head=WINE)
    usuario = box(c, 0, 440, 140, "TB_MB_USUARIO", ["PK  id_usuario  NUMBER", "nome  VARCHAR2(100)",
                                                    "UK  email  VARCHAR2(150)", "perfil  VARCHAR2(10)",
                                                    "FK  id_bairro  NUMBER"], head=WINE)
    indic = box(c, 360, 440, 140, "TB_MB_INDICADOR_BAIRRO",
                ["PK  id_indicador  NUMBER", "FK/UK  id_bairro  NUMBER", "infraestrutura  NUMBER(3,1)",
                 "seguranca  NUMBER(3,1)", "servicos  NUMBER(3,1)", "lazer  NUMBER(3,1)"], head=WINE)
    reporte = box(c, 180, 280, 140, "TB_MB_REPORTE",
                  ["PK  id_reporte  NUMBER", "FK  id_usuario  NUMBER", "FK  id_bairro  NUMBER",
                   "categoria  VARCHAR2(15)", "descricao  VARCHAR2(500)", "latitude  NUMBER(9,6)",
                   "longitude  NUMBER(9,6)", "status  VARCHAR2(15)", "criado_em  TIMESTAMP",
                   "resolvido_em  TIMESTAMP"], head=WINE)
    voto = box(c, 180, 120, 140, "TB_MB_VOTO", ["PK  id_voto  NUMBER", "FK  id_reporte  NUMBER",
                                                "FK  id_usuario  NUMBER", "criado_em  TIMESTAMP",
                                                "UK (id_reporte, id_usuario)"], head=WINE)

    a, b = (180, 410), (140, 410)
    poly(c, [a, b])
    lbl(c, a[0] - 8, a[1] + 3, "1")
    lbl(c, b[0] + 3, b[1] + 3, "N")
    a, b = (320, 410), (360, 410)
    poly(c, [a, b])
    lbl(c, a[0] + 3, a[1] + 3, "1")
    lbl(c, b[0] - 8, b[1] + 3, "1")
    a, b = bottom(bairro, 0.5), top(reporte, 0.5)
    poly(c, [a, b])
    lbl(c, a[0] + 4, a[1] - 9, "1")
    lbl(c, b[0] + 4, b[1] + 3, "N")
    a, b = bottom(usuario, 0.65), left(reporte, 0.75)
    poly(c, [a, (a[0], b[1]), b])
    lbl(c, a[0] + 4, a[1] - 9, "1")
    lbl(c, b[0] - 8, b[1] + 3, "N")
    a, b = bottom(reporte, 0.5), top(voto, 0.5)
    poly(c, [a, b])
    lbl(c, a[0] + 4, a[1] - 9, "1")
    lbl(c, b[0] + 4, b[1] + 3, "N")
    a, b = bottom(usuario, 0.2), left(voto, 0.5)
    poly(c, [a, (a[0], b[1]), b])
    lbl(c, a[0] + 4, a[1] - 9, "1")
    lbl(c, b[0] - 8, b[1] + 3, "N")
    lbl(c, 360, 330, "Notacao: 1 = um   N = muitos", 6.5, GRAY)
    lbl(c, 360, 320, "PK = chave primaria", 6.5, GRAY)
    lbl(c, 360, 310, "FK = chave estrangeira", 6.5, GRAY)
    lbl(c, 360, 300, "UK = chave unica", 6.5, GRAY)


# ------------------------------ PROTOTIPOS ------------------------------
def rrect(c, x, y, w, h, r=3, fill=None, stroke=LINEC, lw=0.6):
    c.saveState()
    if fill is not None:
        c.setFillColor(fill)
    if stroke:
        c.setStrokeColor(stroke)
    c.setLineWidth(lw)
    c.roundRect(x, y, w, h, r, fill=1 if fill is not None else 0, stroke=1 if stroke else 0)
    c.restoreState()


def txt(c, x, y, t, size=6.5, bold=False, color=DARK, center=False, right_=False):
    t = acc(t)
    c.saveState()
    c.setFillColor(color)
    c.setFont("Helvetica-Bold" if bold else "Helvetica", size)
    if center:
        c.drawCentredString(x, y, t)
    elif right_:
        c.drawRightString(x, y, t)
    else:
        c.drawString(x, y, t)
    c.restoreState()


def botao(c, x, y, w, h, t, fill=WINE, color=WHITE):
    rrect(c, x, y, w, h, 3, fill=fill, stroke=None)
    txt(c, x + w / 2, y + h / 2 - 2.2, t, 6.5, True, color, center=True)


def campo(c, x, y, w, label, valor="", h=13):
    txt(c, x, y + h + 2, label, 6, True, GRAY)
    rrect(c, x, y, w, h, 2, fill=WHITE, stroke=LINEC)
    if valor:
        txt(c, x + 4, y + h / 2 - 2.2, valor, 6.5, False, DARK)


def chip(c, x, y, t, fill, color=WHITE):
    w = len(t) * 4.0 + 8
    rrect(c, x, y, w, 10, 5, fill=fill, stroke=None)
    txt(c, x + w / 2, y + 3, t, 5.8, True, color, center=True)
    return w


def janela(c, x, y, w, h, url):
    rrect(c, x, y, w, h, 5, fill=WHITE, stroke=DARK, lw=0.9)
    c.saveState()
    c.setFillColor(colors.HexColor("#E6E6E6"))
    c.roundRect(x, y + h - 16, w, 16, 5, fill=1, stroke=0)
    c.rect(x, y + h - 16, w, 8, fill=1, stroke=0)
    for i, col in enumerate(["#E5534B", "#E5B94B", "#57AB5A"]):
        c.setFillColor(colors.HexColor(col))
        c.circle(x + 8 + i * 8, y + h - 8, 2.4, fill=1, stroke=0)
    c.restoreState()
    rrect(c, x + 36, y + h - 13, w - 44, 10, 5, fill=WHITE, stroke=None)
    txt(c, x + 42, y + h - 10.3, url, 5.8, False, GRAY)
    # cabecalho do app
    c.saveState()
    c.setFillColor(WINE)
    c.rect(x, y + h - 34, w, 18, fill=1, stroke=0)
    c.restoreState()
    txt(c, x + 8, y + h - 28, "Meu Bairro", 8, True, WHITE)
    txt(c, x + w - 8, y + h - 27.5, "Ranking   Reportes   Novo reporte", 5.8, False, WHITE, right_=True)
    return y + h - 34  # topo da area de conteudo


def tela_ranking(c, x, y, w, h):
    t = janela(c, x, y, w, h, "meubairro.app/ranking")
    txt(c, x + 10, t - 15, "Ranking de bairros", 9, True, WINE)
    txt(c, x + 10, t - 25, "Nota = 35% infra + 25% seguranca + 20% servicos + 20% lazer", 5.5, False, GRAY)
    dados = [("1", "Pinheiros", 8.2), ("2", "Vila Mariana", 7.6), ("3", "Tatuape", 7.1), ("4", "Mooca", 6.3)]
    yy = t - 48
    for pos, nome, nota in dados:
        rrect(c, x + 10, yy, w - 20, 22, 3, fill=LIGHT, stroke=None)
        txt(c, x + 16, yy + 8, pos + "\u00ba", 8, True, WINE)
        txt(c, x + 34, yy + 8, nome, 7.5, True)
        rrect(c, x + 100, yy + 8, 70, 5, 2, fill=colors.HexColor("#DDDDDD"), stroke=None)
        rrect(c, x + 100, yy + 8, 70 * nota / 10, 5, 2, fill=WINE, stroke=None)
        txt(c, x + w - 16, yy + 8, "%.1f" % nota, 8, True, right_=True)
        yy -= 27


def tela_bairro(c, x, y, w, h):
    t = janela(c, x, y, w, h, "meubairro.app/bairros/1")
    txt(c, x + 10, t - 15, "Pinheiros", 10, True, WINE)
    txt(c, x + 10, t - 25, "Sao Paulo / SP  -  65.000 habitantes", 6, False, GRAY)
    rrect(c, x + w - 62, t - 28, 52, 22, 4, fill=WINE, stroke=None)
    txt(c, x + w - 36, t - 15, "8,2", 10, True, WHITE, center=True)
    txt(c, x + w - 36, t - 23, "1\u00ba lugar", 5.5, False, WHITE, center=True)
    ind = [("Infraestrutura", 8.5), ("Seguranca", 7.8), ("Servicos", 8.4), ("Lazer", 7.9)]
    yy = t - 48
    for nome, v in ind:
        txt(c, x + 10, yy, nome, 6.5, True)
        rrect(c, x + 70, yy - 1, 110, 6, 3, fill=colors.HexColor("#DDDDDD"), stroke=None)
        rrect(c, x + 70, yy - 1, 110 * v / 10, 6, 3, fill=WINE, stroke=None)
        txt(c, x + w - 12, yy, "%.1f" % v, 7, True, right_=True)
        yy -= 17
    botao(c, x + 10, y + 12, 100, 15, "Ver reportes do bairro")
    botao(c, x + 118, y + 12, 105, 15, "Editar indicadores", fill=GRAY)


def tela_lista(c, x, y, w, h):
    t = janela(c, x, y, w, h, "meubairro.app/reportes")
    txt(c, x + 10, t - 14, "Reportes", 9, True, WINE)
    campo(c, x + 10, t - 38, 65, "Bairro", "Pinheiros")
    campo(c, x + 82, t - 38, 65, "Status", "Todos")
    campo(c, x + 154, t - 38, 70, "Categoria", "Todas")
    yy = t - 82
    itens = [("BURACO", "Buraco grande na calcada...", "ABERTO", 12, colors.HexColor("#C0392B")),
             ("ILUMINACAO", "Poste apagado na rua...", "EM_ANDAMENTO", 7, colors.HexColor("#B9770E")),
             ("LIXO", "Lixo acumulado na esquina...", "RESOLVIDO", 3, colors.HexColor("#1E8449"))]
    for cat, desc, st, v, cor in itens:
        rrect(c, x + 10, yy, w - 20, 30, 3, fill=WHITE, stroke=LINEC)
        wc = chip(c, x + 14, yy + 18, cat, GRAY)
        chip(c, x + 18 + wc, yy + 18, st, cor)
        txt(c, x + 14, yy + 8, desc, 6.3)
        txt(c, x + 14, yy + 2, "%d confirmacoes" % v, 5.5, False, GRAY)
        botao(c, x + w - 62, yy + 4, 46, 12, "Tambem vejo", fill=WINE)
        yy -= 35


def tela_novo(c, x, y, w, h):
    t = janela(c, x, y, w, h, "meubairro.app/reportes/novo")
    txt(c, x + 10, t - 14, "Novo reporte", 9, True, WINE)
    campo(c, x + 10, t - 38, 100, "Usuario (id)", "2")
    campo(c, x + 118, t - 38, 107, "Bairro", "Vila Mariana")
    campo(c, x + 10, t - 64, 100, "Categoria", "BURACO")
    campo(c, x + 10, t - 108, w - 20, "Descricao", "Buraco grande na calcada em frente ao n\u00ba 100", h=32)
    campo(c, x + 10, t - 134, 100, "Latitude", "-23.5871")
    campo(c, x + 118, t - 134, 107, "Longitude", "-46.6384")
    botao(c, x + 10, y + 5, 70, 14, "Enviar reporte")
    botao(c, x + 88, y + 5, 50, 14, "Cancelar", fill=GRAY)


def tela_detalhe(c, x, y, w, h):
    t = janela(c, x, y, w, h, "meubairro.app/reportes/7")
    txt(c, x + 10, t - 14, "Reporte #7", 9, True, WINE)
    chip(c, x + 10, t - 30, "BURACO", GRAY)
    txt(c, x + 10, t - 44, "Buraco grande na calcada em frente ao no 100", 6.5)
    txt(c, x + 10, t - 53, "Vila Mariana  -  lat -23.5871, lon -46.6384  -  por Maria Souza", 5.6, False, GRAY)
    etapas = ["ABERTO", "EM_ANDAMENTO", "RESOLVIDO"]
    xs = [x + 36, x + w / 2, x + w - 36]
    poly(c, [(xs[0], t - 72), (xs[2], t - 72)], color=LINEC, w=1.2)
    for i, e in enumerate(etapas):
        c.saveState()
        c.setFillColor(WINE if i <= 1 else WHITE)
        c.setStrokeColor(WINE)
        c.circle(xs[i], t - 72, 4.5, fill=1, stroke=1)
        c.restoreState()
        txt(c, xs[i], t - 85, e, 5.8, True, WINE if i <= 1 else GRAY, center=True)
    txt(c, x + 10, t - 104, "12 vizinhos confirmaram", 6.8, True)
    botao(c, x + 10, y + 34, 70, 15, "Tambem vejo")
    botao(c, x + 88, y + 34, 80, 15, "Remover meu voto", fill=GRAY)
    txt(c, x + 10, y + 22, "Acoes de administrador (perfil ADMIN):", 5.6, False, GRAY)
    botao(c, x + 10, y + 6, 80, 14, "Avancar status", fill=colors.HexColor("#B9770E"))
    botao(c, x + 98, y + 6, 55, 14, "Excluir", fill=colors.HexColor("#C0392B"))


def tela_admin(c, x, y, w, h):
    t = janela(c, x, y, w, h, "meubairro.app/admin/bairros")
    txt(c, x + 10, t - 14, "Cadastro de bairro e indicadores", 9, True, WINE)
    campo(c, x + 10, t - 38, 100, "Nome", "Mooca")
    campo(c, x + 118, t - 38, 70, "Cidade", "Sao Paulo")
    campo(c, x + 194, t - 38, 30, "UF", "SP")
    campo(c, x + 10, t - 64, 100, "Populacao", "87000")
    yy = t - 84
    for nome, v in [("Infraestrutura", 5.9), ("Seguranca", 6.6), ("Servicos", 6.8), ("Lazer", 6.3)]:
        txt(c, x + 10, yy, nome, 6.3, True)
        poly(c, [(x + 75, yy + 2), (x + 175, yy + 2)], color=LINEC, w=1.5)
        c.saveState()
        c.setFillColor(WINE)
        c.circle(x + 75 + 100 * v / 10, yy + 2, 3.5, fill=1, stroke=0)
        c.restoreState()
        txt(c, x + w - 12, yy, "%.1f" % v, 6.8, True, right_=True)
        yy -= 14
    botao(c, x + 10, y + 8, 60, 15, "Salvar")
    botao(c, x + 78, y + 8, 60, 15, "Excluir", fill=colors.HexColor("#C0392B"))


TELAS = [
    ("Tela 1 - Ranking de bairros", "GET /ranking", tela_ranking),
    ("Tela 2 - Detalhe do bairro", "GET /bairros/{id}", tela_bairro),
    ("Tela 3 - Lista de reportes", "GET /reportes  |  POST /reportes/{id}/votos", tela_lista),
    ("Tela 4 - Novo reporte", "POST /reportes", tela_novo),
    ("Tela 5 - Detalhe do reporte", "GET /reportes/{id}  |  PUT /reportes/{id}/status  |  DELETE", tela_detalhe),
    ("Tela 6 - Cadastro de bairro", "POST /bairros  |  PUT /bairros/{id}/indicadores", tela_admin),
]


def linha_prototipos(par):
    def fn(c):
        for i, (titulo, api, f) in enumerate(par):
            x = i * 260
            f(c, x, 20, 240, 192)
            txt(c, x + 120, 9, titulo, 7.5, True, DARK, center=True)
            txt(c, x + 120, 1, api, 6, False, GRAY, center=True)
    return Diagram(500, 216, fn)


# ------------------------------ DOCUMENTO ------------------------------
class Doc(BaseDocTemplate):
    def __init__(self, fn):
        super().__init__(fn, pagesize=A4, leftMargin=55, rightMargin=55, topMargin=50, bottomMargin=48,
                         title="Documentação - %s" % PROJETO, author="CitizenTech", subject="Global Solution 2026.2")
        fr = Frame(self.leftMargin, self.bottomMargin, self.width, self.height, id="f")
        self.addPageTemplates([PageTemplate(id="capa", frames=[fr], onPage=self._capa),
                               PageTemplate(id="normal", frames=[fr], onPage=self._normal)])

    def _capa(self, c, d):
        c.saveState()
        c.setFillColor(WINE)
        c.rect(0, A4[1] - 18, A4[0], 18, fill=1, stroke=0)
        c.rect(0, 0, A4[0], 18, fill=1, stroke=0)
        c.restoreState()

    def _normal(self, c, d):
        c.saveState()
        c.setStrokeColor(WINE)
        c.setLineWidth(1)
        c.line(55, A4[1] - 40, A4[0] - 55, A4[1] - 40)
        c.setFont("Helvetica", 8)
        c.setFillColor(GRAY)
        c.drawString(55, A4[1] - 34, acc("%s - %s" % (PROJETO, SUBTITULO)))
        c.drawRightString(A4[0] - 55, A4[1] - 34, "FIAP - Global Solution 2026.2")
        c.drawString(55, 30, "CitizenTech - Engenharia de Software - Domain Driven Design (Java)")
        c.drawRightString(A4[0] - 55, 30, "Página %d" % d.page)
        c.restoreState()

    def afterFlowable(self, f):
        if isinstance(f, Paragraph) and f.style.name in ("H1", "H2"):
            self.notify("TOCEntry", (0 if f.style.name == "H1" else 1, f.getPlainText(), self.page))


def tabela(dados, larguras, header=True, extra=None, zebra=True):
    t = Table(dados, colWidths=larguras, repeatRows=1 if header else 0)
    est = [("VALIGN", (0, 0), (-1, -1), "MIDDLE"), ("GRID", (0, 0), (-1, -1), 0.4, LINEC),
           ("TOPPADDING", (0, 0), (-1, -1), 3), ("BOTTOMPADDING", (0, 0), (-1, -1), 3)]
    if header:
        est += [("BACKGROUND", (0, 0), (-1, 0), WINE), ("TEXTCOLOR", (0, 0), (-1, 0), WHITE)]
    if zebra:
        for i in range(1 if header else 0, len(dados)):
            if i % 2 == 0:
                est.append(("BACKGROUND", (0, i), (-1, i), LIGHT))
    t.setStyle(TableStyle(est + (extra or [])))
    return t


def hcell(t):
    return Paragraph('<font color="white"><b>%s</b></font>' % acc(t), CELL)


COR_METODO = {"GET": "#1a7f37", "POST": "#0b5cad", "PUT": "#b45f06", "DELETE": "#b3261e"}

ENDPOINTS = [
    ("GET", "/bairros", "Lista os bairros", "200", "-"),
    ("GET", "/bairros/{id}", "Detalha o bairro com indicadores, nota e posicao no ranking", "200", "404"),
    ("POST", "/bairros", "Cria um bairro", "201", "400, 409"),
    ("PUT", "/bairros/{id}", "Atualiza um bairro", "200", "400, 404, 409"),
    ("DELETE", "/bairros/{id}", "Remove o bairro (apenas sem reportes/usuarios vinculados)", "204", "404, 422"),
    ("GET", "/bairros/{id}/indicadores", "Consulta os indicadores do bairro", "200", "404"),
    ("PUT", "/bairros/{id}/indicadores", "Define os indicadores (0 a 10)", "200", "400, 404"),
    ("GET", "/ranking", "Ranking de bairros pela nota", "200", "-"),
    ("GET", "/usuarios", "Lista usuarios", "200", "-"),
    ("GET", "/usuarios/{id}", "Detalha usuario", "200", "404"),
    ("POST", "/usuarios", "Cria usuario (e-mail unico)", "201", "400, 404, 409"),
    ("PUT", "/usuarios/{id}", "Atualiza usuario", "200", "400, 404, 409"),
    ("DELETE", "/usuarios/{id}", "Remove usuario (apenas sem reportes/votos)", "204", "404, 422"),
    ("GET", "/reportes?bairroId=&status=&categoria=", "Lista reportes com filtros opcionais", "200", "400"),
    ("GET", "/reportes/{id}", "Detalha reporte (inclui quantidade de votos)", "200", "404"),
    ("POST", "/reportes", "Cria reporte (nasce com status ABERTO)", "201", "400, 404"),
    ("PUT", "/reportes/{id}", "Edita reporte (nao permitido se RESOLVIDO)", "200", "400, 404, 422"),
    ("PUT", "/reportes/{id}/status", "Avanca o status; somente usuario ADMIN", "200", "400, 404, 422"),
    ("DELETE", "/reportes/{id}", "Remove o reporte e seus votos", "204", "404"),
    ("GET", "/reportes/{id}/votos", "Lista votos do reporte", "200", "404"),
    ("POST", "/reportes/{id}/votos", "Confirma o reporte (um voto por usuario)", "201", "400, 404, 409, 422"),
    ("DELETE", "/reportes/{id}/votos/{usuarioId}", "Remove o voto do usuario", "204", "404"),
]


def monta():
    s = []
    # ---------- CAPA ----------
    s += [Spacer(1, 70), P("FIAP - Engenharia de Software", CAPA_I), P("Global Solution 2026.2 - CitizenTech", CAPA_I),
          P("Domain Driven Design - Java", CAPA_I), Spacer(1, 70), P(PROJETO, CAPA_T), Spacer(1, 8),
          P(SUBTITULO, CAPA_S), Spacer(1, 60)]
    linhas = [[hcell("Integrante"), hcell("RM")]] + [[P(n, CELL), P(rm, CELL)] for n, rm in INTEGRANTES]
    s += [tabela(linhas, [330, 110]), Spacer(1, 40),
          P("Repositório: " + link(GITHUB), ParagraphStyle("l", parent=CAPA_I, textColor=DARK)),
          P("Deploy: " + deploy_txt(), ParagraphStyle("l2", parent=CAPA_I, textColor=DARK)),
          NextPageTemplate("normal"), PageBreak()]

    # ---------- INDICE ----------
    toc = TableOfContents()
    toc.levelStyles = [
        ParagraphStyle("t0", fontName="Helvetica-Bold", fontSize=10.5, leading=15, spaceBefore=6),
        ParagraphStyle("t1", fontName="Helvetica", fontSize=9.5, leading=13, leftIndent=16)]
    s += [P("Indice", ParagraphStyle("IdxT", parent=H1)), toc, PageBreak()]

    # ---------- 1. ESPECIFICACAO ----------
    s.append(P("1. Especificacao do projeto", H1))
    s.append(P("1.1 Descritivo da solucao", H2))
    s.append(P("<b>Meu Bairro</b> é uma API REST que transforma a participacao dos moradores em informacao util "
               "para a gestao urbana. Qualquer morador pode <b>reportar um problema</b> do seu bairro (buraco, "
               "iluminacao, lixo, alagamento ou outro), informando descricao e localizacao (latitude e longitude). "
               "Os vizinhos que enfrentam o mesmo problema <b>confirmam o reporte com um voto</b> (\"tambem vejo\"), "
               "o que ajuda a medir a relevancia de cada ocorrencia. Usuarios com perfil <b>ADMIN</b> (equipe da "
               "prefeitura/gestao) acompanham o reporte e fazem seu status avancar de <b>ABERTO</b> para "
               "<b>EM_ANDAMENTO</b> e depois <b>RESOLVIDO</b>."))
    s.append(P("Alem dos reportes, cada bairro possui quatro <b>indicadores de 0 a 10</b> (infraestrutura, "
               "seguranca, servicos e lazer). A aplicacao calcula uma <b>nota ponderada</b> e monta um "
               "<b>ranking</b> de bairros, permitindo comparar a qualidade de vida entre regioes de forma "
               "transparente."))
    s.append(P("1.2 Justificativa", H2))
    s.append(P("Problemas urbanos do dia a dia costumam ser comunicados de forma dispersa e sem um criterio claro de "
               "prioridade: o poder publico nem sempre sabe quantas pessoas sao afetadas, e o morador nao "
               "acompanha o andamento da solicitacao. A confirmacao por vizinhos cria um sinal objetivo de "
               "prioridade, o controle de status devolve visibilidade ao cidadao e os indicadores por bairro "
               "oferecem uma base comparavel para decisoes. A solucao representa o dominio do problema em uma "
               "aplicacao organizada em camadas e extensivel, alinhada ao proposito da CitizenTech de aproximar "
               "tecnologia e cidadania."))
    s.append(P("1.3 Objetivos", H2))
    s.append(P("<b>Objetivo geral:</b> disponibilizar uma API RESTful em Java com Spring Boot, persistida em banco "
               "Oracle, que permita registrar, confirmar e acompanhar problemas urbanos e avaliar bairros por "
               "meio de indicadores e ranking."))
    s += bullets([
        "Modelar o dominio (bairros, usuarios, reportes, votos e indicadores) em uma camada <i>model</i> fiel ao banco de dados.",
        "Isolar o acesso a dados (DAO, JDBC com SQL explicito) das regras de negocio (BO) e da exposicao HTTP (Controller).",
        "Expor os verbos GET, POST, PUT e DELETE para todos os recursos, com validacao dos dados de entrada.",
        "Padronizar o tratamento de erros em uma camada de excecoes com respostas JSON consistentes.",
        "Publicar a aplicacao na nuvem (Render) com documentacao interativa via Swagger UI.",
    ])
    s.append(P("1.4 Regras de negocio", H2))
    s += bullets([
        "<b>Nota do bairro</b> = 0,35 x infraestrutura + 0,25 x seguranca + 0,20 x servicos + 0,20 x lazer (uma casa decimal, arredondamento HALF_UP).",
        "O <b>status</b> do reporte so avanca: ABERTO, EM_ANDAMENTO, RESOLVIDO; somente usuarios <b>ADMIN</b> podem altera-lo.",
        "Reporte <b>RESOLVIDO</b> nao aceita edicao nem novos votos.",
        "O <b>autor</b> do reporte nao pode votar nele; cada usuario vota <b>uma unica vez</b> por reporte.",
        "O <b>e-mail</b> do usuário é único; o par (nome, cidade) do bairro é único.",
        "Bairro só é removido sem reportes/usuários vinculados; usuário só é removido sem reportes/votos.",
    ])
    s.append(P("1.5 Tecnologias", H2))
    tec = [[hcell("Item"), hcell("Uso")],
           [P("Java 21", CELL), P("Linguagem (records para o modelo, enums para dominio fechado)", CELL)],
           [P("Spring Boot 3.3.5", CELL), P("Web (REST), validacao (Bean Validation) e inicializacao", CELL)],
           [P("Spring JDBC (JdbcTemplate)", CELL), P("Camada DAO com SQL explicito", CELL)],
           [P("Oracle (servidor FIAP) / ojdbc11", CELL), P("Banco de dados relacional", CELL)],
           [P("springdoc-openapi 2.6.0", CELL), P("Documentacao interativa (Swagger UI)", CELL)],
           [P("Maven 3.9+ / Docker", CELL), P("Build e empacotamento da aplicacao", CELL)],
           [P("Render.com", CELL), P("Deploy em servidor de aplicacao", CELL)]]
    s.append(tabela(tec, [170, 270]))

    # ---------- 2. DIAGRAMA DE CLASSES ----------
    s += [PageBreak(), P("2. Diagrama de classes", H1)]
    s.append(P("O codigo segue a arquitetura em camadas vista em aula: <b>controller</b> recebe a requisicao HTTP, "
               "<b>bo</b> aplica as regras de negocio, <b>dao</b> executa o SQL no Oracle e <b>exception</b> "
               "centraliza o tratamento de erros. Os diagramas abaixo refletem as classes do pacote "
               "<font face='Courier'>br.com.fiap.meubairro</font>."))
    s.append(P("2.1 Camadas e dependencias", H2))
    s.append(Diagram(500, 500, desenha_camadas))
    s.append(P("Figura 1 - Controllers, BOs, DAOs e tratamento de excecoes (setas indicam \"usa\").", CAP))
    s += [PageBreak(), P("2.2 Modelo de dominio (pacote model)", H2)]
    s.append(Diagram(500, 470, desenha_dominio))
    s.append(P("Figura 2 - Classes do modelo (records), enums e seus relacionamentos. "
               "<font face='Courier'>BairroResumo</font> é uma visão de leitura (bairro + indicadores + nota + posicao).", CAP))

    # ---------- 3. PROTOTIPOS ----------
    s += [PageBreak(), P("3. Prototipos de tela", H1)]
    s.append(P("Prototipos do front-end que consome a API. Cada tela indica os endpoints envolvidos."))
    s.append(linha_prototipos(TELAS[0:2]))
    s.append(linha_prototipos(TELAS[2:4]))
    s.append(linha_prototipos(TELAS[4:6]))
    s.append(P("Figura 3 - Prototipos das telas do front-end.", CAP))

    # ---------- 4. ENDPOINTS ----------
    s += [PageBreak(), P("4. Tabela de endpoints", H1)]
    s.append(P("Todas as rotas retornam JSON. Erros seguem o formato descrito abaixo da tabela. A documentacao "
               "interativa fica em <font face='Courier'>/swagger-ui.html</font>."))
    dados = [[hcell("Metodo"), hcell("Rota"), hcell("Descricao"), hcell("Sucesso"), hcell("Erros")]]
    for m, r, d, ok, er in ENDPOINTS:
        dados.append([Paragraph('<font color="%s"><b>%s</b></font>' % (COR_METODO[m], m), CELL),
                      Paragraph('<font face="Courier" size="7">%s</font>' % r.replace("&", "&amp;"), CELL),
                      P(d, CELL), P(ok, CELL), P(er, CELL)])
    s.append(tabela(dados, [46, 148, 156, 46, 58]))
    s.append(Spacer(1, 8))
    s.append(P("Codigos de erro: <b>400</b> dados invalidos, <b>404</b> recurso inexistente, <b>409</b> conflito "
               "(duplicidade), <b>422</b> regra de negocio violada, <b>503</b> falha de banco, <b>500</b> erro interno.", SMALL))
    s.append(P("Exemplos de requisição e resposta", H2))
    EXEMPLOS = """// POST /reportes
{ "usuarioId": 2, "bairroId": 2, "categoria": "BURACO",
  "descricao": "Buraco grande na calçada em frente ao nº 100",
  "latitude": -23.5871, "longitude": -46.6384 }

// PUT /reportes/7/status
{ "status": "EM_ANDAMENTO", "adminId": 1 }

// Resposta de erro (422)
{ "timestamp": "...", "status": 422, "erro": "Unprocessable Entity",
  "mensagem": "Apenas usuários ADMIN podem alterar o status de um reporte",
  "caminho": "/reportes/7/status", "detalhes": [] }"""
    s.append(Preformatted(EXEMPLOS, CODE))

    # ---------- 5. DER ----------
    s += [PageBreak(), P("5. Diagrama Entidade-Relacionamento (DER)", H1)]
    s.append(P("Tabelas criadas no Oracle pelo script <font face='Courier'>schema.sql</font> (executado na primeira "
               "inicializacao da aplicacao)."))
    s.append(Diagram(500, 450, desenha_der))
    s.append(P("Figura 4 - DER com as cinco tabelas do projeto.", CAP))
    rest = [[hcell("Tabela"), hcell("Restricoes principais")],
            [P("tb_mb_bairro", CELL), P("UK (nome, cidade); populacao >= 0", CELL)],
            [P("tb_mb_usuario", CELL), P("UK email; perfil IN (MORADOR, ADMIN); FK id_bairro (opcional)", CELL)],
            [P("tb_mb_reporte", CELL), P("categoria IN (BURACO, ILUMINACAO, LIXO, ALAGAMENTO, OUTRO); status IN "
                                         "(ABERTO, EM_ANDAMENTO, RESOLVIDO) com padrao ABERTO; indices por bairro e status", CELL)],
            [P("tb_mb_voto", CELL), P("UK (id_reporte, id_usuario): um voto por usuario em cada reporte", CELL)],
            [P("tb_mb_indicador_bairro", CELL), P("UK id_bairro (1 conjunto por bairro); indicadores entre 0 e 10", CELL)]]
    s.append(tabela(rest, [120, 320]))

    # ---------- 6. EXECUCAO ----------
    s += [PageBreak(), P("6. Instrucoes para executar o projeto", H1)]
    s.append(P("6.1 Ferramentas e versoes", H2))
    s += bullets(["<b>Ferramentas:</b> IntelliJ IDEA (ou VS Code), Git, Postman/Insomnia (opcional), Docker (opcional).",
                  "<b>Versoes:</b> Java JDK 21, Maven 3.9+, banco Oracle (servidor da FIAP).",
                  "<b>Links:</b> GitHub " + link(GITHUB) + " - Deploy: " + deploy_txt()])
    s.append(P("6.2 Execucao local (passo a passo)", H2))
    passos = [
        "Clone o repositorio e abra a pasta no IntelliJ: <font face='Courier'>git clone " + GITHUB + "</font>",
        "Defina as variaveis de ambiente (nunca commite a senha): <font face='Courier'>DB_URL</font> "
        "(ex.: jdbc:oracle:thin:@oracle.fiap.com.br:1521:ORCL), <font face='Courier'>DB_USER</font> (seu RM) e "
        "<font face='Courier'>DB_PASSWORD</font>.",
        "Execute <font face='Courier'>mvn spring-boot:run</font> ou rode a classe "
        "<font face='Courier'>MeuBairroApplication</font> pelo IntelliJ.",
        "Na primeira execucao a aplicacao cria as tabelas (<font face='Courier'>schema.sql</font>) e carrega dados de "
        "exemplo (<font face='Courier'>data.sql</font>) se o banco estiver vazio. Para desligar: "
        "<font face='Courier'>DB_INIT=false</font>.",
        "Acesse <font face='Courier'>http://localhost:8080/swagger-ui.html</font> e teste os endpoints.",
    ]
    for i, p in enumerate(passos, 1):
        s.append(Paragraph(acc(p), BUL, bulletText="%d." % i))
    s.append(P("6.3 Execucao com Docker", H2))
    s.append(Preformatted("docker build -t meu-bairro-api .\ndocker run -p 8080:8080 -e DB_URL=... -e DB_USER=... "
                          "-e DB_PASSWORD=... meu-bairro-api", CODE))
    s.append(P("6.4 Deploy no Render", H2))
    if not DEPLOY:
        s.append(P("<b>Situacao do deploy:</b> " + MOTIVO_SEM_DEPLOY + ". A aplicacao foi validada localmente contra um "
                   "Oracle (todos os endpoints testados) e o procedimento abaixo, junto com o Dockerfile do projeto, "
                   "esta pronto para ser executado assim que o banco estiver disponivel.", BODY))
    for i, p in enumerate([
        "Suba o codigo para o GitHub.",
        "No Render: <b>New > Web Service</b>, conecte o repositorio e escolha o runtime <b>Docker</b>.",
        "Em <i>Environment</i>, cadastre <font face='Courier'>DB_URL</font>, <font face='Courier'>DB_USER</font> e "
        "<font face='Courier'>DB_PASSWORD</font> (o Render fornece <font face='Courier'>PORT</font> sozinho).",
        "Execute o deploy e acesse <font face='Courier'>/swagger-ui.html</font> na URL publica" + (": " + link(DEPLOY) if DEPLOY else " gerada pelo Render."),
    ], 1):
        s.append(Paragraph(acc(p), BUL, bulletText="%d." % i))
    s.append(P("O Oracle da FIAP precisa estar acessivel pela internet a partir do Render.", SMALL))
    s.append(P("Se o Oracle da FIAP nao estiver acessivel pela internet, e possivel usar um Oracle Autonomous Database "
               "(Oracle Cloud Free) com conexao TLS sem wallet: basta informar a URL "
               "<font face='Courier'>jdbc:oracle:thin:@(description=(address=(protocol=tcps)(port=1521)(host=HOST))"
               "(connect_data=(service_name=SERVICO))(security=(ssl_server_dn_match=yes)))</font> em "
               "<font face='Courier'>DB_URL</font>, sem alterar o codigo.", SMALL))
    s.append(P("6.5 Informacoes adicionais", H2))
    s += bullets(["O servidor sobe na porta definida por <font face='Courier'>PORT</font> (padrao 8080).",
                  "CORS liberado para consumo por um front-end separado (<font face='Courier'>CorsConfig</font>).",
                  "Dados de exemplo: bairros Pinheiros, Vila Mariana, Tatuape e Mooca; usuario ADMIN "
                  "<font face='Courier'>admin@meubairro.com</font>."])
    return s


if __name__ == "__main__":
    Doc(SAIDA).multiBuild(monta())
    print("PDF gerado em", SAIDA)
