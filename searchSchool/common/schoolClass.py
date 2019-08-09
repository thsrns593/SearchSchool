from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import pyperclip, time
import json
# 파라미터 2개 지역, 학교명 을 받았다는 가정하에 학교 리스트 출력
class SelectSH:
    def __init__(self):      #selenium을 하기위한 chromedriver 기본 옵션 적용
        path = "/opt/searchSchool/common/chromedriver"
        options = webdriver.ChromeOptions()
        options.add_argument('disable-infobars')    
        options.add_argument('headless')
        options.add_argument('window-size=1920x1080')
        options.add_argument("disable-gpu")
        options.add_argument("no-sandbox") 
        options.add_argument("disable-dev-shm-usage")
        #옵션
        options.add_argument("user-agent=Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36")
        #옵션 적용 
        self.driver = webdriver.Chrome(path, chrome_options=options)
    
        
    def searchPage(self, area_list):               #정보를 얻고자 하는 사이트 page, area_list값으로 입력 및 버튼 클릭 까지
        self.driver.get("https://www.schoolinfo.go.kr/")    #사이트 URL
        title =self.driver.find_element_by_xpath("//ul[@id='Gnb']") #공시정보 를 클릭하기 위한 틀
        title_click = title.find_element_by_xpath("//a[@href='/ei/ss/Pneiss_a01_s0.do']")# 공시정보란
        title_click.click()     #공시정보 클릭
        #metropolis = 시/도 부분의 option의 태크 이름을 전부다 가져온다.
        metropolis = self.driver.find_element_by_xpath("//select[@id='SIDO_CODE']").find_elements_by_tag_name("option")
        
        state_list = []     #시/도 리스트
    
        for g in metropolis:    #정보를 text를 사용해 읽을수 있는 정보로 반환 strip()을 사용해서 공백을 제거 
            state_list.append(g.text.strip())
            state_list.pop(0)   #0번째 정보가 시/도 여서 필요없는 정보라 pop를 통해 제거

            if area_list[0] == g.text.strip():  #area_list[0]번째 정보와 g.text.strip()과 같다면 g 클릭
                g.click()                       #area_list의 0번쨰 정보는 시/도 정보이다.
                break                           #같은게 있다면 클릭후 멈춰라 더이상찾을 이유가 없으니까
        region = self.driver.find_element_by_xpath("//select[@id='GUGUN_CODE']").find_elements_by_tag_name("option")
        #위에 metoripolis와 같다 
        region_list = []

        for g in region:    #위와 같다.
            region_list.append(g.text.strip())  #g text로 공백없이
            region_list.pop(0)
            if area_list[1] == g.text.strip():
                g.click()
                break
        
        self.driver.find_element_by_xpath("//button[@id='hgListFormSubmit']").click()    #검색버튼 클릭
        
        time.sleep(1)   #1초후에 정보를 찾기 위해 time을 걸어둔다
                        #time.sleep(1)을 걸지 않으면 자료를 정보가 화면에 나오기전에 찾기때문에 1초후에 찾을수 있도록 하게 하기 위함 

    def element(self):      #초등학교    #클릭하여 나온 정보들중 초등학교 부분만 추출 
        #초등학교 정보
        elementSchool = self.driver.find_element_by_xpath("//ul[@id='Result_List_02']").find_elements_by_tag_name("li")
        
        element_list = []   #초등학교 리스트
        #번호를 추가 하기 위해 elementSchool길이만큼 숫자 생성
        # element_numbers = [i for i in range(1, len(elementSchool) + 1)]
        
        #element_list에 elemetSchool정보를 추가 get_attribute는 data-schul-nm의 값만 추출 
        #get_attribute는 해당 태그에 있는 정보를 추출
        for x in elementSchool: #element_list 초등학교 리스트에 숫자와 get_attribute를 통해 해당 attribute의 내용을 가져온다. 
            element_list.append(x.get_attribute("data-schul-nm"))
            
        return element_list
        
    def element_click(self, selectSchoolNumber):   #초등학교 page 클릭
        self.driver.find_element_by_xpath("//ul[@id="+'"Result_List_02"' + ']/li['+ selectSchoolNumber +"]").click()
        
    def middle(self):       #중학교
        #중학교정보
        middleSchool = self.driver.find_element_by_xpath("//ul[@id='Result_List_03']").find_elements_by_tag_name("li")
        
        middle_list = []    #중학교 리스트
        
        for x in middleSchool: #middle_list 중학교 리스트에 숫자와 get_attribute를 통해 해당 attribute의 내용을 가져온다.
            middle_list.append(x.get_attribute("data-schul-nm"))
        
        return middle_list
        
    def middle_click(self, selectSchoolNumber):     #중학교 page 클릭
        self.driver.find_element_by_xpath("//ul[@id="+'"Result_List_03"' + ']/li['+ selectSchoolNumber +"]").click()

    def high(self):         #고등학교
        #고등학교정보
        highSchool = self.driver.find_element_by_xpath("//ul[@id='Result_List_04']").find_elements_by_tag_name("li")

        high_list = []      #고등학교 리스트

       
        for x in highSchool:    #high_list 고등학교 리스트에 숫자와 get_attribute를 통해 해당 attribute의 내용을 가져온다.
            high_list.append(x.get_attribute("data-schul-nm"))
            
        return high_list

    def high_click(self, selectSchoolNumber):   #고등학교 page 클릭
        self.driver.find_element_by_xpath("//ul[@id="+'"Result_List_04"' + ']/li['+ selectSchoolNumber +"]").click()

    def special(self):      #특수학교
        #특수학교정보
        specialSchool = self.driver.find_element_by_xpath("//ul[@id='Result_List_05']").find_elements_by_tag_name("li")
    
        special_list = []   #특수학교 리스트
        
        
        for x in specialSchool: #special_list 특수학교 리스트에 숫자와 get_attribute를 통해 해당 attribute의 내용을 가져온다.
            special_list.append(x.get_attribute("data-schul-nm"))
            
        return special_list

    def special_click(self, selectSchoolNumber):    #특수학교 page 클릭
        self.driver.find_element_by_xpath("//ul[@id="+'"Result_List_05"' + ']/li['+ selectSchoolNumber +"]").click()

    def choice_school(self, schoolName): #사용자가 입력한 값에 따른 초등,중등,고등,특수 학교들 정보 표출하기 위한 함수
        total_dic = {"element" : self.element(), "middle" : self.middle(), "high" : self.high(), "special" : self.special()}    
        #total_dic은 학교 리스트들을 학교 이름 의 키 값과 해당학교의 리스트가 values값으로 되어있다.
        if bool(schoolName) == False:   #파라미터 값으로 받는 학교명 값이 False이면 total_dic 반환 
            return total_dic            #boll(None) 이면 값은 False이다.
        else:
            if schoolName[-3:] == "중학교": #뒤에서 3번째까지의 이름이 중학교 이면 중학교 정보 리턴
                for x in self.middle(): #middle() 에서 리턴하는 middle_list 를 x에 대입
                    if x == schoolName: #x 값이 학교명과 같을시 해당인덱스 값을 확인하여 1값을 더해준다.
                        indexnumber = str(total_dic["middle"].index(schoolName) + 1) #middle_click() 의 파라미터는 str타입이므로 반환해준다.
                        self.middle_click(indexnumber)  #학교를 클릭하는 함수
            elif schoolName[-4:] == "초등학교":
                for x in self.element():
                    if x == schoolName:
                        indexnumber = str(total_dic["element"].index(schoolName) + 1)
                        self.element_click(indexnumber)
            elif schoolName[-4:] == "고등학교":
                for x in self.high():
                    if x == schoolName:
                        indexnumber = str(total_dic["high"].index(schoolName) + 1)
                        self.high_click(indexnumber)
            elif schoolName not in self.middle() or self.element() or self.high():  #학교이름이 초,중,고 리스트에 없다면
                for x in self.special():    #위와 같다.
                    if x == schoolName:
                        indexnumber = str(total_dic["special"].index(schoolName) + 1)
                        self.special_click(indexnumber)
    
    def student_current_situation(self):    #학생현황함수
        self.driver.find_element_by_xpath("//div[@class='School_Data2']") #파싱하고자 하는 영역의 큰틀 
        tag_name = self.driver.find_element_by_xpath("//div[@class='School_Data3']").find_element_by_tag_name("h4").text #학생현황의 이름 파싱 
        student = self.driver.find_element_by_xpath("//a[@id='chart1']").get_attribute('innerHTML') #학생수를 추출한 변수 
        
        # title = condition.get_attribute('innerHTML')
        
        # title = title.split('\n')
        student = student.split('\n')   #추출한 내용을 \n을 기준으로 나눈다.
        student_list = []   #정형화된 데이터를 담을 list
        
        for x in range(0, len(student)-1):    
            if student[x][-4:] == "<br>": #<br>tag 가 존재시 <br>을 오른쪽 <br>를 제거 하고 명을 붙여 list에 추가한다.
                student[x] = student[x].rstrip("<br>")
                student_list.append(" ".join(student[x].split()) + "명")
        
        student_dict = {}
        for g in student_list:  
            student_dict[g.split(':')[0]] = g.split(':')[1]

        return student_dict

    
    def teacher_current_situation(self):    #교직원현황함수
        self.driver.find_element_by_xpath("//div[@class='School_Data2']")   #파싱하고자 하는 영역의 큰틀
        tag_name = self.driver.find_element_by_xpath("//div[@class='School_Data3']").find_element_by_tag_name("h4").text #교직원현황의 이름 파싱
        teacher = self.driver.find_element_by_xpath("//a[@id='chart2']").get_attribute('innerHTML') #교직원수를 추출한 변수

        teacher = teacher.split('\n') #추출한 내용을 \n을 기준으로 나눈다.
        teacher_list = []   #정형화된 데이터를 담을 list
        
        for x in range(0, len(teacher)-1): 
            if teacher[x][-4:] == "<br>":   #<br>tag 가 존재시 <br>을 오른쪽 <br>를 제거 하고 명을 붙여 list에 추가한다.
                teacher[x] = teacher[x].rstrip("<br>")
                teacher_list.append(" ".join(teacher[x].split()) + "명")
        
        teacher_dict = {}
        for g in teacher_list:
            teacher_dict[g.split(':')[0]] = g.split(':')[1]
        
        return teacher_dict

    def after_school_current_situation(self):   #방과후학교 운영함수
        div_list = self.driver.find_element_by_xpath("//div[@class='School_Data2']").find_elements_by_xpath("//div[@class='DataBox']") #파싱하고자 하는 영역의 큰틀
        tag_name = div_list[2].find_element_by_tag_name("h2").text #방과후학교 이름 파싱
        after_school = div_list[2].find_element_by_tag_name("ul").find_elements_by_tag_name("li") #방과후학교 프로그램과 참여학생수를 추출한 변수

        after_school_dict = {}
        count = 1

        for x in after_school:  #추출한 정보를 count 변수를 통해 이름에 맞게 개, 명 추가 
            if count == 1:
                after_school_dict[x.text.split('\n')[0]] = x.text.split('\n')[1] + "개"
                count += 1
            else:
                after_school_dict[x.text.split('\n')[0]] = x.text.split('\n')[1] + "명"
                
        return after_school_dict
    
    def school_meals_current_situation(self):   #급식실시현황 함수
        div_list = self.driver.find_element_by_xpath("//div[@class='School_Data2']").find_elements_by_xpath("//div[@class='DataBox']") #파싱하고자 하는 영역의 큰틀
        tag_name = div_list[3].find_element_by_tag_name("h2").text #급식실시 이름 파싱
        school_meals = div_list[3].find_element_by_tag_name("ul").find_elements_by_tag_name("li") #급식실시안에 정보를 추출한 변수
        
        school_meal_dict = {}
        for x in school_meals:     #추출한 정보를 이름에 맞게 원, 명 추가
            if x.text.split('\n')[0][-1] == "수":
                school_meal_dict[x.text.split('\n')[0]] = x.text.split('\n')[1] + "명"
                # school_meal_list.append(x.text.replace("\n", " : ") + "명") 
            elif x.text.split('\n')[0][-1] == "액":
                school_meal_dict[x.text.split('\n')[0]] = x.text.split('\n')[1] + "원"
                # school_meal_list.append(x.text.replace("\n", " : ") + "원")     
            else:
                school_meal_dict[x.text.split('\n')[0]] = x.text.split('\n')[1]
                # school_meal_list.append(x.text.replace("\n", " : "))
        return school_meal_dict
    
    def school_library_current_situation(self): #학교도서관현황 함수
        div_list = self.driver.find_element_by_xpath("//div[@class='School_Data2']").find_elements_by_xpath("//div[@class='DataBox']") #파싱하고자 하는 영역의 큰틀
        tag_name = div_list[4].find_element_by_tag_name("h2").text  #학교도서관 이름 파싱
        school_library = div_list[4].find_element_by_tag_name("ul").find_elements_by_tag_name("li") #학교도서관안에 정보를 추출한 변수
       
        school_library_dict = {}
        for x in school_library:    #추출한 정보를 이름에 맞게 권 추가
            # school_library_list.append(x.text.replace("\n", " : ") + "권")
            school_library_dict[x.text.split('\n')[0]] = x.text.split('\n')[1] + "권"
        
        return school_library_dict

    def student_parents_counseling_performance(self):   #학생/학부모 상담 실적 함수
        div_list = self.driver.find_element_by_xpath("//div[@class='School_Data2']").find_elements_by_xpath("//div[@class='DataBox']") #파싱하고자 하는 영역의 큰틀
        tag_name = div_list[5].find_element_by_tag_name("h2").text  #학생/학부모상담 이름 파싱
        counseling_performance = div_list[5].find_element_by_tag_name("ul").find_elements_by_tag_name("li") #학생/학부모상담 안에 정보를 추출한 변수
        
        counseling_performance_dict = {}
        
        for x in counseling_performance:    #추출한 정보를 이름에 맞게 명 추가
            counseling_performance_dict[x.text.split('\n')[0]] = x.text.split('\n')[1] + "명"
        
        return counseling_performance_dict
    def total_current_situation(self):      #학생,교직원,방과후 학교,급식실시,학교도서관,학생/학부모상담 의 정보를 모아주는 함수
        total_situation_dic = {"student" : self.student_current_situation(), "teacher" : self.teacher_current_situation(), 
        "after" : self.after_school_current_situation(), "school_meals" : self.school_meals_current_situation(), 
        "school_library" : self.school_library_current_situation(), "student_parents" : self.student_parents_counseling_performance()}
        self.driver.close()
        #
        return total_situation_dic
        
    def findData(self): #사용자가 입력한 학교 page로 이동하여 정보를 찾는 함수
        # title = self.driver.find_element_by_xpath("//h1[@class='NameArea']")
        school_name = self.driver.find_element_by_xpath("//span[@style='position:relative; top:3px']") #파싱하고자 정보의 틀 
        # print(school_name.text)
        school_Data = self.driver.find_element_by_xpath("//ul[@class='School_Data']").find_elements_by_xpath("li") #틀 안에 정보를 담는 변수
        
        Data_dict = {}
        
        for x in school_Data:   #담은 정보를 딕셔너리 형태로 저장 
            Data_dict[x.text.split('\n')[0]] = x.text.split('\n')[1]
        
        return Data_dict
        
    def data_worker(self, region_data, schoolName): #전체적인 동작을 담당하는 함수
        self.searchPage(region_data)    #입력받은 지역page로 이동
        self.choice_school(schoolName)  #입력받은 학교로 이동 
        result = self.findData()        #파싱한 학교정보 담는 함수
        result["학교이름"] = schoolName  #학교이름 추가 
        #self.driver.close()

        return result
