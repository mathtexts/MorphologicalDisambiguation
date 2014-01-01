
#import pymorphy
import re
import os
import xml.etree.ElementTree
#import pymorphy.utils
import xml.dom.minidom



#from pymorphy import get_morph

class word_morph:
    word = "word"
    morph = "word"
    #speech = "noun"
    word_attr = []

class main_word:
    morph = ""
    word_attr = []
    next_word = []
    count = 1
    prob = 0.0

class child_word:
    morph = ""
    word_attr = []
    count = 1
    prob = 0.0

class pymorphy_gen_morph:
    morph = ""
    word_attr = []
    prob_next = 0.0
    prob_word = 0.0

class pymorphy_word:
    word = ""
    parse_var = []



START_COUNT = 35

speech_all = {"ADVB", "CONJ", "NUMR", "INTJ", "ADJS", "PRED", "PRTS",
"GRND", "ADJF", "COMP", "ADVB", "INFN", "VERB", "NOUN"}


mystem_dir = "mystem\\mystem.exe"

pymorphy_dir = "pymorphy\\dictionary"

output_file = "mystem\\out.txt"
input_file = "mystem\\in.txt"


MAX_COUNT = 100000
LEARN_KOEFF = 0.9

def gen_check_py(tmp_word = word_morph()):

    morph = pymorphy.get_morph(pymorphy_dir)
    try:
        #check_result_py = morph.normalize(str(tmp_word.word))
        gr_info = morph.get_graminfo(str(tmp_word.word).upper())
        #print("word  = ", str(wordInfo.word), "norm = ", pymorphy_result, "morph = ", wordInfo.morph.lower())
        if tmp_word.morph.lower() == check_result_py.lower():
            return True
        else:
            return False
    except TypeError:
        return False

def cor_par(path_to_corpus = "corpus.xml"):

    words = xml.etree.ElementTree.parse(path_to_corpus).findall(".//token")
    word_list_all = []
    word_all = []
    corpus_for_pymorphy2 = open ("corpus_for_pymorphy2_full.txt", "w")
    i = 0
    j = 0
    #print("size = ", words.__len__())
    while (j < words.__len__()):
        word = words[j]
        speech = word.find('tfr').find('v').find('l').find('g').attrib['v']
        #test2 = word.find('tfr').find('v').find('l').find('g').find('v').find('g').attrib['v']
        if (speech_all.__contains__(speech)):
            test1 = word.find('tfr').find('v').find('l')
            test11 = test1.findall("g")
            #print("corpus ")
            for t in test11:
                #print(t.attrib['v'])
                if (not (word_all.__contains__(t.attrib['v']))):
                    word_all.append(t.attrib['v'])
            tmp_word = word_morph()
            tmp_word.word_attr = []
            tmp_word.word = word.attrib['text']

            #tmp_word.speech = speech
            for t in test11:
                tmp_word.word_attr.append(t.attrib['v'])
            #print("list ")
            #for word in tmp_word.word_attr:
                #print(word)
            tmp_word.morph = word.find('tfr').find('v').find('l').attrib['t']
            word_list_all.append(tmp_word)
            #tmp_word.word_attr = []
            i = i + 1
        if i > MAX_COUNT:
            break
        j = j + 1

    word_count = word_list_all.__len__()
    i = 0
    j = 0
    while( i < word_list_all.__len__()):
        #tmp_morph = morph.parse(unicode(corpus[i]))
        #corpus_for_pymorphy2.write(word_list_all[i].word)
        #corpus_for_pymorphy2.write('\n')
        i += 1
        j += 1
    print(j)

    corpus_for_pymorphy2.close()

    print("corpus word count = ", j, "needed word count = ", i)
    #result_word_list = []
    #j = 0
    #while (j < word_list_all.__len__()):
    #    temp_word = word_list_all[j]
    #    if (speech_all.__contains__(temp_word.word_attr[0])):
    #        result_word_list.append(temp_word)
    #    j = j + 1

    word_all_f = open("word_all_corpus.txt", "w")
    for word in word_all:
        word_all_f.write(word)
        word_all_f.write('\n')
    word_all_f.close()

    #return result_word_list
    return word_list_all




