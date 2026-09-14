# Humanizer patterns — referência canônica

24 padrões de "AI writing" para detectar e remover. Compartilhado entre `modes/humanize.md`, `modes/newsletter.md` (etapa polish), `modes/post.md` e `modes/longform.md`.

Baseado na página "Signs of AI writing" do WikiProject AI Cleanup. Corpo do documento em inglês (terminologia canônica). Para textos PT-BR, ver bloco "Patterns extras PT-BR" abaixo, que adapta ao contexto brasileiro.

## Patterns extras PT-BR

**Anglicismos desnecessários** (frequentes em texto AI traduzido):
- AI → IA (sempre, exceto quando "AI" é nome de produto: "Anthropic AI")
- start-up → startup (já é português corrente)
- "fazer sense" → fazer sentido / soar bem
- "compelling" → forte / convincente
- "actionable" → prático / aplicável
- "leverage" como verbo → usar / aproveitar
- "framework" — manter quando técnico, mas evitar "framework conceitual" (redundante)

**Construções traduzidas literais** (sinal de AI traduzindo do EN):
- "É importante notar que..." → cortar (em EN: *"It's important to note that..."*)
- "Vale ressaltar..." → afirmar diretamente
- "Em sua essência..." → cortar
- "Por fim, mas não menos importante..." → cortar
- "No final do dia..." → cortar (em EN: *"at the end of the day"*)
- "De fato..." quando aparece sem ser ênfase real → cortar

**Vocabulário acadêmico-empresarial inflado** (PT-BR):
- "potencializar" → aumentar / amplificar
- "alavancar" → usar / impulsionar (caso específico)
- "fomentar" → criar / estimular
- "desbravar" → começar / explorar
- "empoderar" → dar autonomia / capacitar
- "robustez" → solidez / consistência
- "holístico" → completo / integrado
- "ressignificar" → redefinir / repensar

**Anti-atribuição AI** (regra inviolável do DNA central):
Toda expressão sugerida pelo agente entra marcada `[SUGESTÃO AI]`. Se detectar expressão sem origem rastreável no brain dump / entrevista / fontes verificadas, marcar imediatamente. Não correr na prosa como se fosse voz do autor.

---

## PERSONALITY AND SOUL

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop. Good writing has a human behind it.

### Signs of soulless writing (even if technically "clean"):
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

### How to add voice:

**Have opinions.** Don't just report facts - react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.

**Vary your rhythm.** Short punchy sentences. Then longer ones that take their time getting where they're going. Mix it up.

**Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats "This is impressive."

**Use "I" when it fits.** First person isn't unprofessional - it's honest. "I keep coming back to..." or "Here's what gets me..." signals a real person thinking.

**Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and half-formed thoughts are human.

**Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

### Before (clean but soulless):
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

### After (has a pulse):
> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept. Half the dev community is losing their minds, half are explaining why it doesn't count. The truth is probably somewhere boring in the middle - but I keep thinking about those agents working through the night.

---

## CONTENT PATTERNS

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

---

### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:**
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

---

### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth.

**Before:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

---

### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.

**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

---

### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.

**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

---

### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After:**
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

---

## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI Vocabulary" Words

**High-frequency AI words:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Problem:** These words appear far more frequently in post-2023 text. They often co-occur.

**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

---

### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for simple copulas.

**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

---

### 9. Negative Parallelisms

**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused.

**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.

---

### 10. Rule of Three Overuse

**Problem:** LLMs force ideas into groups of three to appear comprehensive.

**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.

---

### 11. Elegant Variation (Synonym Cycling)

**Problem:** AI has repetition-penalty code causing excessive synonym substitution.

**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.

---

### 12. False Ranges

**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

---

## STYLE PATTERNS

### 13. Em Dash Overuse

**Problem:** LLMs use em dashes (—) more than humans, mimicking "punchy" sales writing.

**Before:**
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

---

### 14. Overuse of Boldface

**Problem:** AI chatbots emphasize phrases in boldface mechanically.

**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

---

### 15. Inline-Header Vertical Lists

**Problem:** AI outputs lists where items start with bolded headers followed by colons.

**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

---

### 16. Title Case in Headings

