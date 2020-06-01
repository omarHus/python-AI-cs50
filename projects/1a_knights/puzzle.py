from logic import *



AKnight = Symbol("A is a Knight")
AKnave = Symbol("A is a Knave")

BKnight = Symbol("B is a Knight")
BKnave = Symbol("B is a Knave")

CKnight = Symbol("C is a Knight")
CKnave = Symbol("C is a Knave")

# # Base knowledge

def base_knowledge(Knave, Knight):
    return And(
        Not(And(Knave, Knight)),
        Biconditional(Not(Knave), Knight),
        Biconditional(Not(Knight), Knave)
    )

def sentence_knowledge(sentence, Knave, Knight):
    return And(
        Biconditional(sentence, Knight),
        Biconditional(Not(sentence), Knave)
    )


# Puzzle 0
# A says "I am both a knight and a knave."
# Encode if said by a KNave then it is a lie
sentence = Symbol("I am both a knight and a knave")
knowledge0 = And(
    base_knowledge(AKnave, AKnight),
    sentence_knowledge(sentence, AKnave, AKnight),
    Implication(sentence, And(AKnight, AKnave)),

)

# Puzzle 1
# A says "We are both knaves."
# B says nothing.
sentenceA = Symbol("We are both Knaves")
sentenceB = Symbol("")

knowledge1 = And(
    base_knowledge(AKnave, AKnight),
    base_knowledge(BKnave, BKnight),
    sentence_knowledge(sentenceA, AKnave, AKnight),
    sentence_knowledge(sentenceB, BKnave, BKnight),
    Implication(sentenceA, And(AKnave, BKnave)),
    Implication(Not(sentenceA), Or(Not(AKnave), Not(BKnave)))
)

# Puzzle 2
# A says "We are the same kind."
# B says "We are of different kinds."
sentenceA = Symbol("We are the same kind.")
sentenceB = Symbol("We are of different kinds.")
knowledge2 = And(
    base_knowledge(AKnave, AKnight),
    base_knowledge(BKnave, BKnight),
    sentence_knowledge(sentenceA, AKnave, AKnight),
    sentence_knowledge(sentenceB, BKnave, BKnight),
    Implication(sentenceA, Or(And(AKnight, BKnight), And(AKnave, BKnave))),
    Implication(sentenceB, Not(Or(And(AKnight, BKnight),And(AKnave, BKnave)))),
    Biconditional(sentenceA, Not(sentenceB)),
    Biconditional(sentenceB, Not(sentenceA))
)

# Puzzle 3
# A says either "I am a knight." or "I am a knave.", but you don't know which.
# B says "A said 'I am a knave'."
# B says "C is a knave."
# C says "A is a knight."
sentenceA1 = Symbol("I am a knight.")
sentenceA2 = Symbol("I am a knave.")
sentenceB1 = Symbol("A said 'I am a knave'.")
sentenceB2 = Symbol("C is a knave")
sentenceC = Symbol("A is a knight")

knowledge3 = And(
    base_knowledge(AKnave, AKnight),
    base_knowledge(BKnave, BKnight),
    base_knowledge(CKnave, CKnight),
    sentence_knowledge(sentenceB1, BKnave, BKnight),
    sentence_knowledge(sentenceB2, BKnave, BKnight),
    sentence_knowledge(sentenceC,  CKnave, CKnight),
    Implication(sentenceA1, AKnight),
    Implication(sentenceA2, AKnave),
    Implication(AKnave, Not(sentenceA2)),
    Or(sentenceA1, sentenceA2),
    Implication(sentenceB1, sentenceA2),
    Implication(sentenceB2, CKnave),
    Implication(Not(sentenceB2), CKnight),
    Implication(sentenceC, AKnight),
)


def main():
    symbols = [AKnight, AKnave, BKnight, BKnave, CKnight, CKnave]
    puzzles = [
        ("Puzzle 0", knowledge0),
        ("Puzzle 1", knowledge1),
        ("Puzzle 2", knowledge2),
        ("Puzzle 3", knowledge3)
    ]
    for puzzle, knowledge in puzzles:
        print(puzzle)
        if len(knowledge.conjuncts) == 0:
            print("    Not yet implemented.")
        else:
            for symbol in symbols:
                if model_check(knowledge, symbol):
                    print(f"    {symbol}")


if __name__ == "__main__":
    main()