def pymorphy_part(corpus):
    count = 0
    good_count = 0
    i = 0
    while (i < corpus.__len__()):
        tmp = corpus[i]
        if gen_check_py(tmp):
            good_count = good_count + 1
        count = count + 1
        i = i + 1

    print("Pymorphy")
    print("cheking words count = ", str(count), "\n", "morphs = ", str(good_count))

def check_main_list(word_attr, main_word_list):
    result = TRUE

    for word in main_word_list:
        if (word.word_attr == word_attr):
            result = FALSE
    return result

def learn(corpus):
    word_count = int(corpus.__len__() * LEARN_KOEFF)
    i = 0
    main_word_list = []
    while ( i < word_count-1):
        #tmp_word = main_word()
        #tmp_word.morph = corpus[i].morph
        #tmp_word.word_attr = corpus[i].word_attr

        tmp_attr = corpus[i].word_attr

        result = 1
        word_num = 0
        for word in main_word_list:
            if (word.word_attr == tmp_attr):
                result = 0
                break;
            word_num += 1

        if (result):
            tmp_word = main_word()
            tmp_word.morph = corpus[i].morph
            tmp_word.word_attr = corpus[i].word_attr
            #tmp_word.count = 1
            main_word_list.append(tmp_word)
        else:
            main_word_list[word_num].count += 1
            word_num2 = 0
            result2 = 1
            for word in main_word_list[word_num].next_word:
                if (word.word_attr == corpus[i+1].word_attr):
                    result2 = 0
                    break;
                word_num2 += 1
            if (result2):
                ch_word = child_word()
                ch_word.morph = corpus[i+1].morph
                ch_word.word_attr = corpus[i+1].word_attr
                main_word_list[word_num].next_word.append(ch_word)
            else:
                main_word_list[word_num].next_word[word_num2].count += 1

        i += 1

    #probability count
    model = open("model.txt", "w")
    i = 0
    while (i < main_word_list.__len__()):
        main_word_list[i].prob = main_word_list[i].count / word_count
        model.write("(")
        for word in main_word_list[i].word_attr:
            model.write(word)
            model.write(" ")
        model.write(")")
        model.write(" probability = ")
        model.write(str(main_word_list[i].prob))
        model.write('\n')
        j = 0
        tmp_main_word_count = 0
        for word in main_word_list[i].next_word:
            tmp_main_word_count += word.count
        while (j < main_word_list[i].next_word.__len__()):
            main_word_list[i].next_word[j].prob = main_word_list[i].next_word[j].count / tmp_main_word_count
            model.write("(")
            for word in main_word_list[i].word_attr:
                model.write(word)
                model.write(" ")
            model.write(")")
            model.write(" ----> ")
            model.write("(")
            for word in main_word_list[i].next_word[j].word_attr:
                model.write(word)
                model.write(" ")
            model.write(")")
            model.write(" probability = ")
            model.write(str(main_word_list[i].next_word[j].prob))
            model.write('\n')
            j += 1

        i += 1

    model.close()

    return main_word_list

