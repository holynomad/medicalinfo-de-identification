# 특정 폴더의 검사결과 파일(xml)에서 의료(민감)정보 필드를 가명처리 @ 2021.03.09.
# ref & thx to : https://skkim1080.tistory.com/entry/Python%EC%9C%BC%EB%A1%9C-xml-%ED%8C%8C%EC%9D%BC-%EB%82%B4%EC%9A%A9-%EC%88%98%EC%A0%95%ED%95%98%EA%B8%B0

import os
import xml.etree.ElementTree as ET

targetDir = r"InputYourXMLFolder"
num = 1

# targetDir에서 .xml파일 이름들 리스트로 가져오기
file_list = os.listdir(targetDir)
xml_list = []

for file in file_list:
    if '.xml' in file:
        xml_list.append(file)

# 모든 .xml파일에 대해 수정
for xml_file in xml_list:
    
    replaceFailCnt = 0   

    target_path = targetDir + "\\" + xml_file
    targetXML = open(target_path, 'rt', encoding='UTF8')

    tree = ET.parse(targetXML)

    root = tree.getroot()

    # 수정할 부분 (PatInfoID)
    successYn = True
    target_tag = root.find("PatientInfo/ID")

    # 일괄치환
    try:
        target_tag.text = "IDisDeidentified"
    except AttributeError:
        print("AttributeError : " + str(target_tag)) 
        successYn = False
        replaceFailCnt += 1

    # logging 
    if successYn:
        print("[" + str(num) + "]" + xml_file + " > " + str(target_tag.tag) + " > " + "[success]")
    else:
        print("[" + str(num) + "]" + xml_file + " > " + str(target_tag.tag) + " > " + "[failed...]")
    
    # 수정할 부분 (PatInfo 풀네임)
    successYn = True
    target_tag = root.find("PatientInfo/Name/Full")

    # 일괄치환
    try:
        target_tag.text = ""
    except AttributeError:
        print("AttributeError : " + str(target_tag)) 
        successYn = False
        replaceFailCnt += 1

    # logging (환자 풀네임)
    if successYn:
        print("[" + str(num) + "]" + xml_file + " > " + str(target_tag.tag) + " > " + "[success]")
    else:
        print("[" + str(num) + "]" + xml_file + " > " + str(target_tag.tag) + " > " + "[failed...]")



    if replaceFailCnt == 0:
        tree.write(target_path.replace('.xml', '_deidentified.xml'))
    else:
        print("target_path is not de-identified (failcount = " + str(replaceFailCnt) + ")")        

    num += 1

print("process is finished.")