**Problem:** AI chatbots capitalize all main words in headings.

**Before:**
> ## Strategic Negotiations And Global Partnerships

**After:**
> ## Strategic negotiations and global partnerships

---

### 17. Emojis

**Problem:** AI chatbots often decorate headings or bullet points with emojis.

**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting

**After:**
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

---

### 18. Curly Quotation Marks

**Problem:** ChatGPT uses curly quotes (“...”) instead of straight quotes ("...").

**Before:**
> He said “the project is on track” but others disagreed.

**After:**
> He said "the project is on track" but others disagreed.

---

## COMMUNICATION PATTERNS

### 19. Collaborative Communication Artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Problem:** Text meant as chatbot correspondence gets pasted as content.

**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

---

### 20. Knowledge-Cutoff Disclaimers

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

**Problem:** AI disclaimers about incomplete information get left in text.

**Before:**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:**
> The company was founded in 1994, according to its registration documents.

---

### 21. Sycophantic/Servile Tone

**Problem:** Overly positive, people-pleasing language.

**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After:**
> The economic factors you mentioned are relevant here.

---

## FILLER AND HEDGING

### 22. Filler Phrases

**Before → After:**
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"

---

### 23. Excessive Hedging

**Problem:** Over-qualifying statements.

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**
> The policy may affect outcomes.

---

### 24. Generic Positive Conclusions

**Problem:** Vague upbeat endings.

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After:**
> The company plans to open two more locations next year.

---

## Process

1. Read the input text carefully
2. Identify all instances of the patterns above
3. Rewrite each problematic section
4. Ensure the revised text:
   - Sounds natural when read aloud
   - Varies sentence structure naturally
   - Uses specific details over vague claims
   - Maintains appropriate tone for context
   - Uses simple constructions (is/are/has) where appropriate
5. Present the humanized version

## Output Format

Provide:
1. The rewritten text
2. A brief summary of changes made (optional, if helpful)

---

## Full Example

**Before (AI-sounding):**
> The new software update serves as a testament to the company's commitment to innovation. Moreover, it provides a seamless, intuitive, and powerful user experience—ensuring that users can accomplish their goals efficiently. It's not just an update, it's a revolution in how we think about productivity. Industry experts believe this will have a lasting impact on the entire sector, highlighting the company's pivotal role in the evolving technological landscape.

**After (Humanized):**
> The software update adds batch processing, keyboard shortcuts, and offline mode. Early feedback from beta testers has been positive, with most reporting faster task completion.

**Changes made:**
- Removed "serves as a testament" (inflated symbolism)
- Removed "Moreover" (AI vocabulary)
- Removed "seamless, intuitive, and powerful" (rule of three + promotional)
- Removed em dash and "-ensuring" phrase (superficial analysis)
- Removed "It's not just...it's..." (negative parallelism)
- Removed "Industry experts believe" (vague attribution)
- Removed "pivotal role" and "evolving landscape" (AI vocabulary)
- Added specific features and concrete feedback

---

## Reference

This skill is based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. The patterns documented there come from observations of thousands of instances of AI-generated text on Wikipedia.

Key insight from Wikipedia: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."


---

## Tells 2026 + calibração newsletter (adicionado 2026-06-14)

> Catálogo upstream adotado como referência: **blader/humanizer** (33 patterns) e **Aboudjem/humanizer-skill** (43 patterns). Os 24 patterns acima cobrem os tells "clássicos" (Wikipedia AI Cleanup). Abaixo, os tells que só ficaram evidentes em 2026 + os PT-BR calibrados com o autor na sessão newsletter "beco sem saída / LeCun".

### 25. Punchline staccato / cadência uniforme (tell 2026 mais durável)
**Problema:** fragmentos de 1-2 palavras usados pra drama engenheirado ("Acerta." · "Não me incomoda." · "E quanto."), e várias frases seguidas do mesmo comprimento/ritmo.
**Teste:** leia 3 frases em sequência — se têm o mesmo tamanho e cadência, é uniformidade. Funda fragmentos em frases mais longas e alterne curta/longa de propósito.
**Antes:** > Pergunte e ele responde que quebra. Acerta. Mas acerta por correlação.
**Depois:** > Pergunte e ele responde, corretamente, que quebra, mas responde assim por correlação.

