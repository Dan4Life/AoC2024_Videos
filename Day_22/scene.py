from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day22
class Day22(Scene):
    def next_secret(self, secret):
        secret = (secret ^ (secret * 64)) % 16777216
        secret = (secret ^ (secret // 32)) % 16777216
        secret = (secret ^ (secret * 2048)) % 16777216
        return secret

    def compute_next_n_secrets(self, secret, n):
        secrets = [secret]
        for _ in range(n):
            secrets.append(self.next_secret(secrets[-1]))
        return secrets[1:]

    def binary_representation(self, number, bit_width=8):
        return f"{number:0{bit_width}b}"

    def show_mix_operation(self, secret, mix_value):
        title = MathTex("\\text{Mix Operation: XOR}",color=YELLOW).to_edge(UP)
        self.play(Write(title),run_time=0.5)
        secret_binary = self.binary_representation(secret, 8)
        mix_binary = self.binary_representation(mix_value, 8)

        secret_tex = MathTex(
            "\\text{Secret: }", f"\\texttt{{{secret}}}",color=RED
        ).to_edge(LEFT).set_y(2)
        mix_tex = MathTex(
            "\\text{Mix Value: }", f"\\texttt{{{mix_value}}}",color=BLUE
        ).next_to(secret_tex, DOWN, aligned_edge=LEFT)
        secret_binary_tex = MathTex(
            "\\text{Secret (Binary): }", f"\\texttt{{{secret_binary}}}",color=RED
        ).next_to(mix_tex, DOWN, aligned_edge=LEFT)
        mix_binary_tex = MathTex(
            "\\text{Mix Value (Binary): }", f"\\texttt{{{mix_binary}}}",color=BLUE
        ).next_to(secret_binary_tex, DOWN, aligned_edge=LEFT)
        
        self.play(LaggedStart(Write(secret_tex), Write(mix_tex),Write(secret_binary_tex), Write(mix_binary_tex)))
        self.wait(0.5)

        xor_result = secret ^ mix_value
        xor_binary = self.binary_representation(xor_result, 8)

        new_value_tex = MathTex(
            "\\text{New Value: }", f"\\texttt{{{xor_result}}}",color=GREEN
        ).next_to(mix_binary_tex, DOWN, aligned_edge=LEFT)

        xor_style = VGroup(
            MathTex(f"\\texttt{{{secret_binary}}}",color=RED),
            MathTex("\\oplus",color=YELLOW),
            MathTex(f"\\texttt{{{mix_binary}}}",color=BLUE),
            MathTex("\\hline"),
            MathTex(f"\\texttt{{{xor_binary}}}",color=GREEN),
        ).arrange(DOWN, aligned_edge=LEFT).move_to(RIGHT*7+UP)
        self.play(Write(xor_style),run_time=0.5)
        self.play(Write(new_value_tex),run_time=0.5)
        self.wait();self.clear();self.wait(0.5);return

    def show_prune_operation(self,secret):
        title = MathTex("\\text{Prune Operation: Modulo}",color=YELLOW).to_edge(UP)
        self.play(Write(title),run_time=0.5)
        secret_tex = MathTex(
            "\\text{Secret: }", f"\\texttt{{{secret}}}",color=RED
        ).to_edge(LEFT).set_y(2)
        
        prune_desc = MathTex("\\text{Prune: Secret} \\mod 16777216",color=BLUE
        ).next_to(secret_tex, DOWN, aligned_edge=LEFT)
        prune_calc = MathTex(f"{secret} \\mod 16777216 = {secret % 16777216}",color=GREEN
        ).next_to(prune_desc, DOWN, aligned_edge=LEFT)
        self.play(Write(secret_tex),run_time=0.5)
        self.play(Write(prune_desc),run_time=0.5)
        self.play(Write(prune_calc),run_time=0.5)
        self.wait();self.clear();self.wait(0.5);return

    def next_secret_step(self, secret, step):
        if step == 1: return (secret ^ (secret * 64)) % 16777216
        elif step == 2: return (secret ^ (secret // 32)) % 16777216
        elif step == 3: return (secret ^ (secret * 2048)) % 16777216

    def show_pseudocode_example(self, initial_secret):
        pseudocode = VGroup(
            MathTex("\\text{Function next\_secret(secret):}"),
            MathTex("\\text{secret = (secret XOR (secret * 64) mod 16777216}", color=RED),
            MathTex("\\text{secret = (secret XOR (secret / 32)) mod 16777216}", color=BLUE),
            MathTex("\\text{secret = (secret XOR (secret * 2048)) mod 16777216}", color=YELLOW),
            MathTex("\\text{return secret}", color=GREEN)
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).scale(0.7).move_to(LEFT*2.5+UP*1.5)
        for i in range(1, len(pseudocode)):pseudocode[i].shift(RIGHT)
        
        example_title = MathTex(f"\\text{{Initial Secret = {initial_secret}}}",color=WHITE).to_edge(UP)
        self.play(Write(example_title),run_time=0.5)
        self.play(Write(pseudocode))

        secret = initial_secret
        example_steps = []
        cols = [RED,BLUE,ORANGE]
        for step in range(1, 4):
            prev_secret = secret
            secret = self.next_secret_step(secret, step)
            if step == 1: operation = f"{prev_secret} \\oplus {prev_secret*64}"
            elif step == 2: operation = f"{prev_secret} \\oplus {prev_secret//32}"
            elif step == 3: operation = f"{prev_secret} \\oplus {prev_secret*2048}"
            example_steps.append(f"\\text{{Step {step}: }} {operation} \\mod 16777216 = {secret}")

        example_steps.append(f"\\text{{New secret: }} {secret}")

        cols = [RED,BLUE,YELLOW,GREEN]
        example_steps_tex = VGroup(
            *[MathTex(step,color=cols[i]).scale(0.7) for i,step in enumerate(example_steps)]
        ).arrange(DOWN, aligned_edge=LEFT).next_to(pseudocode, DOWN, buff=1)

        self.play(Write(example_steps_tex))
        self.wait();self.clear();self.wait(0.5);return

    def show_first_n_numbers(self, secret, n):
        title = MathTex(f"\\text{{First {n} Pseudo Numbers}}").scale(0.8).to_edge(UP)
        self.play(Write(title))

        secret_tex = MathTex(
            "\\text{Secret: }", f"\\texttt{{{secret}}}",color=RED
        ).to_edge(LEFT).set_y(3).scale(0.75)

        secrets = self.compute_next_n_secrets(secret, n)
        secret_texts = VGroup(*[
            MathTex(f"{i + 1}: {secrets[i]}",color=YELLOW).scale(0.75) for i in range(n)
        ]).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)

        self.play(Write(secret_tex))
        self.play(Write(secret_texts))
        self.wait();self.clear();self.wait(0.5);return

    def show_2000th_numbers_and_sum(self, initial_secrets):
        title = MathTex("\\text{2000th Numbers}").to_edge(UP)
        self.play(Write(title))

        results = [self.compute_next_n_secrets(secret, 2000)[-1] for secret in initial_secrets]
        result_texts = VGroup(*[
            MathTex(f"\\text{{Starting Secret: }} {initial_secrets[i]} \\rightarrow {results[i]}",color=YELLOW) for i in range(len(initial_secrets))
        ]).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT)

        self.play(Write(result_texts))

        total_sum = sum(results)
        total_sum_text = MathTex(f"\\text{{Sum: }} {total_sum}",color=GREEN).to_edge(DOWN)
        self.play(Write(total_sum_text))
        self.wait();self.clear();self.wait(0.5);return

    def show_part_2_demo(self,secret,n,target):
        #Note: Only supports the case where target is found!

        title = MathTex(f"\\text{{Part 2 Demo}}").scale(0.8).to_edge(UP)
        self.play(Write(title))

        secret_tex = MathTex( "\\text{Secret: }", f"\\texttt{{{secret}}} \\hspace{{3 mm}} ({{{secret%10}}})",color=RED
        ).to_edge(LEFT).set_y(3).scale(0.75)

        target_tex = MathTex( "\\text{Target: }", f"{target}",color=RED).move_to(UP)
        dif_tex = MathTex( "\\text{Difference: }", f"{0}",color=YELLOW)
        list_tex = MathTex( "\\text{List: }", f"-",color=GREEN).move_to(DOWN+RIGHT)

        secrets = self.compute_next_n_secrets(secret, n)
        secret_texts = VGroup(*[
            MathTex(f"{i + 1}: {secrets[i]} \\hspace{{3 mm}} ({secrets[i]%10})",color=YELLOW).scale(0.75) for i in range(n)
        ]).arrange(DOWN, aligned_edge=LEFT).to_edge(LEFT).set_y(-0.2)

        self.play(Write(secret_tex),Write(target_tex))
        self.play(Write(secret_texts),Write(dif_tex),Write(list_tex))


        pointer = Triangle(color=YELLOW, fill_opacity=1, fill_color=YELLOW).scale(0.1).rotate(PI/2)
        pointer.next_to(secret_tex, RIGHT)
        self.play(FadeIn(pointer))


        cur = secret%10
        cur_list = []
        
        for i in range(len(secrets)):
            dif = secrets[i]%10 - cur 
            cur_list.append(dif)
            self.play(pointer.animate.next_to(secret_texts[i],RIGHT))
            dif_tex.become(MathTex( "\\text{Difference: }", f"{dif}",color=YELLOW))
            list_tex.become(MathTex( "\\text{List: }", f"{cur_list}",color=GREEN).move_to(DOWN+RIGHT))
            cur = secrets[i]%10

            if len(cur_list)>=4 and cur_list[-4:]==target:
                list_tex.become(MathTex( "\\text{List: }", f"{cur_list}",color=RED).move_to(DOWN+RIGHT))
                ans_tex = MathTex( "\\text{Answer: }", f"{cur}",color=RED).move_to(DOWN*2+RIGHT)
                self.play(Write(ans_tex))
                break

            self.wait(0.5)
        
        self.wait();self.clear();self.wait(0.5);return

    
    def construct(self):
        initial_secrets = [1, 10, 100, 2024]
        self.show_mix_operation(42, 15)
        self.show_prune_operation(100000000)
        self.show_pseudocode_example(123)
        self.show_first_n_numbers(123, 10)
        self.show_2000th_numbers_and_sum(initial_secrets)
        target = [-1,-1,0,2]
        self.show_part_2_demo(123,10,target)
