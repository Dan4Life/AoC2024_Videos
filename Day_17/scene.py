from manim import *

# manim -pqh --resolution 1920,1080 scene.py Day17

class Day17(Scene):

    def construct(self):

        def createArray(curA):
            v = VGroup(
                *[
                    VGroup(
                        Square(side_length=0.7, color=WHITE),
                        Text(str(x), font_size=40),
                        Text(str(i), font_size=20)
                    )
                    for i,x in enumerate(curA)
                ])
            for i in range(len(v)):
                if i%2: col = BLUE 
                else: col = RED
                v[i].set_color(col)
            v.arrange(RIGHT, buff=0.1)
            for i in range(len(v)):
                v[i][2].move_to(v[i][1].get_bottom()+DOWN*.35)
            return v

        def combo(x,reg):
            if x<=3:return x
            return reg[x-4]

        def f(a,v):
            reg =[a,0,0]
            j = 0
            ans = []
            while j<len(v):
                x = v[j]
                if x==0:reg[0]//=2**combo(v[j+1],reg)
                elif x==1:reg[1]^=v[j+1]
                elif x==2:reg[1]=combo(v[j+1],reg)%8
                elif x==3 and reg[0]: j=v[j+1]-2
                elif x==4: reg[1]^=reg[2]
                elif x==5: ans.append(combo(v[j+1],reg)%8)
                elif x==6: reg[1]=reg[0]//(2**combo(v[j+1],reg))
                elif x==7: reg[2]=reg[0]//(2**combo(v[j+1],reg))
                j+=2
            return ans

        def recur(n,v,pos):
            for i in range(8):
                if f(n*8+i,v)[0]==v[pos]:
                    if pos==0: return n*8+i 
                    ans = recur(n*8+i,v,pos-1)
                    if ans!=-1: return ans 
            return -1

        def createRegister(register_name="A", register_value=0, box_color=WHITE):
            name_text = MathTex(f"\\text{{Reg}}_{{{register_name}}}", color=box_color).scale(0.8)
            value_text = MathTex(f"{register_value}", color=box_color).scale(1.0)

            def update_box():
                box_width = max(name_text.width, value_text.width) + 0.1
                box_height = name_text.height + value_text.height + 0.25
                box.width = box_width
                box.height = box_height
                name_text.move_to(box.get_top() + DOWN * 0.3)
                value_text.move_to(box.get_center()+DOWN*0.25)

            box = Rectangle(width=2, height=1, color=box_color)
            update_box()

            register = VGroup(box, name_text, value_text)

            def update_value(new_value):
                value_text.become(MathTex(f"{new_value}", color=box_color).scale(1.0))
                update_box()

            register.update_value = update_value
            return register


        def solver(v,a,b=0,c=0):
            arr = createArray(v).move_to(RIGHT*3)
            self.play(Create(arr))

            instructions = VGroup(
                MathTex("0: \\text{Reg}_A \\gets \\left\\lfloor \\frac{\\text{Reg}_A}{2^{\\text{combo(operand)}}} \\right\\rfloor", color=WHITE),
                MathTex("1: \\text{Reg}_B \\gets \\text{Reg}_B \\oplus \\text{literal(operand)}", color=WHITE),
                MathTex("2: \\text{Reg}_B \\gets \\text{combo(operand)} \\bmod 8", color=WHITE),
                MathTex("3: \\text{if Reg}_A \\neq 0, \\text{ jump to literal(operand)}", color=WHITE),
                MathTex("4: \\text{Reg}_B \\gets \\text{Reg}_B \\oplus \\text{Reg}_C", color=WHITE),
                MathTex("5: \\text{output combo(operand)} \\bmod 8", color=WHITE),
                MathTex("6: \\text{Reg}_B \\gets \\left\\lfloor \\frac{\\text{Reg}_A}{2^{\\text{combo(operand)}}} \\right\\rfloor", color=WHITE),
                MathTex("7: \\text{Reg}_C \\gets \\left\\lfloor \\frac{\\text{Reg}_A}{2^{\\text{combo(operand)}}} \\right\\rfloor", color=WHITE)
            )

            for instruction in instructions:
                instruction.align_to(instructions[0], LEFT)
            instructions.arrange(DOWN, buff=0.2).scale(0.6)
            instructions.move_to(LEFT * 4+DOWN*1.5)

            func_instructions = VGroup(
                MathTex("\\text{literal(operand)} \\gets \\text{operand}", color=WHITE),
                MathTex(
                    "\\text{combo(operand)} \\gets "
                    "\\begin{cases} "
                    "\\text{operand} & \\text{if operand} \\leq 3 \\\\ "
                    "\\text{Reg}_A & \\text{if operand} = 4 \\\\ "
                    "\\text{Reg}_B & \\text{if operand} = 5 \\\\ "
                    "\\text{Reg}_C & \\text{if operand} = 6 "
                    "\\end{cases}",
                    color=WHITE
                )
            )
            func_instructions.arrange(DOWN, buff=0.2).scale(0.52).move_to(LEFT * 5.1 + UP * 2.5)

            for instruction in func_instructions:
                instruction.align_to(func_instructions[0], LEFT)

            Rect = SurroundingRectangle(instructions,color=YELLOW)
            Rect2 = SurroundingRectangle(func_instructions,color=YELLOW)
            instructions.add(Rect); func_instructions.add(Rect2)
            self.play(Write(instructions),Write(func_instructions))

            Reg = [   createRegister("A",a,RED).move_to(UP*3+RIGHT*0.5),
                        createRegister("B",b,BLUE).move_to(UP*3+RIGHT*3),
                        createRegister("C",c,GREEN).move_to(UP*3+RIGHT*5.5)]

            self.play(Write(Reg[0]),Write(Reg[1]),Write(Reg[2]), run_time=0.5)

            pointer = Triangle(color=YELLOW, fill_opacity=1, fill_color=YELLOW).scale(0.2)
            pointer.next_to(arr[0], DOWN).set_y(arr.get_y()-0.75)

            output = Text("Output = ").next_to(arr, DOWN*3.5).scale(0.5)
            self.play(Create(pointer), Write(output), run_time=0.5)
            
            j, ans, reg = 0, [], [a, b, c]
            highlighted_instr, highlighted_func = None, None
            
            NUM = len(f(a,v))
            while j < len(v):
                x, oldj = v[j], j

                if x == 0:
                    instr_index, func_index = 0, 1
                    new_v = reg[0] //  2**combo(v[j+1], reg)
                    values_tex = MathTex(
                        f"\\text{{Reg}}_A \\gets \\left\\lfloor \\frac{{{reg[0]}}}{{2^{combo(v[j+1], reg)}}} \\right\\rfloor = {new_v}",
                        color=YELLOW
                    )
                    reg[0] = new_v
                elif x == 1:  # bxl
                    instr_index, func_index = 1, 0
                    new_v = reg[1] ^ v[j+1]
                    values_tex = MathTex(
                        f"\\text{{Reg}}_B \\gets {reg[1]} \\oplus {v[j+1]} = {new_v}",
                        color=YELLOW
                    )
                    reg[1] = new_v
                elif x == 2:  # bst
                    instr_index, func_index = 2, 1
                    new_v = combo(v[j+1], reg) % 8
                    values_tex = MathTex(
                        f"\\text{{Reg}}_B \\gets {combo(v[j+1], reg)} \\bmod 8 = {new_v}",
                        color=YELLOW
                    )
                    reg[1] = new_v
                elif x == 3 and reg[0]:  # jnz
                    instr_index, func_index = 3, 0
                    values_tex = MathTex(
                        f"\\text{{if }} {reg[0]} \\neq 0, \\text{{ jump to }} {v[j+1]}",
                        color=YELLOW
                    )
                    j = v[j+1] - 2
                elif x == 4:  # bxc
                    instr_index, func_index = 4, 0
                    new_v = reg[1] ^ reg[2]
                    values_tex = MathTex(
                        f"\\text{{Reg}}_B \\gets {reg[1]} \\oplus {reg[2]} = {new_v}",
                        color=YELLOW
                    )
                    reg[1] = new_v
                elif x == 5:  # out
                    instr_index, func_index = 5, 1
                    new_v = combo(v[j+1], reg) % 8
                    values_tex = MathTex(
                        f"\\text{{output }} {combo(v[j+1], reg)} \\bmod 8 = {new_v}",
                        color=YELLOW
                    )
                    ans.append(new_v)
                elif x == 6:  # bdv
                    instr_index, func_index = 6, 1
                    new_v = reg[0] // (2**combo(v[j+1], reg))
                    values_tex = MathTex(
                        f"\\text{{Reg}}_B \\gets \\left\\lfloor \\frac{{{reg[0]}}}{{2^{combo(v[j+1], reg)}}} \\right\\rfloor = {new_v}",
                        color=YELLOW
                    )
                    reg[1] = new_v
                elif x == 7:  # cdv
                    instr_index, func_index = 7, 1
                    new_v = reg[0] // (2**combo(v[j+1], reg))
                    values_tex = MathTex(
                        f"\\text{{Reg}}_C \\gets \\left\\lfloor \\frac{{{reg[0]}}}{{2^{combo(v[j+1], reg)}}} \\right\\rfloor = {new_v}",
                        color=YELLOW
                    )
                    reg[2] = new_v
                j += 2

                highlighted_instr = instructions[instr_index]
                highlighted_func = func_instructions[func_index]
                values_tex.scale(0.6).next_to(arr, UP*3.5)

                animations = [
                            highlighted_instr.animate.set_color(RED),
                            highlighted_func.animate.set_color(BLUE),
                            pointer.animate.set_x(arr[oldj].get_center()[0]),
                            Write(values_tex)
                ]
                if x!=3 or reg[0]: 
                    self.play(*animations, run_time=0.3)

                    if x != 5:
                        for k in range(3):
                            Reg[k].update_value(reg[k])
                    else:
                        cur = output.text
                        cur+=str(ans[-1])
                        NUM-=1
                        if NUM>0: cur+=','
                        output.become(Text(cur).next_to(arr, DOWN*3.5).scale(0.5))
                        output.text=cur

                    self.play(FadeOut(values_tex), highlighted_instr.animate.set_color(WHITE),
                                highlighted_func.animate.set_color(WHITE),run_time=0.3)
                else: self.play(Uncreate(pointer),run_time=0.3)
        
            self.wait();self.clear();self.wait(0.5);return


        def solver2(v,a,b=0,c=0):
            solver(v,a,b,c)
            A = recur(0,v,len(v)-1)
            if a!=A: solver(v,A,b,c)

        A, v = 729, [0, 1, 5, 4, 3, 0]
        solver(v,A)
        A, v = 2024, [0, 3, 5, 4, 3, 0]
        solver2(v,A)
        solver(v,A)
        self.wait(0.5)
        
        
