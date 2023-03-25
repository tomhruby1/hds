# BUILD RULES DICT
import json

V = ['i', 'e', 'a', 'o', 'u', 'I', 'A', 'O', 'U', 'y', 'Y', 'F'] #samohlasky
K = ['f', 'v', 's', 'z', 'S', 'Z', 'x', 'h', 'l', 'r', 'R', 'j', 'p', 'b', 't', 'd', 'T', 'D', 'k', 'g', 
     'm','n', 'J', 'c', 'C', 'w', 'W', 'N', 'M', 'G', 'Q', 'P', 'L', 'H'] #souhlasky
# parove korespondence
ZPK = ['b','d', 'D', 'g', 'v', 'z', 'Z', 'h', 'w', 'W', 'R']    #znele parove souhlasky
NPK = ['p','t', 'T', 'k', 'f', 's', 'S', 'X', 'c', 'C', 'Q']    #neznele parove souhlasky
JK  = ['m', 'n', 'J', 'l', 'r', 'j']    #jedinecne souhlasky 

NP = ['k', 's', 'v', 'z'] #neslabicne predlozky
JPZ = ['bez', 'nad', 'ob', 'od', 'pod', 'pRed'] #jednoslab. predlozky


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
    '_n+e_': 'Je',
    '_m+ě_': 'mJe'
}

# TODO: zanedbani 2.19, 2.23 a 2.24 !!?

# vyslovnost samohlasek v okolí pauzy -- po libovolne pauze raz pred samohlasku
rules[4] = {
    '#,#+|_$V_': '!*', # asterisk --the og char 
}


# --- SECOND OPERATIONS USING FONETIC UNITS ---
# 2.26, ignoruju prefixovy predel
# TODO: dodat !
# spodoba (asimilace) znelosti
rules[5] = {
    # vyjimky
    #'_v_$NPK':'f',
    # main stuff
    '_$ZPK_$NPK,|+$NPK,|+$JK,|+$V,|+#' : '$~ZPK', 
    '_$NPK_$ZPK,|+$ZPK': '$~NPK'
}

with open('rules2.json', 'w', encoding='UTF-8') as f:
    json.dump(rules, f )
