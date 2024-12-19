from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day11

class Day11(ZoomedScene):
    def construct(self):
        stones = [125, 17]
        initial_positions = [ LEFT, RIGHT ]

        STONES = VGroup(
            *[
                self.create_stone(position, number)
                for position, number in zip(initial_positions, stones)
            ]
        )
        self.counter = Variable(3,Text("Stones",color=RED), num_decimal_places=0)
        self.counter.label.scale(0.6)
        self.counter.value.next_to(self.counter.label.get_center(),RIGHT*3.6)
        self.counter_tracker=self.counter.tracker
        self.counter.move_to(self.camera.frame_center+(RIGHT+UP)*0.8)

        
        self.arrange_elements(STONES)
        self.fit_camera_to_stones(STONES)
        self.play(FadeIn(STONES))

        num_rounds = 6
        ok = 0
        for _ in range(num_rounds):
            new_stones = VGroup()
            TOT = [0]*len(STONES)
            for i,stone in enumerate(STONES):
                position = stone.get_center()
                num = int(stone[1].get_tex_string())
                num1, num2 = num, 0
                if num == 0:
                    num1+=1; num2=-1
                elif len(str(num))%2:
                    num1*=2024; num2=-1
                else:
                    sz = len(str(num))//2
                    num1, num2 = int(str(num)[:sz]), int(str(num)[sz:])

                new_stone1 = self.create_stone(position, num1)
                new_stones.add(new_stone1)
                TOT[i]+=1
                if num2!=-1:
                    new_stone2 = self.create_stone(position, num2)
                    new_stones.add(new_stone2)
                    TOT[i]+=1

            self.arrange_elements(new_stones)
            self.fit_camera_to_stones(new_stones)

            animations = []
            v = []
            j = 0
            dif = 0

            for i,stone in enumerate(STONES):
                if TOT[i]==1:
                    animations.append(ReplacementTransform(stone,new_stones[j]))
                else:
                    animations.append(ReplacementTransform(stone,new_stones[j]))
                    animations.append(FadeIn(new_stones[j+1]))
                    v.append(j+1)
                    dif+=1
                j+=TOT[i]

            self.remove(new_stones)
            self.play(*animations)
            
            if ok:
                self.play(self.counter.animate.move_to(STONES.get_top()+UP/3),
                      self.counter_tracker.animate.increment_value(dif),run_time=0.5)
            else:
                self.counter.move_to(STONES.get_top()+UP/3+[0.75,0,0])
                self.add(self.counter)
                ok = 1
            
            for i in v:
                self.remove(new_stones[i])
            self.remove(STONES)
            STONES = new_stones.copy()
            self.add(STONES)
            self.wait(0.5)

    def create_stone(self, position, number):
        circle = Circle(radius=0.5, color=WHITE).move_to(position)
        label = MathTex(str(number), color=RED)

        label_width = label.get_width()
        label_height = label.get_height()
        circle_diameter = 2 * circle.radius
        max_label_size = 0.8 * circle_diameter
        scale_factor = min(max_label_size / label_width, max_label_size / label_height)

        if len(str(number)) < 4:
            scale_factor = min(scale_factor, 1.0)
        
        label.scale(scale_factor).move_to(circle.get_center())
        return VGroup(circle, label)


    def arrange_elements(self, vgroup):
        screen_width = config.frame_width 
        screen_height = config.frame_height 
        element_spacing = 2*vgroup[0][0].radius+.2 
        max_cols = int(screen_width / element_spacing)

        for i, element in enumerate(vgroup):
            row = i // max_cols
            col = i % max_cols
            x_position = -screen_width / 2 + (col + 0.5) * element_spacing
            y_position = screen_height / 2 - (row + 0.5) * element_spacing
            element.move_to([x_position, y_position, 0])

    def fit_camera_to_stones(self, stones):
        left = stones.get_critical_point(LEFT)[0]
        right = stones.get_critical_point(RIGHT)[0]
        total_width = right - left
        self.play(self.camera.frame.animate.set_width(total_width * 1.1).move_to(stones.get_center()))
