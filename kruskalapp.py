import streamlit as st
import networkx as nx
from pyvis.network import Network
import streamlit.components.v1 as components

def draw_graph(graph, highlight_edges=[], start_node=None):
    net = Network(height="600px", width="100%", directed=graph.is_directed())

    for node in graph.nodes:
        if node == start_node:
            net.add_node(node, label=str(node), color='green', size=25)
        else:
            net.add_node(node, label=str(node), color='blue')

    for u, v, data in graph.edges(data=True):
        weight = data.get('weight', 1)
        color = 'red' if (u,v) in highlight_edges or (v,u) in highlight_edges else 'blue'
        net.add_edge(u, v, label=str(weight), arrows="to" if graph.is_directed() else "", color=color)

    tmp_file = "temp_graph.html"
    net.save_graph(tmp_file)

    with open(tmp_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    return html_content

st.title("Network Planner Using Kruskal's Algorithm")

if "graph" not in st.session_state:
    st.session_state.graph = nx.DiGraph()

# Add nodes
with st.expander("Add Node"):
    node_name = st.text_input("Node Name", key="node_input")
    if st.button("Add Node"):
        if node_name:
            if node_name not in st.session_state.graph.nodes:
                st.session_state.graph.add_node(node_name)
                st.success(f"Node '{node_name}' added")
            else:
                st.warning("Node already exists")
        else:
            st.warning("Please enter a node name")

# Add edges
with st.expander("Add Directed Edge"):
    from_node = st.text_input("From Node", key="from_node")
    to_node = st.text_input("To Node", key="to_node")
    weight = st.number_input("Weight", min_value=1, value=1, step=1, key="weight")
    if st.button("Add Edge"):
        if from_node in st.session_state.graph.nodes and to_node in st.session_state.graph.nodes:
            st.session_state.graph.add_edge(from_node, to_node, weight=weight)
            st.success(f"Edge from '{from_node}' to '{to_node}' with weight {weight} added")
        else:
            st.warning("Both nodes must exist before adding an edge")

# Show original graph
if st.button("Show Graph"):
    if st.session_state.graph.number_of_nodes() == 0:
        st.warning("Add some nodes first")
    else:
        html = draw_graph(st.session_state.graph)
        components.html(html, height=650, scrolling=True)

st.markdown("---")

# Select start node (optional)
start_node = None
if st.session_state.graph.number_of_nodes() > 0:
    start_node = st.selectbox("Select Starting Node (for visualization)", options=st.session_state.graph.nodes)

# Calculate MST using Kruskal's algorithm
if st.button("Calculate Minimum Cost using Kruskal"):
    if st.session_state.graph.number_of_nodes() == 0:
        st.warning("Add some nodes first")
    else:
        undirected_graph = st.session_state.graph.to_undirected()
        mst = nx.minimum_spanning_tree(undirected_graph, algorithm='kruskal', weight='weight')
        total_cost = sum(d.get('weight', 1) for u, v, d in mst.edges(data=True))
        st.success(f"Total minimum cost (MST) is: {total_cost}")
        html = draw_graph(undirected_graph, highlight_edges=mst.edges(), start_node=start_node)
        components.html(html, height=650, scrolling=True)