### 26. Throat-clearing / signposting
**Problema:** frase que anuncia o que vem em vez de já dizer ("O argumento é simples de enunciar", "Separo em dois horizontes", "Repare na posição da X", "Os números deixam claro").
**Teste 2026:** corte a 1ª frase de cada parágrafo — se não perde nada, era throat-clearing.
**Correção:** ir direto ao conteúdo, ou front-load o ponto (afirmar a tese e deixar os fatos sustentarem).

### 27. Intensificadores-muleta (PT-BR)
**Problema:** "de verdade", "de fato", "realmente", "muito", "mais ou menos" repetidos como ênfase vazia ("trabalho de verdade", "modelo de verdade", "entrega de fato").
**Correção:** remover o intensificador — a frase fica mais firme sem ele. Trocar por dado concreto quando possível ("os pesos abertos" em vez de "o modelo de verdade").

### 28. Fórmula de aforismo ("X é o Y de Z" / "tem nome, e é")
**Problema:** moldura dramática pra uma afirmação simples ("a camada de controle é a parte que fica", "o erro tem nome, e é...", "simetria é a linguagem da confiança").
**Correção:** afirmar o fato sem a moldura.

### 29. Conjunction openers por ritmo (E / Mas)
**Problema:** abrir frases com "E..."/"Mas..." pra dar cadência vira hábito detectável (parente da cadência uniforme).
**Correção:** juntar à oração anterior, começar pelo sujeito, ou usar conectivo que carregue sentido ("Ainda assim", "Mesmo assim").

### 30. Explicar a piada (over-explanation de exemplo) — 2026-07-03
**Problema:** destrinchar o mecanismo do exemplo/humor até matá-lo — o modelo não confia que o leitor completa a inferência. Feedback literal do autor (artigo Nexo): "Parece uma pessoa autista explicando uma piada. Explicar a piada perde a graça."
**Teste:** se depois de contar o exemplo você escreveu 2+ frases explicando POR QUE ele mostra o problema, corte-as e feche com um arremate seco de no máximo 1 frase.
**Antes:** > O problema é que ela não entende o contexto óbvio: você vai ao lava-carros pra lavar o carro, então ele precisa estar com você. Sem o carro, a viagem inteira perde o sentido.
**Depois:** > O conselho é saudável. Só esquece o carro.

### 31. Hedge duplo em atribuição incerta — 2026-07-03
**Problema:** empilhar dois hedges pra mesma incerteza numa citação ("A frase é atribuída a X" + "não há evidência sólida de que ele tenha dito isso — é uma daquelas frases que a história repete sem fonte..."). Soa prolixo e inseguro (feedback do autor: "quase que inseguro").
**Regra:** UM hedge basta — "atribuída a" já carrega toda a incerteza. Detalhe da proveniência vai pra referência/nota, não pra prosa.
**Antes:** > A frase é atribuída a William Lever. Não há evidência sólida de que ele tenha dito isso — é uma daquelas frases que a história do marketing repete há um século sem fonte confirmada —, mas o problema que ela descreve é real...
**Depois:** > A frase é atribuída a William Lever, fundador da Lever Brothers, e circula no mundo dos negócios há décadas. O problema que ela descreve é real...

### 32. Densidade estatística cumulativa (regra de processo) — 2026-07-03
**Problema:** não é um tell de frase, é de PROCESSO: cada pedido de rigor isolado parece certo (explicar o escopo do estudo, adicionar o número de agilidade, esclarecer a escala), mas o acúmulo de rodadas vira "bomba de números" — 4 parágrafos de metodologia num texto de opinião (caso Nexo: leitor externo e review comparativo com a série convergiram no mesmo diagnóstico).
**Regra:** rigor mora no APÊNDICE de evidência (tabela claim→fonte→print, ver um fluxo de rigor de fontes); a prosa fica com os 2-3 números que carregam o argumento. A cada 3-4 rodadas de edição, reler a seção mais densa contra 2 peças publicadas do mesmo veículo e perguntar: "isso tem mais estatística por parágrafo que os pares?"

