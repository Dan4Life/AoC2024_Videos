from manim import *

class Day24(ZoomedScene):
    def construct(self):
        def create_gate(label, position):
            body = Square(side_length=1.5, color=BLUE).move_to(position)
            text = Text(label).move_to(body.get_center()).scale(0.8)
            input1 = Dot(body.get_left() + UP * 0.3)
            input2 = Dot(body.get_left() + DOWN * 0.3)
            output = Dot(body.get_right())
            return VGroup(body, text, input1, input2, output)

        def create_wire(start, end, value):
            color = GREEN if value == 1 else RED
            wire = Line(start, end, color=color, stroke_width=10)
            wire.value = value
            wire.z_index = -1
            return wire

        and_gate = create_gate("AND", UP * 3)
        xor_gate = create_gate("XOR", ORIGIN)
        or_gate = create_gate("OR", DOWN * 3)

        x00_label = Text("x00").scale(0.5).next_to(and_gate[2], LEFT * 11.5)
        y00_label = Text("y00").scale(0.5).next_to(and_gate[3], LEFT * 11.5)
        z00_label = Text("z00").scale(0.5).next_to(and_gate[4], RIGHT * 8.2)

        x01_label = Text("x01").scale(0.5).next_to(xor_gate[2], LEFT * 11.5)
        y01_label = Text("y01").scale(0.5).next_to(xor_gate[3], LEFT * 11.5)
        z01_label = Text("z01").scale(0.5).next_to(xor_gate[4], RIGHT * 8.2)

        x02_label = Text("x02").scale(0.5).next_to(or_gate[2], LEFT * 11.5)
        y02_label = Text("y02").scale(0.5).next_to(or_gate[3], LEFT * 11.5)
        z02_label = Text("z02").scale(0.5).next_to(or_gate[4], RIGHT * 8.2)

        input_x00 = Dot(LEFT * 3.5 + UP * 3).set_color(RED).set_y(and_gate[2].get_y())
        input_y00 = Dot(LEFT * 3.5 + UP * 2).set_color(RED).set_y(and_gate[3].get_y())
        input_x01 = Dot(LEFT * 3.5).set_color(RED).set_y(xor_gate[2].get_y())
        input_y01 = Dot(LEFT * 3.5 + DOWN).set_color(RED).set_y(xor_gate[3].get_y())
        input_x02 = Dot(LEFT * 3.5 + DOWN * 2).set_color(RED).set_y(or_gate[2].get_y())
        input_y02 = Dot(LEFT * 3.5 + DOWN * 3).set_color(RED).set_y(or_gate[3].get_y())

        wires = [
            create_wire(input_x00.get_center(), and_gate[2].get_center(), 0),
            create_wire(input_y00.get_center(), and_gate[3].get_center(), 0),
            create_wire(input_x01.get_center(), xor_gate[2].get_center(), 0),
            create_wire(input_y01.get_center(), xor_gate[3].get_center(), 0),
            create_wire(input_x02.get_center(), or_gate[2].get_center(), 0),
            create_wire(input_y02.get_center(), or_gate[3].get_center(), 0),
        ]

        and_output = create_wire(and_gate[4].get_center(), and_gate[4].get_center() + RIGHT * 2, 0)
        xor_output = create_wire(xor_gate[4].get_center(), xor_gate[4].get_center() + RIGHT * 2, 0)
        or_output = create_wire(or_gate[4].get_center(), or_gate[4].get_center() + RIGHT * 2, 0)

        outputs = [and_output, xor_output, or_output]

        input_dots = [
            [input_x00, input_y00], 
            [input_x01, input_y01], 
            [input_x02, input_y02],
        ]

        self.play(Write(x00_label), Write(y00_label), Write(z00_label),
                  Write(x01_label), Write(y01_label), Write(z01_label),
                  Write(x02_label), Write(y02_label), Write(z02_label),
                  run_time=0.5)
        for dots in input_dots:
            self.play(*[Create(dot) for dot in dots])
        self.play(Create(and_gate), Create(xor_gate), Create(or_gate))
        self.play(*[Create(wire) for wire in wires])
        self.play(Create(and_output), Create(xor_output), Create(or_output))

        def simulate_gate(gate, dots, wires, output, cases):
            for case in cases:
                animations = []
                for i, value in enumerate(case[:2]):
                    wires[i].value = value
                    dot_color = GREEN if value else RED
                    animations.append(wires[i].animate.set_color(dot_color))
                    animations.append(dots[i].animate.set_color(dot_color))
                self.play(*animations, run_time=0.5)
                output.value = case[2]
                self.play(output.animate.set_color(GREEN if output.value else RED), run_time=0.5)

        def zoom_to_gate(gate):
            self.play(self.camera.frame.animate.move_to(gate.get_center()).set_width(9), run_time=1)

        def zoom_out():
            self.play(self.camera.frame.animate.move_to(ORIGIN).set_width(14), run_time=1)

        cases = [
            [[0, 1, 0], [1, 0, 0], [1, 1, 1]],
            [[0, 1, 1], [1, 0, 1], [1, 1, 0]],
            [[0, 1, 1], [1, 0, 1], [1, 1, 1]],
        ]

        for i, gate in enumerate([and_gate, xor_gate, or_gate]):
            zoom_to_gate(gate)
            simulate_gate(gate, input_dots[i], wires[i * 2:i * 2 + 2], outputs[i], cases[i])
            zoom_out()

        self.wait()
