# graph.py
import plotly.graph_objects as go

def render_sankey(results):
    from collections import defaultdict

    # === Aggregate ===
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

    # === Top 15 agencies and top 5 programs each ===
    top_15_agencies = sorted(agency_totals.items(), key=lambda x: x[1], reverse=True)[:15]
    top_agencies = {agency for agency, _ in top_15_agencies}

    labels = ['Government']
    agency_indices = {}
    program_indices = {}
    links = []
    node_index = 1

    for agency, _ in top_15_agencies:
        agency_indices[agency] = node_index
        labels.append(agency)
        node_index += 1

    for agency in top_agencies:
        top_programs = sorted(agency_program_totals[agency].items(), key=lambda x: x[1], reverse=True)[:3]
        for program, amount in top_programs:
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

    for agency, _ in top_15_agencies:
        links.append({
            'source': 0,
            'target': agency_indices[agency],
            'value': agency_totals[agency]
        })

    # === Sankey ===
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

    fig.update_layout(title_text="Government → Top 15 Agency → Top 5 Programs", font_size=10)
    return fig