def test(model, corpus, pymorphy_main_list):

    test_result = []
    #word_count = int(corpus.__len__() * (1 - LEARN_KOEFF))
    #pymorphy all test words
    #first_word = corpus[corpus.__len__() - word_count + 1]
    #pymorphy_main_list = []
    #i = corpus.__len__() - word_count + 1
    #i = 0
    #while ( i < pymorphy_corpus.__len__()):
    #    first_word = pymorphy_corpus[i]
    #    pym_word = pymorphy_word()
    #    pym_word.word = first_word.word
    #    pym_gen_morph = pymorphy_gen_morph()
        #pymorphy genereted morph
    #    pym_gen_morph.morph = ""
    #    pym_gen_morph.word_attr = first_word.word_attr
    #    pym_word.parse_var.append(pym_gen_morph)
    #    pymorphy_main_list.append(pym_word)
    #    i += 1

    print("OK")

    i = 0
    #for morph_var in pymorphy_main_list[0].parse_var:
    while ( i < pymorphy_main_list[0].parse_var.__len__()):
        for word in model:
            if (word.word_attr == pymorphy_main_list[0].parse_var[i].word_attr):
                pymorphy_main_list[0].parse_var[i].prob_word = word.prob
                for ch_word in word.next_word:
                    j = 0
                    while(j < pymorphy_main_list[1].parse_var.__len__()):
                        if (ch_word.word_attr == pymorphy_main_list[1].parse_var[j].word_attr):
                            pymorphy_main_list[1].parse_var[j].prob_next = ch_word.prob
                        j += 1
        i += 1

    max_val = 0.0
    i = j = 0
    mi = mj = 0
    for word in pymorphy_main_list[0].parse_var:
        #tmp_max = word.prob_word
        for ch_word in pymorphy_main_list[1].parse_var:
            tmp_max = word.prob_word * ch_word.prob_word * ch_word.prob_next
            if (tmp_max > max_val):
                max_val = tmp_max
                mi = i
                mj = j
            j += 1
        i += 1
    test_result.append(pymorphy_main_list[0].parse_var[mi])
    test_result.append(pymorphy_main_list[1].parse_var[mj])

    i = 1
    curr_index = mj
    while ( i < pymorphy_main_list.__len__() - 1):
        for word in model:
            if(word.word_attr == pymorphy_main_list[i].parse_var[curr_index].word_attr):
                pymorphy_main_list[i].parse_var[curr_index].prob_word = word.prob
                for ch_word in word.next_word:
                    j = 0
                    while( j < pymorphy_main_list[i+1].parse_var.__len__()):
                        if (ch_word.word_attr == pymorphy_main_list[i+1].parse_var[j]):
                            for word_prob in model:
                                if(word_prob.word_attr == pymorphy_main_list[i+1].parse_var[j].word_attr):
                                    pymorphy_main_list[i+1].parse_var[j].prob_word = word_prob.prob
                            pymorphy_main_list[i+1].parse_var[j].prob_next = ch_word.prob
                        j += 1

        max_val = 0.0
        k = 0
        curr_index = 0
        for word in pymorphy_main_list[i+1].parse_var:

            tmp_max = word.prob_word * word.prob_next
            #for ch_word in pymorphy_main_list[1].parse_var:
            if (tmp_max > max_val):
                max_val = tmp_max
                curr_index = k
            k += 1

        test_result.append(pymorphy_main_list[i+1].parse_var[curr_index])


        i += 1
   
        
    print("OK")
    for word in test_result:
        print(word.morph)
        for tag in word.word_attr:
            print("   ", tag)
    return test_result



def test_result(corpus_part, pymorphy_part):
    word_count = int(corpus_part.__len__() * (1 - LEARN_KOEFF))
    i = 0
    good_count = 0
    count = START_COUNT

    while( i < pymorphy_part.__len__() - 1):
        print(corpus_part[i + corpus_part.__len__() - word_count].word, " ", pymorphy_part[i].morph)
        if( corpus_part[i + corpus_part.__len__() - word_count].word_attr == pymorphy_part[i].word_attr):
            good_count += 1
        count += 1
        i += 1
    print("Result = ", good_count/count)


def parse_pymorphy2():
    f = open("morph_parse4.txt", "r")
    main_word_list = []
    pymorphy2_words = f.read()
    words = pymorphy2_words.split('\n')
    main_w = pymorphy_word()
    first_word = 1
    i = 0
    j = 0
    #word = words[0].split("=")
    for word in words:
        word = word.split('=')
        if( word[0] == "word"):
            print(word[1])
            if (not first_word):
                main_word_list.append(main_w)
            first_word = 0
            main_w = pymorphy_word()
            main_w.word = word[1]
            main_w.parse_var = []
            i = 0
        if( word[0] == "morph"):
            print(word[1])
            pgm = pymorphy_gen_morph()
            pgm.morph = word[1]
            main_w.parse_var.append(pgm)
        if( word[0] == "tag"):
            print(word[1])
            tag = word[1].split(",")
            main_w.parse_var[i].word_attr = []
            for tattr in tag:
                attr1 = tattr.split(' ')
                for attr in attr1:
                    main_w.parse_var[i].word_attr.append(attr)
            i += 1

    main_word_list.append(main_w)

    return main_word_list












corpus = cor_par()
model = learn(corpus)
pymorphy_corpus = parse_pymorphy2()
result = test(model, corpus, pymorphy_corpus)
#test_result(corpus, result)


print("OK")










