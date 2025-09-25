import re
def extract_decision_proposal_motive(text):
    # 1) Decisão
    decision = next(
        (line.split(":", 1)[1].strip().lower()
         for line in text.splitlines()
         if line.lower().startswith("decisão:")),
        None
    )

    proposal = None
    # 2) Proposta só se favorável
    if decision == "favoravel":
        m = re.search(
            r"^Proposta:\s*(.*?)(?=^Motivo da decisão:|\Z)",
            text,
            flags=re.DOTALL | re.MULTILINE
        )
        if m:
            proposal = m.group(1).strip()

    # 3) Motivo da decisão
    motive = None
    m2 = re.search(r"^Motivo da decisão:\s*(.*)$", text, flags=re.MULTILINE|re.DOTALL)
    if m2:
        motive = m2.group(1).strip()

    return decision, proposal, motive