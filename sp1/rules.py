# BUILD RULES DICT
import json

V = ['i', 'e', 'a', 'o', 'u', 'I', 'A', 'O', 'U', 'y', 'Y', 'F'] #samohlasky
K = ['f', 'v', 's', 'z', 'S', 'Z', 'x', 'h', 'l', 'r', 'R', 'j', 'p', 'b', 't', 'd', 'T', 'D', 'k', 'g', 
     'm','n', 'J', 'c', 'C', 'w', 'W', 'N', 'M', 'G', 'Q', 'P', 'L', 'H'] #souhlasky
K_rl = ['f', 'v', 's', 'z', 'S', 'Z', 'x', 'h', 'R', 'j', 'p', 'b', 't', 
        'd', 'T', 'D', 'k', 'g', 'm','n', 'J', 'c', 'C', 'w', 'W', 'N', 'M', 'G', 'Q', 'H'] #souhlasky bez r a l, a jejich slabikotvor. variant
# souhlasky, parove korespondence
ZPK = ['b','d', 'D', 'g', 'v', 'z', 'Z', 'h', 'w', 'W', 'R']    #znele parove souhlasky
NPK = ['p','t', 'T', 'k', 'f', 's', 'S', 'x', 'c', 'C', 'Q']    #neznele parove souhlasky
JK  = ['m', 'n', 'J', 'l', 'r', 'j']    #jedinecne souhlasky 
# predlozky 
NP = ['k', 's', 'v', 'z'] #neslabicne
JPZ = ['bez', 'nad', 'ob', 'od', 'pod', 'pRed'] #jednoslab.


# --- FIRST TRANSLATE TO FONETIC UNITS ---
 # aplikace po pravidlech s y a ý
rules = {}
# spojeni samohlasky a souhlasky
# TODO: doplneni razu na konec? -- skupiny slov jako samohlasky definovat promenou string s $
rules[0] = {
    'b,p,v_ě_': 'je', #bě pě vě
    
    '_d_i,í': 'D',        #di ti ni
    '_t_i,í': 'T',
    '_n_i,í': 'J',

    '_d+ě_': 'De',
    '_t+ě_': 'Te',
    '_n+ě_': 'Je',
    '_m+ě_': 'mJe'
}

# likvidace i/y az po predchozich pravidlech
rules[1] = {
    '_c+h_': 'x',
    '_ů_': 'U',
    '_y_': 'i',
    '_ý_': 'í',
}

# á -> A ... po tehle skupine pravidel uz prace s fonetickymi znaky
rules[2] = {
    '_í_':'I',
    '_é_':'E',
    '_á_':'A',
    '_ó_':'O',
    '_ú_':'U',
    '_š_':'S',
    '_ž_':'Z',
    '_ř_':'R',
    '_ť_':'T',
    '_ď_':'D',
    '_ň_':'J',
    '_č_':'C'
}


# spojeni samohlasek
rules[3] = {
    '_o+u_': 'y',
    '_a+u_': 'Y',
    '_e+u_': 'F',
}

# vyslovnost samohlasek v okolí pauzy -- po libovolne pauze raz pred samohlasku
rules[4] = {
    '$V+|_$V_': '!*',
    '$K+|_$V_': '!*',   #2.23, zanedbani '-'
    '_$ZPK_|+$V,|+!+$V': '$~ZPK', #jediny pravidlo, kdy len(ctx) > 2 
    #2.24 - neslab predlozky 
    '|+$NP+|_$V_': '!*',
    #2.25
    '#,#+|_$V_': '!*',
}

# --- 2.26: spodoba (asimilace) znelosti ---  
# zde prace uz s fonet. znaky
# ignoruju prefixovy predel
# vyjimky rules[6] ... musi byt tady TODO: txt se zatim naupdatuje uvnitr rulesetu 
#       ... mozna dobre ruleset by mel byt vylucny?
# rules[7] = {
#     #'_v_$NPK':'f', #asi funguje i bez
#     '_$NPK_v,|+v': '*',
#     '_$ZPK_|+v': '$~ZPK', # 2.28.3 ... v specialita
#     '$NPK_R_': 'Q',
#     '_x_|': 'G' # ch -> znele ch [G] na hranici slov
# }

# TODO: bRetstavenstvo proto znele Q pred rules 7 
rules[7] = {
    '$NPK_R_': 'Q',
    '_x_|': 'G', # ch -> znele ch [G] na hranici slov
}

rules[8] = {
    # spodoba znelosti vyjimky
    '_$NPK_v,|+v': '*',
    '_$ZPK_|+v': '$~ZPK', # 2.28.3 ... v specialita

    # main stuff
    '_$ZPK_$NPK,|+$NPK,|+$JK,|+$V,|+#,|+!' : '$~ZPK', 
    '_$NPK_$ZPK,|+$ZPK': '$~NPK' # 
}
# TODO prefixovy sev '-'

# --- 2.33... asimilace artikulacni ----
# TODO: pro 'nadseni' musi byt pred 6?
rules[5] = {
    '_n_k,g': 'N',
    '_m_v,f': 'M',
    # 2.35 zanedbano
    '_n_T,D': 'J', # volim zmekceni u 2.36
    #'_t+|+s_': 'ts', # hmmm?
    '_t+s_': 'c', # nespisovne jenom na hranici slov? -- nebo v miste slozeni slova?
    '_t+S_': 'C',
}
# slabikotvorne souhlasky 
rules[9] = {
    '$K_r_$K,|': 'P',
    '$K_l_$K,|': 'L',
    '$K_m_$Krl,|': 'H'
}

# zjednodussena vyslovnost souhlaskovych skupin
# TODO: applikace s poradim 6?? nerozbije neco dulezitejsiho??
rules[6] = {
    # 2.41
    '_z+S+T+I_|': 'STI', 
    '_Z+S+T+I_|': 'STI',
    # 2.42 vynecháno
    'z_d_n,N': '',
    # 2.44 vynecháno
    # tcera -> cera
}

# TODO: na tohle nejsou moje pravidla ready :(
# vyslovnost dvou stejnych fonetickych jednotek
# rules[10] = {
#     '_*+*_': '*', # le co vnitrni predel -- asi prostě akceptuju nespisovnost
# }

# slova - speciality 
rules[11] = {
    # byti -> odstranit 'j'
    '|_j_s+m+e': '',
    '|_j_s+e+m': '',
    '|_j_s+i': '',
    # dcera a slova odvozena
    '|_d_c+e': '',
    # srdce 
    's+r_d_c': '',
}

if __name__=='__main__':
    with open('rules.json', 'w', encoding='UTF-8') as f:
        json.dump(rules, f )
    print("Rules saved.")