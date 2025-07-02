import json
import plotly.graph_objects as go
from collections import defaultdict

# === Step 0: Load data ===
with open("spending_data.json") as f:
    results = json.load(f)

# === Step 1: Compute totals ===
agency_totals = defaultdict(float)
agency_program_totals = defaultdict(lambda: defaultdict(float))

for entry in results:
    agency = entry['agency']
    program = entry['program']
    amount = entry['amount']

    if not agency or not program or amount is None:
        continue

    agency_totals[agency] += amount
    agency_program_totals[agency][program] += amount

# === Step 2: Top 15 agencies ===
top_15_agencies = sorted(agency_totals.items(), key=lambda x: x[1], reverse=True)[:15]
top_15_agency_names = {agency for agency, _ in top_15_agencies}

# === Step 3: Top 5 programs per agency only (strict) ===
labels = ['Government']
agency_indices = {}
program_indices = {}
links = []
node_index = 1

# Add agency nodes
for agency, _ in top_15_agencies:
    agency_indices[agency] = node_index
    labels.append(agency)
    node_index += 1

# Add program nodes + links
for agency in top_15_agency_names:
    program_spending = agency_program_totals[agency]
    top_5_programs = sorted(program_spending.items(), key=lambda x: x[1], reverse=True)[:5]

    for program, amount in top_5_programs:
        prog_key = f"{agency}::{program}"
        if prog_key not in program_indices:
            program_indices[prog_key] = node_index
            labels.append(program)
            node_index += 1

        links.append({
            'source': agency_indices[agency],
            'target': program_indices[prog_key],
            'value': amount
        })

# Government → Agency links
for agency, _ in top_15_agencies:
    links.append({
        'source': 0,
        'target': agency_indices[agency],
        'value': agency_totals[agency]
    })

# === Plot ===
fig = go.Figure(data=[go.Sankey(
    node=dict(
        pad=15,
        thickness=20,
        line=dict(color="black", width=0.5),
        label=labels
    ),
    link=dict(
        source=[link['source'] for link in links],
        target=[link['target'] for link in links],
        value=[link['value'] for link in links]
    )
)])

fig.update_layout(
    title_text="FY2025 Q2 Federal Spending: Government → Top 15 Agencies → Top 5 Programs",
    font_size=10
)

fig.show()
