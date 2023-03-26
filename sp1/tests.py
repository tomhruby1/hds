from rules import V,K,K_rl,ZPK,JK,NP,JPZ
from phonetic_transcription import match_identifier

DEBUG = False

def match_identifier_test():
    # correct mapping ident -> target text
    test_set_true = {
        '$ZPK+a': ZPK[0]+'a',
        'm+ě': 'mě'
    } 
    
    test_set_false = {
        '$ZPK+a': NPK[0]+'a',
        'm+ě': 'mje'
    }
    
    N = 0
    result_true = {}
    TP = 0
    for ident, target in test_set_true.items():
        result_true[ident] = match_identifier(ident, target)
        if result_true[ident] == True:
            TP += 1
        if DEBUG: print(f"identifier: {ident}, text: {target}, predicted: {result_true[ident]}")
        N += 1

    result_false = {}
    TN = 0
    for ident, target in test_set_false.items():
        result_false[ident] = match_identifier(ident, target)
        if result_false[ident] == False:
            TN += 1
        if DEBUG: print(f"identifier: {ident}, text: {target}, predicted: {result_false[ident]}")
        N += 1


    correct = TP + TN
    print(f"correct: {correct} / {N}")
    print(f"TP: {TP}, TN: {TN}")


if __name__=='__main__':
    match_identifier_test()