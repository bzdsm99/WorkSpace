from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium import webdriver
from io import BytesIO
from PIL import Image
import ddddocr
import requests
import time




html = "https://urp.tfswufe.edu.cn/cas/login?"
login_html = "https://urp.tfswufe.edu.cn/cas/login?service=https://ehall.tfswufe.edu.cn/violin-boot/servlet/public/simpleSSOLogin?app=cjc&pageId=21ba78cbbf6a760a088c3cd9e461c15f&type=9&identityRule=F_Account&cjcmode=h5&pageType=app"

#先登录网址保存cookie，维持登录
driver = webdriver.Chrome()
driver.get(login_html)

#设置模拟窗口格式
driver.set_window_size(1200, 800)
driver.implicitly_wait(10)
# driver.maximize_window()    #最大化窗口
# option = webdriver.ChromeOptions()  #无界面
# option.add_argument('--headless')

class Login():
    def __init__(self):
        self.Username = "42301717"
        self.password = "Z18723259228z"  
    def login_get_code(self):
        #获取验证码截图处理
        time.sleep(2)
        element = driver.find_element(By.CSS_SELECTOR,'[onclick="this.src=\'captcha.jpg?\'+Math.random()"]')
        x, y = element.location.values() # 坐标
        h, w = element.size.values() # 宽高
        image_data = driver.get_screenshot_as_png() # 把截图以二进制形式的数据返回
        screenshot = Image.open(BytesIO(image_data)) # 以新图片打开返回的数据
        result = screenshot.crop((x, y, x + w, y + h)) # 对截图进行裁剪
        result.save('code.png')   # result.show() # 显示图片

        with open('code.png', 'rb') as f:
            img_bytes = f.read()
        ocr = ddddocr.DdddOcr(show_ad=False)
        code = ocr.classification(img_bytes)
        print(f'验证码识别成功: {code}')
        return code
    def login_input(self):
        driver.find_element(By.ID, "username").send_keys(self.Username)
        driver.find_element(By.NAME, "password").send_keys(self.password)
        driver.find_element(By.CSS_SELECTOR, '#authcode').send_keys(self.login_get_code())
        driver.find_element(By.CSS_SELECTOR, '#submitTest').click()
    def login_get(self):       
        def get_try():
            self.login_input()      
            time.sleep(5)
            success_url = driver.current_url
            success_html = driver.page_source
            print(f"当前地址为:{success_url}")
            return success_html
        
        while 'pc门户 - 智慧融合门户' not in get_try():
            print('验证码识别错误！！...重新获取中')
            #刷新验证码重试
            try:
                driver.find_element(By.CSS_SELECTOR,'[onclick="this.src=\'captcha.jpg?\'+Math.random()"]').click()
                driver.find_element(By.ID, "username").clear()
                driver.find_element(By.NAME, "password").clear()
                driver.find_element(By.CSS_SELECTOR, '#authcode').clear()
            except Exception:
                print("没有找到登录的元素！！")
            get_try()
        else:
            print('登录成功!!!')





class right_xpath():
    """对多窗口进行定位,返回窗口的xpath和位置名称"""

    def __init__(self,window:int,curriculum:int) -> None:
        self.window = window
        self.curriculum = curriculum

    def should_number(self):
        """判断是否符合不同窗口数量的条件"""
        windows_should_number = []
        curriculums_should_number = []
        for i in range(1,self.window + 1):
            windows_should_number.append(i)
        
        for i in range(1,self.curriculum + 1):
            curriculums_should_number.append(i)
            
        return windows_should_number,curriculums_should_number

    def window_xpath(self)->str:
        
        if self.window in self.should_number()[0]:
            
            windows = f'//*[@id="app"]/div/section/div/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[2]/div/div/div[{self.window}]/div/div/div/div/div[2]/div/div/div'
            
            return self.window, windows
        else:
            print("窗口选择错误")

    def curriculum_xpath(self)->str:
        """选择课程，默认为:6"""
        if self.curriculum in self.should_number()[1]:
            
            curriculums = f'/html/body/div/div[2]/div[3]/ul/li[{self.curriculum}]/div[2]/h3/a'
        
            return self.curriculum,curriculums      
        else:
            print("课程选择错误")


class goto:

    def __init__(self,window:int,curriculum:int) -> None:
        """选择窗口和超星的课程

        Args:
            window (int): 窗口(超星在第五个窗口)
            curriculum (int):超星的课程
        """
        self.window_wicket = 9 #窗口数量
        self.curriculum = 6 #课程数量

        self.path = right_xpath(window,curriculum)
        self.window_xpath = self.path.window_xpath()
        self.curriculum_xpath = self.path.curriculum_xpath()
        print(self.window_xpath,self.curriculum_xpath)

    

    def num_path(self):
        """对前往某些地址执行特定步骤"""
        
        # 获取当前窗口的句柄,在终端打印
        def current_message():
            print(f"转到新地址为:{driver.current_url},该地址标题为:{driver.title}")
        
        
        if self.window_xpath[0] == 5:
            print(f'选择当前第{self.window_xpath[0]}个窗口')
            #执行第五个窗口需要的步骤
             
            time.sleep(5)   #等待网页渲染完成
            driver.find_element(By.XPATH,self.window_xpath[1]).click()  #点击窗口
            current_message()
                   
            #打开了新的选项卡
            time.sleep(3) 
            driver.get('https://tfswufe.fanya.chaoxing.com/portal')
            current_message()

            #mama的，这个新窗口有iframe结构定位不了
            # 获取当前所有窗口的句柄
            window_handles = driver.window_handles
            driver.find_element(By.CSS_SELECTOR,'[target="_blank"]').click()  # 执行会导致新开窗口的操作
            time.sleep(3)
            new_window = [handle for handle in driver.window_handles if handle not in window_handles][0]
            driver.switch_to.window(new_window)
            new_window_url = driver.current_url  # 获取新窗口的URL
            print(new_window_url)
            #选择课程
            driver.get(new_window_url)
            iframe = driver.find_element(By.ID, 'frame_content')   #解决了，hi hi
            driver.switch_to.frame(iframe)
            print(f'选择当前第{self.curriculum_xpath[0]}个课程')
            driver.find_element(By.XPATH,self.curriculum_xpath[1]).click()  #点击课程
            


def go_run():
    # 登录页面
    login = Login()
    login.login_get()
    # 进入课程
    GoTo = goto(window=5,curriculum=1)
    GoTo.num_path()


if __name__ == '__main__':
    go_run()
    
    time.sleep(6*60)
