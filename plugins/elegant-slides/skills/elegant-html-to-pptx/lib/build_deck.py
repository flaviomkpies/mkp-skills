#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Reconstrói a Proposta RI Pack (v3) como PPTX nativo editável no tema Elegant P&B."""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
import pptxlib as L
from pptxlib import (new_prs, add_slide, add_text, add_line, add_rect, add_img, run,
                     E, P, C, INK, G1, G2, HAIR, HAIRS, PAPER,
                     SERIF, SERIF_LIGHT, SANS, SANS_SB)
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR

G = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "glyphs"))
PHOTO = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "palco_tight.jpg"))

MARGIN_X = 130
CONTENT_R = 1790          # right edge
NAV = ["Quem conduz", "Contexto", "Crenças", "Ofertas", "Próximos passos"]
NAV_X = [151, 354, 505, 636, 765]

# ---------- chrome comum ----------
def margin_rule(s):
    add_line(s, 104, 84, 104, 996, color=HAIR, weight_px=1)

def nav(s, active):
    for i, lab in enumerate(NAV):
        b = (i == active)
        add_text(s, NAV_X[i], 40, 260, 30,
                 [[run(lab, font=SANS, size=21, color=INK if b else G2, bold=b)]])

def pager(s, num):
    add_text(s, CONTENT_R-260, 40, 260, 30,
             [[run(f"‹   {num:02d} / 10   ›", font=SANS, size=21, color=G2)]],
             align=PP_ALIGN.RIGHT)

def eyebrow(s, text, y=118):
    add_text(s, MARGIN_X, y, 1400, 26,
             [[run(text, font=SANS, size=17, color=G2, spacing_em=0.14, upper=True)]])

def title(s, text, y=150, size=84, w=1500, lines=1, accent=True):
    h = int(size*1.12*lines)
    if accent:
        add_line(s, MARGIN_X-16, y+6, MARGIN_X-16, y+h-4, color=INK, weight_px=3)
    add_text(s, MARGIN_X, y, w, h,
             [[run(text, font=SERIF_LIGHT, size=size, color=INK)]], line_px=int(size*1.02))
    return y+h

def subtitle(s, text, y, size=30, w=1560):
    add_text(s, MARGIN_X, y, w, int(size*2.4),
             [[run(text, font=SERIF, size=size, color=G1, italic=True)]], line_px=int(size*1.32))

def footer(s, text):
    add_text(s, MARGIN_X, 1006, 1560, 32,
             [[run(text, font=SANS, size=19, color=G2)]])

def glyph(s, name, x=CONTENT_R-40, y=930):
    p = f"{G}/{name}.png"
    if os.path.exists(p):
        add_img(s, p, x, y, 40, 40)

def new_content(prs, active, num):
    s = add_slide(prs)
    margin_rule(s); nav(s, active); pager(s, num)
    return s

# ---------- helpers de bloco ----------
def label_guide_body(s, x, y, w, lab, guide, body, lab_size=27, gap=8):
    add_text(s, x, y, w, 40, [[run(lab, font=SERIF, size=lab_size, color=INK)]])
    yy = y + int(lab_size*1.25)
    if guide:
        add_text(s, x, yy, w, 32, [[run(guide, font=SERIF, size=21, color=G2, italic=True)]])
        yy += 34
    add_text(s, x, yy, w, 260, [[run(body, font=SANS, size=21, color=G1)]], line_px=30)


