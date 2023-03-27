import json
import sys
from rules import V,K,K_rl,ZPK,NPK,JK,NP,JPZ

def get_var(s):
    if s[0] != '$': return
    varname = s[1:]
    if varname == 'ZPK':
        return ZPK
    elif varname == 'NPK':
        return NPK
    elif varname == 'JK':
        return JK
    elif varname == 'V':
        return V
    elif varname == 'K':
        return K
    elif varname == 'Krl':
        return K_rl
    elif varname == 'NP':
        return NP
    elif varname == 'JPZ':
        return JPZ
    else:
        raise Exception(f'Unknown variable {s}')

def get_result(result, char):
    '''args:
        - result: output of the applied rule
        - char: character in question
    '''
    if result.startswith('$'):
        #ZPK x NPK --> return from the other one based on corresponding idx
        if result[1] == '~': 
            if char in ZPK: 
                return NPK[ZPK.index(char)]
            if char in NPK:
                return ZPK[NPK.index(char)]
    if '*' in result:
        return result.replace('*', char)
    # else plain result
    return result

def match_char(ident, target):
    ''' if len(ident) != len(target) returns True if first n-chars of ident match target'''
    if ident.startswith('$'):
        ident = get_var(ident)
    if target in ident:
        return True
    if ident == '#' and target == '$':    # bad hacking to cover $ by #
        return True
    return False

def match_identifier(ident, txt):
    '''matches identifer (left, right, center)'''
    #print(f"matching ident {ident} with text {txt}")
    for j, subident in enumerate(ident.split(',')): #OR
        #over one or two char identifiers connected with
        #should check only one char when len(char_ident) == 1
        all_good = True
        for k, char_ident in enumerate(subident.split('+')): #AND
            if not match_char(char_ident, txt[k]):
                all_good = False
                break
        if all_good: return True
    return False

ctx_size = 3 #left and right maximum context size

def transcribe(sent:str, rules:dict):
    ''' transcribing sentence according to given rules'''
    
    if DEBUG: print(sent)
    # preprocessing na urovni vety 
    sent = sent.lower()
    sent = sent.replace(' ', '|')
    sent = sent.replace(',', '|#')
    sent = sent.split('.')[0]
    sent = "|$|"+sent+"|$|"
    if DEBUG: print(sent)

    txt_out = sent
    for rs_id, ruleset in sorted(rules.items()):
        txt = txt_out[::-1] #reverse, use already translated sequence for the next ruleset application
        txt_out = ""
        i = 0
        while i < len(txt):
            out = txt[i] # default result --> copy original character 
            core_size = 1
            ## find a rule to apply for char[i] and it's left and right context
            for cond, result in ruleset.items():
                idents = cond.split('_')
                # if the main string - core matched -- check context
                # only one option expected for core, context can have mutliple comma seperated vals
                # multiple chars -- connected by '+'
                ctx_size_L = min(len(idents[0].split('+')), ctx_size)
                ctx_size_R = min(len(idents[2].split('+')), ctx_size)
                core_size = len(idents[1].split('+'))
                core = txt[i:i+core_size][::-1] # core string 
                left = txt[i+core_size:i+core_size+ctx_size_L][::-1] # left context
                right = txt[max(0,i-ctx_size_R):i][::-1] # right context
                i_step = 1
                if match_identifier(idents[1], core):
                    #if DEBUG: print(f"char matched {idents[1]}: {core}, condition: {cond}")
                    # context check ... if specified it has to pass
                    if idents[2] != '':
                        if not match_identifier(idents[2], right):
                            continue
                    if idents[0] != '':
                        if not match_identifier(idents[0], left):
                            continue
                    # all conditions met here 
                    if DEBUG: print(f"using rule: {idents[0]}_{idents[1]}_{idents[2]}: {core} -> {result}")
                    out = get_result(result, core)
                    i_step = core_size
                    break  # apply always only one rule from given ruleset per [i] position 
            txt_out = out + txt_out
            i += i_step 
        if DEBUG: print(f"{rs_id}: {txt_out}")
    return txt_out

DEBUG = True

if __name__=="__main__":
    # transcribe input file
    with open('rules.json', 'r', encoding='UTF-8') as f:
        rules = json.load(f)

    if len(sys.argv) > 1:
        p = sys.argv[1]
        print(f"loading input text from {p}")
        with open(p, 'r') as f:
            in_txt = f.readlines()
        out_txt = []
        for sent in in_txt:
            out_txt.append(transcribe(sent, rules))
        # write result
        out_p = "vety_HDS.phntrn.txt"
        if len(sys.argv) > 2:
            out_p = sys.argv[2]
        with open(out_p, 'w') as f:
            f.writelines(l + '\n' for l in out_txt)

    # run test set
    # with open('test.json', 'r') as f:
    #     test_set = json.load(f)

    # correct = 0
    # for x,y in test_set.items():
    #     y_hat = transcribe(x, rules)
    #     if y_hat == y:
    #         correct += 1
    #     else:
    #         print(f"wrong prediction: {x} -> {y_hat}, correct is: {y}")
    # print(f"total correct {correct}/{len(test_set)}")

    # y = transcribe("zvěř chodí", rules) 
    # y = transcribe("přítel", rules)
    # y = transcribe("nashledanou", rules)
    # y = transcribe("pět švestek", rules) #ahh rule 6.2 -- aplikuje se i kdyz by nemusel?
    # y = transcribe("hrob", rules)
    # y = transcribe("francouzští", rules)
    # y = transcribe('pražští', rules)
    # y = transcribe('bez únavy', rules)
    y = transcribe('od reformního', rules)
    print(f"result: {y}")