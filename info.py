from selenium import webdriver
import csv
import config
import time


class instaInfo:
    def __init__(self):
        """
        init webdriver
        """
        self.driver = webdriver.Chrome('chromedriver')
        self.profile_url = ''
        self.followers_count = 0
        self.ask_url()

    def ask_url(self):
        """
        get Instagram profile url
        """
        self.profile_url = input("Enter Instagram profile link: ")
        if self.profile_url[:26] != 'https://www.instagram.com/':
            print('Link must be like \'https://www.instagram.com/user_name/\'')
            return ask_url(self)

    def login_to_instagram(self):
        """
        connect and login to Instagram
        """
        try:
            # connect to Instagram login page
            self.driver.get('https://www.instagram.com/accounts/login/')
        except Exception as e:
            exit(f"Can't connect to: 'https://www.instagram.com/accounts/login/'\nError:{e}")
        time.sleep(2)

        try:
            # input login and password
            self.driver.find_element_by_name('username').send_keys(config.INSTAGRAM_LOGIN)
            self.driver.find_element_by_name('password').send_keys(config.INSTAGRAM_PASSWORD)

            # click to login button
            self.driver.find_element_by_css_selector('button.sqdOP.L3NKy.y3zKF').click()
        except Exception as e:
            exit(f"Can't login!\nError:{e}")
        time.sleep(3)

        try:
            # click save data button
            self.driver.find_element_by_css_selector('button.sqdOP.L3NKy.y3zKF').click()
        except Exception as e:
            exit(f"Can't click !\nError:{e}")
        time.sleep(3)
        print("Logged in Instagram")

    def connect_to_profile(self):
        """
        connect to Instagram profile
        """
        try:
            self.driver.get(self.profile_url)
        except Exception as e:
            exit(f"Can't connect to: {self.profile_url}\nError:{e}")
        time.sleep(3)
        print(f"Connected to profile: {self.profile_url}")

    def get_followers_count(self):
        """
        parse count of followers
        """
        try:
            self.followers_count = self.driver.find_elements_by_css_selector('span.g47SY')[1].get_attribute('title')

            # replace blank and convert to int type
            self.followers_count = int(self.followers_count.replace(' ', ''))
        except Exception as e:
            exit(f"Can't get followers count: {self.profile_url}\nError:{e}")

        print(f"{self.profile_url} count of followers: {self.followers_count}")

    def get_profile_followers(self):
        """
        get followers info
        """
        # click to followers button
        self.driver.find_element_by_css_selector('a.-nal3').click()
        time.sleep(3)

        # load all followers
        last_element = ''
        while last_element != self.driver.find_elements_by_css_selector('a.FPmhX.notranslate._0imsa')[-1]:
            last_element = self.driver.find_elements_by_css_selector('a.FPmhX.notranslate._0imsa')[-1]
            self.driver.execute_script('arguments[0].scrollIntoView(true);', last_element)
            time.sleep(1)

        # get links to followers
        followers_link = [follower.get_attribute('href') for follower in self.driver.find_elements_by_css_selector('a.FPmhX.notranslate._0imsa')]
        for follower_link in followers_link:

            # connect to follower profile
            self.profile_url = follower_link
            instagram_info_obj.connect_to_profile()

            # get count of followers
            self.get_followers_count()

            # write to csv
            self.append_to_csv()

    def append_to_csv(self):
        """
        write profile row and followers count into csv file
        """
        with open('instagramInfo.csv', mode='a', encoding='utf8', newline='') as csv_file:
            writer = csv.writer(csv_file, delimiter=';')
            writer.writerow([self.profile_url, self.followers_count])


if __name__ == "__main__":
    instagram_info_obj = instaInfo()
    instagram_info_obj.login_to_instagram()
    instagram_info_obj.connect_to_profile()
    instagram_info_obj.get_profile_followers()
    instagram_info_obj.driver.quit()
