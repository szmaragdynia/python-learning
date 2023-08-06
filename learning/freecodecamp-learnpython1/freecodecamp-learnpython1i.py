



#------------------------------
print("\n------------------------------")


#------------------------------
print("\n------------------------------")

set1 = [
    "Jakiego koloru jest Słońce?\n(a) zielonego\n(b) Żółtego\n: ",
    "Jakiego koloru jest grunt?\n(a) brązowego\n(b) białosiankowatego\n: ",
    "Jakiego koloru jest kolor zielony?\n(a) zielonego\n(b) Żółtego\n: ",
    ]

questions_and_answers = [
    QA(set1[0], "b"),
    QA(set1[1], "a"),
    QA(set1[2], "a"),
]

def run_test(questions_and_answers):
    score = 0
    for qa in questions_and_answers:
        answer = input(qa.question)
        if answer == qa.answer:
            score += 1
    print("You scored " + str(score) +" out of " + str(len(questions_and_answers)))

run_test(questions_and_answers)
