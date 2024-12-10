import pandas as pd
import numpy as np
from Answers import ans
from matplotlib import pyplot as plt

def color_map(val):
    color = 'red' if val == 'X' else 'black'
    return 'color: %s' % color

class Grader():
    def __init__(self):
        print(
        '''주의사항: 답안은 띄어쓰기나 쉼표 등이 없이 이어서 입력해주세요. (예: 13452.....)
        과목 명은 아래와 같습니다: 
        1교시 생명약학: 생화학, 미생물학, 약물학, 예방약학, 병태생리학
        2교시 산업약학: 물리약학, 합성학, 분석학, 약제학, 생약학
        3교시 임상 및 실무약학: 약물치료학, 약무실무, 품질관리, 약무행정
        4교시 보건의약관계법규: 약사법\n''')

    def __call__(self):
        self.accept_edition()
        self.accept_answers()
        print('\n'+'='*100+'\n')
        self.grade()
        self.display_results()
        return self.df_score, self.df_total

    def accept_edition(self):
        edition = int(input('회차를 입력해주세요:'))
        if edition not in [71,72,73,74,75]:
            raise ValueError('유효하지 않은 회차입니다.')
        else:
            self.answers = ans[edition]
            if not self.check_validity():
                raise ValueError('정확한 답안이 아닙니다.')
            else:
                return True
    
    def check_validity(self):
        vals = [len(i) for i in self.answers.values()]
        self.lens = [20, 20, 20, 20, 20, 18, 18, 18, 18, 18, 77, 27, 18, 18, 20]
        clar = True
        for (i, j) in zip(vals, self.lens):
            if i != j:
                clar = False
        return clar

    def accept_answers(self):
        self.accepted = dict()
        for f in ['생화학', '미생물학', '약물학', '예방약학', '병태생리학']:
            field, input_ = self.input_by_field(f, 20)
            self.accepted[field] = input_
        for f in ['물리약학', '합성학', '분석학', '약제학', '생약학']:
            field, input_ = self.input_by_field(f, 18)
            self.accepted[field] = input_
        _, input_1 = self.input_by_field('약물치료학(1~20)', 20)
        _, input_2 = self.input_by_field('약물치료학(21~40)', 20)
        _, input_3 = self.input_by_field('약물치료학(41~60)', 20)
        _, input_4 = self.input_by_field('약물치료학(61~77)', 17)
        self.accepted['약물치료학'] = input_1+input_2+input_3+input_4
        field, input_ = self.input_by_field('약무실무', 27)
        self.accepted[field] = input_
        field, input_ = self.input_by_field('품질관리', 18)
        self.accepted[field] = input_
        field, input_ = self.input_by_field('약무행정', 18)
        self.accepted[field] = input_
        field, input_ = self.input_by_field('약사법', 20)
        self.accepted[field] = input_

    def input_to_list(self, input_):
        return [int(digit) for digit in str(input_)]

    def input_by_field(self, field, length):
        while(True):
            input_ = self.input_to_list(input(f'{field} 답안을 입력해주세요.'))
            if len(input_) != length:
                print(f'{field} 답안이 적절하지 않습니다. 다시 입력해주세요.')
            else:
                break
        return field, input_

    def grade(self):
        results, counts = [], []
        for val_ans, val_acc in zip(self.answers.values(), self.accepted.values()):
            bool_ = [i == j for i, j in zip(val_ans, val_acc)]
            results.append(bool_)
            counts.append(sum(bool_))
        field1 = sum(counts[:5])
        field2 = sum(counts[5:10])/90 * 100
        field3 = sum(counts[10:14])/140 * 100
        field4 = counts[-1]/20 * 100

        f1, f2, f3, f4 = [], [], [], []
        for r in results[:5]:
            f1.extend(r)
        for r in results[5:10]:
            f2.extend(r)
        f3.extend(results[10])
        for r in results[11:]:
            f4.extend(r)
            
        wrong1 = [idx+1 for idx, i in enumerate(f1) if not i]
        wrong2 = [idx+1 for idx, i in enumerate(f2) if not i]
        wrong3 = [idx+1 for idx, i in enumerate(f3) if not i]
        wrong4 = [idx+1 for idx, i in enumerate(f4) if not i]

        self.avg = sum(counts)/350 * 100
        self.each = [sum(counts[:5]),
                     sum(counts[5:10])/90 * 100,
                     sum(counts[10:14])/140 * 100,
                     counts[-1]/20 * 100]

        if self.avg >= 60 and all([i >= 40 for i in self.each]):
            print('합격입니다!')
        else:
            print('실격입니다...')
        print(f'총계:{sum(counts)}점 --- {self.avg:.2f}%\n1교시 생명약학:{self.each[0]:.2f}%\n2교시 산업약학:{self.each[1]:.2f}%\n3교시 임상 및 실무약학:{self.each[2]:.2f}%\n4교시 보건의약관계법규:{self.each[3]:.2f}%')
        print('자세한 결과는 아래를 참고하세요:\n')
        
        fields = ['생화학', '미생물학', '약물학', '예방약학', '병태생리학',
                  '물리약학', '합성학', '분석학', '약제학', '생약학',
                  '약물치료학', '약무실무', '품질관리', '약무행정', '약사법']
        
        score, result = dict(), dict()
        score['총점'] = sum(counts)
        for idx, f in enumerate(fields):
            score[f] = [counts[idx]]
            if self.lens[idx] < 77:
                tmp = ['-' for i in range(77-self.lens[idx])]
                result[f] = ['O' if i else 'X' for i in results[idx]]+tmp
            else:
                result[f] = ['O' if i else 'X' for i in results[idx]]
        self.df_score = pd.DataFrame.from_dict(score).transpose().rename(columns = {0: '점수'})
        self.df_total = pd.DataFrame.from_dict(result).style.applymap(color_map)
        self.df_total.index += 1
        
        print('#'*50+'오답노트'+'#'*50)
        for f, i in zip(['생명약학', '산업약학', '임상 및 실무약학 1', '임상 및 실무약학 2'], [wrong1, wrong2, wrong3, wrong4]):
            print(f'{f}: {i}\n')

    def display_results(self):
        fig, ax = plt.subplots(figsize=(8, 6))
        fields = ('Total', 'Field 1', 'Field 2', 'Field 3', 'Field 4')
        y_pos = np.arange(len(fields))
        performance = [self.avg] + self.each
        ax.barh(y_pos, performance, align='center')
        ax.set_yticks(y_pos, labels=fields)
        ax.invert_yaxis()
        ax.set_xlabel('Score (%)')
        ax.set_title('Results')
        ax.axvline(x=60, color='green', linestyle='--', linewidth=2)
        ax.axvline(x=40, color='red', linestyle='--', linewidth=2)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_color('#DDDDDD')
        ax.tick_params(bottom=False, left=False)
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, color='#EEEEEE')
        ax.yaxis.grid(False)

        ax.set_xlim([0, 100])
        
        fig.tight_layout()
        plt.show()