def build():
    prs = new_prs()
    L._set_bg(prs.slide_masters[0], PAPER)

    # ===== 01 CAPA =====
    s = add_slide(prs)
    add_img(s, f"{G}/cover_network.png", 960-125, 92, 250, 158)
    add_text(s, 130, 322, 1660, 46, [[run("Proposta comercial", font=SERIF, size=30, color=G1)]], align=PP_ALIGN.CENTER)
    add_text(s, 130, 400, 1660, 180, [[run("RI Pack - Adoção de IA", font=SERIF_LIGHT, size=118, color=INK)]], align=PP_ALIGN.CENTER, anchor=MSO_ANCHOR.MIDDLE)
    add_text(s, 300, 600, 1320, 100, [[run("início da jornada de geração de valor com IA a partir da capacitação do time e priorização de oportunidades futuras", font=SERIF_LIGHT, size=30, color=G1, italic=True)]], align=PP_ALIGN.CENTER, line_px=40)
    add_img(s, f"{G}/serrated_baseline.png", 130, 905, 1660, 24)
    add_text(s, 130, 940, 1000, 40, [[run("RI Pack | Flavio Mac Knight Pies", font=SANS, size=21, color=G2)]])
    add_text(s, 790, 940, 1000, 40, [[run("julho 2026", font=SANS, size=21, color=G2)]], align=PP_ALIGN.RIGHT)

    # ===== 02 QUEM CONDUZ =====
    s = add_slide(prs)
    margin_rule(s); nav(s, 0)
    # foto metade direita full-bleed
    add_img(s, PHOTO, 985, 0, 935, 1080)
    eyebrow(s, "quem conduz", y=96)
    add_line(s, MARGIN_X-16, 150, MARGIN_X-16, 224, color=INK, weight_px=3)
    add_text(s, MARGIN_X, 138, 760, 100, [[run("Flavio Mac Knight Pies", font=SERIF_LIGHT, size=66, color=INK)]])
    add_text(s, MARGIN_X, 300, 760, 90, [[run("Consultor que implementa: a IA entra na operação, não em relatório.", font=SANS, size=27, color=INK, bold=True)]], line_px=36)
    p1="Com mais de 10 anos de experiência em consultoria estratégica, Flavio se dedicou a resolver problemas complexos com abordagens pragmáticas e analíticas, trazendo tecnologia para auxiliar executivos e líderes a tomarem decisões e destravarem valor. Engenheiro de produção pela UFRJ e estudos na França e em Wharton, Flavio liderou projetos em grandes empresas como Mercedes, Ipiranga, Klabin e em empresas de pequeno e médio porte, apoiando famílias empresárias em seus desafios de gestão."
    p2="Após mais de dez anos em consultoria estratégica, Flavio hoje atua como conselheiro na consultoria que fundou, a Mondoré, e auxilia empresas de diferentes setores a adotar IA na prática: capacitação dos executivos em workshops e monitorias, priorização de iniciativas de geração de valor e desenvolvimento de soluções tecnológicas que continuam a gerar valor depois que a consultoria sai."
    p3="Mestrando na FGV, pesquisa a adoção de IA generativa em serviços profissionais. Escreve a Newsletter do Flavio: IA na prática e leva o tema a palcos de eventos e salas de aula de MBA."
    add_text(s, MARGIN_X, 410, 760, 560,
             [[run(p1, font=SERIF, size=21, color=G1)],
              [run(p2, font=SERIF, size=21, color=G1)],
              [run(p3, font=SERIF, size=21, color=G1)]],
             line_px=30, para_gap_px=14)

    # ===== 03 CONTEXTO (matriz 2x2) =====
    s = new_content(prs, 1, 3)
    eyebrow(s, "contexto RI Pack")
    add_line(s, MARGIN_X-16, 156, MARGIN_X-16, 250, color=INK, weight_px=3)
    add_text(s, MARGIN_X, 150, 1520, 130, [[run("A RI Pack já compreendeu que IA é uma jornada e pode ajudar a empresa a gerar valor: para tal, ela precisa de apoio para começar a jornada", font=SERIF_LIGHT, size=40, color=INK)]], line_px=48)
    quad = [
        ("Operação", "embalagens de madeira sob medida para multinacionais em operação verticalizada",
         "equipe administrativa com aproximadamente 40 pessoas, porém sem equipe de TI: melhorias de gestão hoje dependem da liderança"),
        ("Sistemas", "operações acontecem no ERP, porém geração de inteligência é um desafio",
         "ERP cobre operações do dia a dia, entretanto coleta de dados apenas gera inteligência a partir de trabalhos manuais e planilhas. Um sintoma é o fechamento financeiro, que sai normalmente com dados de mais de um mês de atraso"),
        ("Potencial", "primeiras hipóteses de áreas com geração de valor pela IA",
         "atividades primárias: PCP e S&OP (previsão de vendas), entretanto foco inicial parece ser nas atividades administrativas e gerenciais (finanças, relatórios e rituais de gestão, compras, etc.)"),
        ("Ponto de partida", "o que já existe",
         "uso incipiente, início de utilização e exploração por cinco pessoas em nova contratação do Claude Teams. Compreensão é de que o time precisa de capacitação do “zero até o avançado”"),
    ]
    cw, gap = 800, 60
    xs = [MARGIN_X, MARGIN_X+cw+gap]
    ys = [430, 720]
    for i, (lab, guide, body) in enumerate(quad):
        x = xs[i % 2]; y = ys[i//2]
        add_line(s, x, y-14, x+cw, y-14, color=HAIRS, weight_px=1)
        add_text(s, x, y, 360, 40, [[run(lab, font=SERIF, size=26, color=INK)]])
        add_text(s, x+300, y+4, cw-300, 40, [[run(guide, font=SERIF, size=19, color=G2, italic=True)]], line_px=25)
        add_text(s, x, y+ (40 if len(guide)<45 else 66), cw, 180, [[run(body, font=SANS, size=20, color=G1)]], line_px=28)
    footer(s, "Fonte: conversa Flavio · Thiago Ribeiro, 21/07/2026")
    glyph(s, "glyph_s03")

    # ===== 04 CRENÇAS =====
    s = new_content(prs, 2, 4)
    eyebrow(s, "crenças")
    add_line(s, MARGIN_X-16, 152, MARGIN_X-16, 214, color=INK, weight_px=3)
    add_text(s, MARGIN_X, 146, 1400, 80, [[run("O que eu acredito sobre adoção de IA", font=SERIF_LIGHT, size=52, color=INK)]])
    bel = [
        ("Prática, não teoria", "adoção não acontece em palestra: acontece com o problema real da empresa na tela. É a diferença entre conversar sobre o trabalho e ter a IA fazendo o trabalho com você"),
        ("Contato próximo, presencial", "a mudança de hábito acontece lado a lado com quem faz o trabalho, no ritmo de quem faz o trabalho: por isso workshops presenciais, com monitoria para cada participante"),
        ("O erro tem cara de acerto", "a IA funciona muito bem em algumas tarefas e piora o resultado em outras, e o contorno entre elas não segue a intuição: quem mapeia isso, atividade por atividade, captura o ganho sem herdar o erro"),
        ("Autonomia da casa", "o objetivo é a equipe da RI Pack dominar as ferramentas e tornar explícita a própria forma de trabalhar. Esse ativo ninguém desinstala"),
    ]
    y = 300; rh = 168
    for lab, body in bel:
        add_line(s, MARGIN_X, y-16, CONTENT_R, y-16, color=HAIRS, weight_px=1)
        add_text(s, MARGIN_X, y, 500, 80, [[run(lab, font=SERIF, size=30, color=INK)]], line_px=36)
        add_text(s, MARGIN_X+560, y+2, 1100, 130, [[run(body, font=SANS, size=21, color=G1)]], line_px=30)
        y += rh
    footer(s, "Crenças")
    glyph(s, "glyph_s04")

    # ===== 05 PALCOS E PUBLICAÇÕES =====
    s = new_content(prs, 2, 5)
    eyebrow(s, "palcos e publicações")
    add_line(s, MARGIN_X-16, 152, MARGIN_X-16, 214, color=INK, weight_px=3)
    add_text(s, MARGIN_X, 146, 560, 200, [[run("A prática também vira aula, palco e artigo", font=SERIF_LIGHT, size=46, color=INK)]], line_px=54)
    add_text(s, MARGIN_X, 340, 540, 200, [[run("no segundo trimestre de 2026, três empresas passaram pela capacitação em IA e vários executivos pela mentoria individual", font=SERIF, size=23, color=G1, italic=True)]], line_px=32)
    # coluna direita 2/3
    RX = 760
    add_text(s, RX, 150, 900, 26, [[run("principais eventos e palestras", font=SANS, size=17, color=G2, spacing_em=0.12, upper=True)]])
    ev = [
        ("Herdeiros do Varejo · C6 Bank", "palestra sobre adoção de IA para líderes e famílias empresárias do varejo"),
        ("MBA de Comunicação · PUC Minas", "aulas práticas de IA e multiagentes para executivos de marketing"),
        ("ClawCon São Paulo", "palestra sobre um time de agentes de IA no dia a dia de uma consultoria"),
        ("AI First Cast", "episódio sobre o impacto da IA no mundo das consultorias"),
    ]
    ey = 196; ecw = 470
    for i, (lab, body) in enumerate(ev):
        x = RX + (i % 2)*(ecw+60); yy = ey + (i//2)*130
        add_line(s, x, yy-10, x+ecw, yy-10, color=HAIR, weight_px=1)
        add_text(s, x, yy, ecw, 40, [[run(lab, font=SERIF, size=23, color=INK)]])
        add_text(s, x, yy+34, ecw, 80, [[run(body, font=SANS, size=19, color=G1)]], line_px=26)
    add_text(s, RX, 470, 900, 26, [[run("publicações", font=SANS, size=17, color=G2, spacing_em=0.12, upper=True)]])
    pub = [
        ("Nexo Jornal", "“A fronteira irregular da inteligência artificial”, na série As escolhas em relação à inteligência artificial", "nexojornal.com.br/debate/2026/07/13/inteligencia-artificial-desafios-tecnologia"),
        ("Newsletter do Flavio: IA na prática", "diário de quem implementa IA em empresas, toda semana", "flaviomacknightpies.substack.com"),
    ]
    for i, (lab, body, link) in enumerate(pub):
        x = RX + i*(ecw+60); yy = 516
        add_line(s, x, yy-10, x+ecw, yy-10, color=HAIR, weight_px=1)
        add_text(s, x, yy, ecw, 40, [[run(lab, font=SERIF, size=23, color=INK)]])
        add_text(s, x, yy+34, ecw, 90, [[run(body, font=SANS, size=19, color=G1)]], line_px=26)
        add_text(s, x, yy+120, ecw, 30, [[run(link, font=SANS, size=16, color=G2)]])
    footer(s, "Palcos e publicações")
    glyph(s, "glyph_s4b")

    # ===== 06 OFERTAS =====
    s = new_content(prs, 3, 6)
    eyebrow(s, "ofertas · investimento")
    add_line(s, MARGIN_X-16, 152, MARGIN_X-16, 214, color=INK, weight_px=3)
    add_text(s, MARGIN_X, 146, 1500, 80, [[run("Duas formas de começar, e a jornada que segue depois", font=SERIF_LIGHT, size=50, color=INK)]])
    cols_y = 292; col_w = 505; col_h = 560; gap = 22
    cx = [MARGIN_X, MARGIN_X+col_w+gap, MARGIN_X+2*(col_w+gap)]
    def offer_col(x, tag, name, price, items, recommended=False, faded=False):
        lab_c = G2 if faded else INK
        body_c = HAIRS if faded else G1
        if recommended:
            add_rect(s, x, cols_y, col_w, col_h, fill=None, line=INK, line_px=3)
            add_rect(s, x+col_w-190, cols_y, 190, 40, fill=INK)
            add_text(s, x+col_w-190, cols_y+8, 190, 26, [[run("RECOMENDADO", font=SANS, size=15, color=PAPER, spacing_em=0.1, upper=True)]], align=PP_ALIGN.CENTER)
        else:
            add_rect(s, x, cols_y, col_w, col_h, fill=None, line=HAIR, line_px=1)
        px = x+26
        add_text(s, px, cols_y+22, col_w-52, 24, [[run(tag, font=SANS, size=17, color=(HAIRS if faded else G2), spacing_em=0.12, upper=True)]])
        add_text(s, px, cols_y+50, col_w-52, 66, [[run(name, font=SANS, size=25, color=lab_c, bold=True)]], line_px=32)
        add_text(s, px, cols_y+122, col_w-52, 60, [[run(price, font=SERIF_LIGHT, size=(44 if not faded else 27), color=lab_c, italic=faded)]])
        add_line(s, px, cols_y+200, x+col_w-26, cols_y+200, color=HAIR, weight_px=1)
        # itens num único bloco que flui (evita erro de matemática por-item)
        paras = [[run(it, font=SANS, size=18, color=body_c)] for it in items]
        add_text(s, px, cols_y+214, col_w-52, col_h-232, paras, line_px=25, para_gap_px=13)
    offer_col(cx[0], "opção 1", "Capacitação", "R$ 30 mil", [
        "3 workshops presenciais de 3h30, turma de 10 a 15 pessoas",
        "3 monitorias de 1h (online, remoto) após cada workshop para resolver dúvidas e esclarecer conceitos",
        "plugins RI Pack: skills Office (Excel, PowerPoint, dashboards e Word/PDF) na identidade visual e voz da empresa e regras de evolução dos agentes desenvolvidos, em metodologia própria"])
    offer_col(cx[1], "opção 2", "Capacitação e Priorização de iniciativas", "R$ 40 mil", [
        "tudo da Capacitação",
        "+ roadmap de IA para 3, 6 e 12 meses, priorizando iniciativas por valor e esforço",
        "+ detalhamento de 3 pilotos no curto prazo, especificando escopo e cronograma, inclusive prompts iniciais para desenvolvimento da solução pelo time da RI Pack"], recommended=True)
    offer_col(cx[2], "adiante", "Apoio mão na massa na jornada de IA da RI Pack", "pra conversar depois", [
        "acompanhamento contínuo da adoção depois dos workshops",
        "evolução dos agentes e novas automações, no ritmo da empresa"], faded=True)
    # adicionais
    ay = 872
    add_line(s, MARGIN_X, ay-14, CONTENT_R, ay-14, color=HAIRS, weight_px=1)
    add_text(s, MARGIN_X, ay, 1400, 24, [[run("adicionais · independentes da opção", font=SANS, size=17, color=G2, spacing_em=0.12, upper=True)]])
    adds = [
        [run("Monitoria com líderes", font=SANS, size=19, color=INK, bold=True), run(" · encontros online de 1h com conteúdo personalizado para o executivo (agentes, skills, regras, discussão de aplicações) · R$ 1.000 por encontro", font=SANS, size=19, color=G1)],
        [run("Monitorias extras", font=SANS, size=19, color=INK, bold=True), run(" · R$ 1.000 por encontro", font=SANS, size=19, color=G1)],
        [run("Desenvolvimento de soluções agênticas", font=SANS, size=19, color=INK, bold=True), run(" · preço a definir", font=SANS, size=19, color=G1)],
    ]
    axs = [MARGIN_X, MARGIN_X+560, MARGIN_X+1080]
    aws = [520, 500, 560]
    for i, para in enumerate(adds):
        add_text(s, axs[i], ay+34, aws[i], 90, [para], line_px=27)
    footer(s, "Condições: pagamento em até 2 parcelas, 10% na assinatura do contrato · valores válidos por 15 dias · despesas de viagens, hospedagem e alimentação não inclusas")

    # ===== 07 CAPACITAÇÃO (linha do tempo) =====
    s = new_content(prs, 3, 7)
    eyebrow(s, "capacitação · linha do tempo")
    add_line(s, MARGIN_X-16, 152, MARGIN_X-16, 250, color=INK, weight_px=3)
    add_text(s, MARGIN_X, 146, 1450, 130, [[run("Três workshops com os problemas da RI Pack na tela", font=SERIF_LIGHT, size=52, color=INK)]], line_px=60)
    add_text(s, MARGIN_X, 300, 1500, 90, [[run("presenciais, 3h30 cada, turma de 10 a 15 pessoas: conceitos, funcionalidades, aplicações à realidade da RI Pack e case prático em cada encontro", font=SERIF, size=26, color=G1, italic=True)]], line_px=36)
    steps = [
        ("1", "Claude Chat", "conceitos de IA generativa e domínio do chat: prompts, análises e os primeiros ganhos de tempo de cada participante"),
        ("2", "Claude Cowork", "a IA no computador de cada um: planilhas, documentos e apresentações da empresa feitos com o Cowork"),
        ("3", "Agentes no Claude Cowork", "agentes que executam rotinas de trabalho: da tarefa individual ao processo da operação"),
    ]
    ty = 620; sx = [MARGIN_X, MARGIN_X+540, MARGIN_X+1080]; scw = 380
    for i, (nrec, nm, desc) in enumerate(steps):
        x = sx[i]
        add_text(s, x, ty, 90, 90, [[run(nrec, font=SERIF_LIGHT, size=84, color=INK)]])
        add_line(s, x+4, ty+96, x+4, ty+128, color=INK, weight_px=2)
        add_text(s, x, ty+140, scw, 70, [[run(nm, font=SANS, size=25, color=INK, bold=True)]], line_px=32)
        nlines = 1 if len(nm) <= 15 else 2
        add_text(s, x, ty+140 + nlines*40 + 8, scw, 160, [[run(desc, font=SANS, size=21, color=G1)]], line_px=30)
        # conector pontilhado + label monitoria
        conx = x+430
        add_line(s, conx, ty+60, conx+80, ty+60, color=HAIRS, weight_px=1, dash='sysDot')
        add_text(s, conx-6, ty+72, 110, 60, [[run("monitoria de 1h, online", font=SERIF, size=17, color=G2, italic=True)]], line_px=23, align=PP_ALIGN.CENTER)
    footer(s, "Temas ajustados com a RI Pack antes de cada encontro")
    glyph(s, "glyph_s06")

    # ===== 08 ROADMAP =====
    s = new_content(prs, 3, 8)
    eyebrow(s, "opção 2 · o que se soma à capacitação")
    add_line(s, MARGIN_X-16, 152, MARGIN_X-16, 250, color=INK, weight_px=3)
    add_text(s, MARGIN_X, 146, 560, 240, [[run("Um roadmap para decidir onde a IA gera resultado primeiro", font=SERIF_LIGHT, size=44, color=INK)]], line_px=52)
    add_text(s, MARGIN_X, 400, 540, 200, [[run("metodologia própria, aplicada em programa de capacitação e roadmap de IA em multinacional de bens de consumo", font=SERIF, size=23, color=G1, italic=True)]], line_px=32)
    RX = 760
    rows = [
        ("Mapeamento de processos", "onde o tempo é gasto", "levantamento dos processos do administrativo (financeiro, compras, PCP e S&OP) e das horas que cada um consome"),
        ("Ideação e impacto", "o filtro do que vem primeiro", "oportunidades de IA levantadas processo a processo e avaliadas por valor e esforço, numa matriz de priorização decidida com a liderança"),
        ("Roadmap em ondas", "3, 6 e 12 meses", "iniciativas organizadas em ondas, cada uma com responsável, esforço e resultado esperado"),
        ("3 pilotos detalhados", "prontos pra sair do papel", "escopo, cronograma e prompts iniciais para o time da RI Pack desenvolver as primeiras soluções"),
    ]
    y = 176; rh = 190
    for lab, guide, body in rows:
        add_line(s, RX, y-12, CONTENT_R, y-12, color=HAIRS, weight_px=1)
        add_text(s, RX, y, 900, 38, [[run(lab, font=SERIF, size=27, color=INK)]])
        add_text(s, RX, y+40, 900, 30, [[run(guide, font=SERIF, size=20, color=G2, italic=True)]], line_px=27)
        add_text(s, RX, y+78, 900, 120, [[run(body, font=SANS, size=21, color=G1)]], line_px=30)
        y += rh
    footer(s, "Incluído na opção 2 · Capacitação e Priorização de iniciativas")
    glyph(s, "glyph_s07")

    # ===== 09 PLUGINS =====
    s = new_content(prs, 3, 9)
    eyebrow(s, "plugins e skills")
    add_line(s, MARGIN_X-16, 152, MARGIN_X-16, 260, color=INK, weight_px=3)
    add_text(s, MARGIN_X, 146, 560, 260, [[run("Projeto inclui o desenvolvimento de plugin para RI Pack no Claude Cowork", font=SERIF_LIGHT, size=40, color=INK)]], line_px=48)
    add_text(s, MARGIN_X, 430, 540, 220, [[run("skills de uso mais frequente com a identidade visual da RI Pack, além da capacidade de os agentes continuarem a melhorar conforme o uso", font=SERIF, size=23, color=G1, italic=True)]], line_px=32)
    RX = 760
    rows = [
        ("Plugins de Office", "na identidade visual e voz da empresa", "apresentações PowerPoint, planilhas Excel, dashboards e documentos gerados no padrão visual e de escrita da RI Pack, prontos pra uso"),
        ("Skills de agentes", "pra criar melhoria contínua mesmo depois dos workshops", "como criar e evoluir agentes no dia a dia da operação, sem depender de equipe de TI"),
        ("Adiante na jornada", "não incluso nesta proposta comercial", "automações mais complexas e com retorno financeiro, como fechamento mensal financeiro e alertas de PCP e S&OP: devem ser avaliadas em apoios futuros"),
    ]
    y = 200; rh = 250
    for lab, guide, body in rows:
        add_line(s, RX, y-12, CONTENT_R, y-12, color=HAIRS, weight_px=1)
        add_text(s, RX, y, 900, 40, [[run(lab, font=SERIF, size=27, color=INK)]])
        add_text(s, RX, y+40, 900, 32, [[run(guide, font=SERIF, size=20, color=G2, italic=True)]], line_px=27)
        add_text(s, RX, y+78, 900, 130, [[run(body, font=SANS, size=21, color=G1)]], line_px=30)
        y += rh
    glyph(s, "glyph_s09")

    # ===== 10 PRÓXIMOS PASSOS =====
    s = new_content(prs, 4, 10)
    add_line(s, MARGIN_X-16, 150, MARGIN_X-16, 224, color=INK, weight_px=3)
    add_text(s, MARGIN_X, 140, 900, 90, [[run("Próximos passos", font=SERIF_LIGHT, size=66, color=INK)]])
    steps = [
        ("1 · Conversa com o fundador", "apresentação da proposta na quinta-feira, 23/07, com Thiago e o fundador da RI Pack"),
        ("2 · Escolha da opção", "escolha entre as opções 1 e 2 e ajuste fino dos temas dos workshops com o Thiago"),
        ("3 · Assinatura do contrato", "formalização da opção escolhida, com 10% na assinatura"),
        ("4 · Agenda", "datas dos três workshops, no calendário da equipe"),
    ]
    y = 320; rh = 148
    for lab, body in steps:
        add_line(s, MARGIN_X, y-16, 1180, y-16, color=HAIRS, weight_px=1)
        add_text(s, MARGIN_X, y, 460, 60, [[run(lab, font=SERIF, size=27, color=INK)]])
        add_text(s, MARGIN_X+500, y+2, 680, 100, [[run(body, font=SANS, size=21, color=G1)]], line_px=30)
        y += rh
    # contato à direita
    add_line(s, 1320, 320, 1320, 780, color=HAIR, weight_px=1)
    add_text(s, 1380, 320, 420, 40, [[run("contato", font=SANS, size=17, color=G2, spacing_em=0.12, upper=True)]])
    add_text(s, 1380, 360, 420, 50, [[run("Flavio Mac Knight Pies", font=SERIF_LIGHT, size=30, color=INK)]])
    add_text(s, 1380, 420, 420, 200, [[run("flaviomkpies@gmail.com", font=SANS, size=19, color=G1)],
                                       [run("linkedin.com/in/flavio-mac-knight-pies", font=SANS, size=19, color=G1)],
                                       [run("flaviomacknightpies.substack.com", font=SANS, size=19, color=G1)]], line_px=34)
    footer(s, "Proposta válida por 30 dias")
    glyph(s, "glyph_s09", x=CONTENT_R-40, y=930)

    out = os.path.join(os.path.dirname(__file__), "RIPack_deck.pptx")
    prs.save(out)
    print("saved", out, "slides:", len(prs.slides._sldIdLst))
    return out

if __name__ == "__main__":
    build()
