# 파일 경로 및 이름 설정
file_path = 'before.txt'

# 파일을 읽어들이고 조건에 맞게 필터링
with open(file_path, 'r', encoding='UTF-8') as file:
    lines = file.readlines()

filtered_lines = [line.strip() for line in lines if 'scroll:' not in line and 'L1_#' not in line]

# 필터링된 내용을 출력 또는 다른 작업 수행
with open('after.txt', 'w', encoding='UTF-8') as file:
    i = 0
    for line in filtered_lines:
        if line != '':
            if "VM" not in line:
                print(line + "\n")
                file.write("%%" + line + "")
                continue
            else:
                i += 1
                s = "\n!" + str(i) + ". " + ' '.join(line.split(' ')[1:])
                print(s)
                file.write(s)
                if i % 50 == 0:
                    file.write("\n영어로 번역해줘. 오직 각 라인에 있는 문장만 번역하고, 다른 라인의 문장은 참조는 하되 절대 번역하지마. (!번호. 한국어 원문 @@ 영어 번역문) 형식으로 출력해. '%%' 이후의 문자열도 빠짐없이 출력해. 각 번호 번역이 끝나면 라인마다 한 줄씩만 띄어. 문장 끝에 '.'은 생략해.\n")       
