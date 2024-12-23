from manim import *
# manim -pqh --resolution 1920,1080 scene.py Day19

class Day19(Scene):

    def construct(self):
        self.counter, self.counter_tracker, self.cnt = [], [], []

        def clearCounters():
            self.counter, self.counter_tracker, self.cnt = [], [], []

        def addCounter(text, pos):
            self.cnt.append(0)
            self.counter.append(Variable(self.cnt[-1], text, num_decimal_places=0))
            self.counter[-1].label.scale(0.6)
            self.counter[-1].value.next_to(self.counter[-1].label.get_center(),RIGHT*3.6)
            self.counter[-1].move_to(pos)
            self.counter_tracker.append(self.counter[-1].tracker)

        def createStringVGroup(arr):
            strings = VGroup(*[Tex(arr[i],color=YELLOW) for i in range(len(arr))])
            strings.arrange(DOWN,buff=0.5)
            return strings
        
        def solver(patterns, words):
            clearCounters()
            addCounter(Text("Sum", color=RED), UP*3.5)
            addCounter(Text("Sum2", color=GREEN), UP*3.5+RIGHT*5.8)
            line = Line(UP*4+LEFT*2,DOWN*4+LEFT*2)

            Pattern_text = Tex("Patterns",color=BLUE).move_to(UP*3.5+LEFT*4.5)
            Patterns = createStringVGroup(patterns).move_to(LEFT*4.5+DOWN*0.4)
            
            self.play(Write(Patterns), Write(Pattern_text), Create(line))
            self.play(*[Write(self.counter[i]) for i in range(2)],run_time=0.5)
            
            for word in words:
                remObjs = []
                word_text = Tex(word,color=YELLOW).scale(2.5)
                word_text.move_to(UP*2+RIGHT*3)
                self.play(Write(word_text))
                
                n = len(word)-1
                remObjs.append(word_text)
                word_groups = []
                
                count_words = 0
                for mask in range(0,2**n):
                    cur, ok = word[0],1
                    pattern_list = []

                    for i in range(n):
                        if not ok: break
                        if mask>>i&1:
                            if cur not in patterns:ok=0
                            else: pattern_list.append(cur); cur=word[i+1]
                        else: cur+=word[i+1]

                    if cur not in patterns: ok=0
                    else: pattern_list.append(cur)
                    
                    if not ok: continue 
                    count_words+=1
                    combination_text = " + ".join(pattern_list)+" "
                    combination = Tex(combination_text,color=YELLOW).scale(1.2)
                    word_groups.append(combination)
                
                if count_words:
                    WordVGroup = VGroup(*word_groups).arrange(DOWN,buff=0.2).move_to(RIGHT*3)
                    if len(WordVGroup)>=3:WordVGroup.move_to(RIGHT*3+DOWN)
                    self.play(Create(WordVGroup))

                    remObjs.append(WordVGroup)
                    self.cnt[0]+=1; self.cnt[1]+=count_words
                    self.play(self.counter_tracker[1].animate.set_value(self.cnt[1]),
                              self.counter_tracker[0].animate.set_value(self.cnt[0]),run_time=0.5)
                else:
                    text = Tex("No Partition",color=RED).scale(2).move_to(RIGHT*3)
                    self.play(Create(text))
                    remObjs.append(text)
                    
                self.wait()
                for c in remObjs: self.remove(c)

            self.wait();self.clear();self.wait(0.5);return

        patterns = ['r', 'wr', 'b', 'g', 'bwu', 'rb', 'gb', 'br']
        words = ['brwrr', 'bggr', 'gbbr', 'rrbgbr', 'ubwu', 'bwurrg', 'brgr', 'bbrgwb']
        solver(patterns,words)
        self.wait(0.5)
