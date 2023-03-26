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
# á -> A ...
rules[0] = {
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
# hacky a carky ^ uz nepouzivany nize
# #basic
rules[1] = {
    '_c+h_': 'x',
    '_ů_': 'U',
    '_y_': 'i',
    '_ý_': 'í',

}
# spojeni samohlasek
rules[2] = {
    '_o+u_': 'y',
    '_a+u_': 'Y',
    '_e+u_': 'F',
}
# spojeni samohlasky a souhlasky
# TODO: doplneni razu na konec? -- skupiny slov jako samohlasky definovat promenou string s $
rules[3] = {
    'b,p,v_ě_': 'je', #bě pě vě
    
    '_d_i,I': 'D',        #di ti ni
    '_t_i,I': 'T',
    '_n_i,I': 'J',

    '_d+ě_': 'De',
    '_t+ě_': 'Te',
    '_n+ě_': 'Je',
    '_m+ě_': 'mJe'
}

# TODO: zanedbani 2.19, 2.23 a 2.24 !!?

# vyslovnost samohlasek v okolí pauzy -- po libovolne pauze raz pred samohlasku
rules[4] = {
    '#,#+|_$V_': '!*', # asterisk --the og char 
}

# --- 2.26: spodoba (asimilace) znelosti ---  
# zde prace uz s fonet. znaky
# ignoruju prefixovy predel
# vyjimky rules[6] ... musi byt tady TODO: txt se zatim naupdatuje uvnitr rulesetu 
#       ... mozna dobre ruleset by mel byt vylucny?
rules[6] = {
    #'_v_$NPK':'f', #asi funguje i bez
    '_$NPK_v,|+v': '*',
    '_$ZPK_|+v': '$~ZPK', # 2.28.3 ... v specialita
    '$NPK_R_': 'Q',
}
rules[7] = {
    # main stuff
    '_$ZPK_$NPK,|+$NPK,|+$JK,|+$V,|+#' : '$~ZPK', 
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
rules[8] = {
    '$K_r_$K,|': 'P',
    '$K_l_$K,|': 'L',
    '$K_m_$Krl,|': 'H'
}

# zjednodussena vyslovnost souhlaskovych skupin
rules[9] = {
    '_z+S+T+I_': 'STI'
}

with open('rules.json', 'w', encoding='UTF-8') as f:
    json.dump(rules, f )

print("Rules saved.")