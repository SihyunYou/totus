with open('temp.txt', 'r', encoding='utf-8') as file1:
    with open('translate.txt' ,'w', encoding='utf-8') as file2:
        s = file1.readlines()
        for t in s:
            if '@@' in t and '영어로 번역해줘' not in t:
                file2.write(t + '\n')
            