# Fake News Claim Verification System (FOL + XAI + Chatbot)

**K. Ramakrishnan College of Engineering (Autonomous)**  
**Department of Artificial Intelligence and Data Science**  
**ADI1221 – Principles of Artificial Intelligence**

## Team
- PADHMA BALA.K
- RAKSHANA MANIKANDAN
- SUMITHRA.S

## Features
- First-Order Logic (FOL) knowledge base (650+ facts, 24 predicates, 10 rules)
- Consistency checking: Consistent / Inconsistent / Unknown
- Explainable AI (XAI): plain-English explanation, why, counterfactuals, fact importance
- Interactive **Chatbot** interface
- Dashboard form interface

## How to Run

### Chatbot (recommended)
```bash
pip3 install streamlit
streamlit run chatbot.py
```

### Classic dashboard
```bash
streamlit run app.py
```

### Terminal
```bash
python3 main.py
```

## Example claims
- Narendra Modi is the chief minister of India → INCONSISTENT
- Paris hosted the 2024 Olympics → CONSISTENT
- Delhi is the capital of France → INCONSISTENT
- Taj Mahal is located in Agra → CONSISTENT
- Google headquarters is in China → INCONSISTENT
