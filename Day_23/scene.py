from manim import *
from itertools import combinations

class Day23(Scene):
    def build_graph(self, connections):
        graph = {}
        for a, b in connections:
            graph.setdefault(a, set()).add(b)
            graph.setdefault(b, set()).add(a)
        return graph

    def find_cliques_of_length(self, graph, length):
        cliques = []
        for nodes in combinations(graph.keys(), length):
            if all(node2 in graph[node1] for node1, node2 in combinations(nodes, 2)):
                cliques.append(nodes)
        return cliques

    def find_largest_clique(self, graph):
        for size in range(len(graph), 2, -1):
            cliques = self.find_cliques_of_length(graph, size)
            if cliques: return cliques[0]
        return []

    def draw_graph(self, graph, node_positions):
        for node, position in node_positions.items():
            self.play(Create(Dot(position, color=BLUE).scale(1.3)),run_time=0.1)
            label = Text(node, font_size=24).move_to(position * 1.2)
            self.play(Write(label),run_time=0.1)

        for node, neighbors in graph.items():
            for neighbor in neighbors:
                if node < neighbor:
                    self.play(Create(Line(node_positions[node], node_positions[neighbor], color=WHITE)),run_time=0.1)
        
    def show_cliques(self, cliques, node_positions, label, to_right):
        title = Text(label, font_size=28, color=YELLOW).to_edge(UP)
        self.play(Write(title), run_time=0.5)
        current_y_position = 2.5
        clique_texts = []

        for clique in cliques:
            edges = [
                Line(node_positions[node1], node_positions[node2], color=YELLOW)
                for node1, node2 in combinations(clique, 2)
            ]
            dots = [ Dot(node_positions[node]).scale(1.3) for node in clique ]
            recolor_animations = [ dot.animate.set_color(YELLOW) for dot in dots ]

            col = RED 
            ok = 0
            for c in clique: 
                if c[0]=='t':ok=1

            if ok: col=GREEN
            clique_text = Text(f"{', '.join(clique)}", font_size=24, color=col)
            if to_right: clique_text.move_to(np.array([6, current_y_position, 0]))
            else: clique_text.move_to(np.array([-6, current_y_position, 0]))
            current_y_position -= 0.5
            clique_texts.append(clique_text)

            self.play(*[Create(edge) for edge in edges], *recolor_animations, Write(clique_text))
            self.wait(1)
            reset_color_animations = [ Uncreate(dot) for dot in dots ]
            self.play(*reset_color_animations, *[Uncreate(edge) for edge in edges])

        self.play(FadeOut(title))

    def construct(self):
        raw_connections = [
            "kh-tc", "qp-kh", "de-cg", "ka-co", "yn-aq", "qp-ub",
            "cg-tb", "vc-aq", "tb-ka", "wh-tc", "yn-cg", "kh-ub",
            "ta-co", "de-co", "tc-td", "tb-wq", "wh-td", "ta-ka",
            "td-qp", "aq-cg", "wq-ub", "ub-vc", "de-ta", "wq-aq",
            "wq-vc", "wh-yn", "ka-de", "kh-ta", "co-tc", "wh-qp",
            "tb-vc", "td-yn",
        ]
        connections = [tuple(conn.split("-")) for conn in raw_connections]
        graph = self.build_graph(connections)

        nodes = list(graph.keys())
        node_positions = {
            node: np.array(
                [2.5*np.cos(i*2*np.pi/len(nodes)), 2.5*np.sin(i*2*np.pi/len(nodes))-0.6, 0]
            ) for i, node in enumerate(nodes)
        }

        self.draw_graph(graph, node_positions)

        cliques_3 = self.find_cliques_of_length(graph, 3)
        self.show_cliques(cliques_3, node_positions, label="Cliques of Length 3",to_right=0)

        largest_clique = self.find_largest_clique(graph)
        self.show_cliques([largest_clique], node_positions, label="Largest Clique",to_right=1)
        self.wait()
