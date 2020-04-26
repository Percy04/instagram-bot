from time import sleep
from selenium import webdriver
import random
import sys
from selenium.webdriver.common.keys import Keys
import fileinput


def print_same_line(text):
    sys.stdout.write('\r')
    sys.stdout.flush()
    sys.stdout.write(text)
    sys.stdout.flush()


class Instabot:

    def __init__(self, username, password):
        """
        Creates an instance of the Instabot class.

        Args:
            username:str: The username of the user
            password:str: The password of the user
        """

        self.username = username
        self.password = password
        self.driver = webdriver.Chrome()

    def login(self):
        """
        Logs a user into Instagram via the web portal
        """
        self.driver.get("https://www.instagram.com/")
        sleep(2)

        username_path = "//input[@name=\"username\"]"
        password_path = "//input[@name=\"password\"]"

        self.driver.find_element_by_xpath(username_path).send_keys(self.username)
        self.driver.find_element_by_xpath(password_path).send_keys(self.password)

        log_in_path = "//button[@type='submit']"
        self.driver.find_element_by_xpath(log_in_path).click()
        sleep(3)

        not_now_path = "//button[@class='aOOlW   HoLwm ']"
        self.driver.find_element_by_xpath(not_now_path).click()
        sleep(2)

    def closebrowser(self):
        """
        Closes the chrome browser
        """
        self.driver.close()

    def photo_follow_comment(self):
        """
        Enters the hashtag page and then selects a range of pics which it then
        likes, follows and comments.
        """
        driver = self.driver

        hashtags = ['coding', 'programming', 'school', 'student', 'f4f',
                    'followforfollow', 'follow4follow', 'cute', 'fun',
                    'photography', 'nofilter', 'photoshop', 'alumni',
                    'happy', 'me', 'followme', 'follow', 'instagood']
        
        tag = random.choice(hashtags)
        
        while True:
            driver.get("https://www.instagram.com/explore/tags/" + tag + "/")
            sleep(2)

            # gathering photos
            pic_hrefs = []

            for i in range(1, 7):
                try:
                    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                    sleep(2)
                    # get tags
                    hrefs_in_view = driver.find_elements_by_tag_name('a')
                    # finding relevant hrefs
                    hrefs_in_view = [elem.get_attribute('href') for elem in hrefs_in_view
                                     if '.com/p/' in elem.get_attribute('href')]
                    # building list of unique photos
                    [pic_hrefs.append(href) for href in hrefs_in_view if href not in pic_hrefs]
                    print("Check: pic href length " + str(len(pic_hrefs)))
                except Exception:
                    pass

            # Liking, following and comment users
            unique_photos = len(pic_hrefs)
            followers_list = []  # Contains the names of the people you followed

            for pic_href in pic_hrefs:
                driver.get(pic_href)
                sleep(2)
                try:
                    # Like this picture
                    driver.find_element_by_xpath("//*[@aria-label='Like']").click()

                    follow_button = driver.find_element_by_class_name('bY2yH')
                    # Follow the user if not followed already
                    if follow_button.text == "•\n" + "Follow":
                        follow_button.click()
                        followed = driver.find_element_by_class_name('e1e1d')
                        followers_list.append(followed.text)
                        with open("file.txt", 'a') as append:  # Add the username to file.txt
                            append.write(",".join(followers_list))
                            append.write(",")

                        # comment
                        comment_prob = random.randint(1, 10)

                        # This makes sure that I comment only a certain percentage of times.
                        if comment_prob >= 6:
                            # Clicking the comment box
                            driver.find_element_by_class_name('Ypffh').click()

                            comment_box_area = driver.find_element_by_xpath(
                                "/html/body/div[1]/section/main/div/div[1]/article/div[2]/section[3]/div/form/textarea")
                            # Adding the comment
                            list_of_comments = ["This is great", "Dope", "This is cool dude",
                                                "Promotions in the comment sections are so annoying."
                                                "NO, I am not going to tell you to follow me",
                                                "ayy nice one",
                                                "How do I get more followers? Make a bot they said",
                                                "This is what you came for - Rihanna",
                                                "Roast me",
                                                "Tell me a few things that you are doing during this quarantine",
                                                "Damn dude. Who else is hella bored ?",
                                                "I am super bored. So comment whether you wanna join or not and follow me"
                                                "and I will add you to a quarantine group chat. "
                                                "Where we all just chat and chill"]

                            comment_box_area.send_keys(random.choice(list_of_comments))

                            # Click Enter to post comment
                            comment_box_area.send_keys(Keys.ENTER)
                            sleep(3)
                        else:
                            pass

                    else:
                        continue

                    for second in reversed(range(0, 3)):
                        print_same_line("#" + tag + ': unique photos left: ' + str(unique_photos)
                                        + " | Sleeping " + str(second))
                        sleep(1)
                except Exception:
                    sleep(2)
                unique_photos -= 1

    def unfollow(self):
        """
        Unfollows the users followed by the bot.
        The names of the users are specified in the usernames.txt file
        """

        driver = self.driver
        with open("usernames.txt", 'r') as file:
            lines = file.read()

        for username in lines.split(","):
            driver.get("https://www.instagram.com/{}/".format(username))
            sleep(3)

            unfollow_button = driver.find_element_by_xpath("//*[@aria-label='Following']")
            if unfollow_button.text != 'Follow':
                unfollow_button.click()
                sleep(2)
                unfollow_confirmation = driver.find_element_by_xpath("//button[@class='aOOlW -Cab_   ']")
                unfollow_confirmation.click()
                sleep(3)
                for line in fileinput.input('usernames.txt', inplace=1):
                    sys.stdout.write(line.replace(username + "{}".format(','), ""))
            else:
                print("Following button was not found")

    def like_latest_posts(self, user, n_posts):
        """
        Likes a number of a users latest posts, specified by n_posts.
        Args:
            user:str: User whose posts to like or unlike
            n_posts:int: Number of most recent posts to like or unlike
        """
        driver = self.driver
        driver.get("https://www.instagram.com/{}/".format(user))

        images = []
        for i in range(1, 7):
            try:
                # get tags
                hrefs_in_list = driver.find_elements_by_tag_name('a')
                # finding relevant hrefs
                hrefs_in_list = [elem.get_attribute('href') for elem in hrefs_in_list
                                 if '.com/p/' in elem.get_attribute('href')]
                # building list of unique photos
                [images.append(href) for href in hrefs_in_list if href not in images]
                print("Check: pic href length " + str(len(images)))
            except Exception:
                pass

        for i in range(n_posts):
            driver.get(images[i])
            sleep(2)
            variable = driver.find_element_by_class_name("wpO6b ")
            if variable.text == "Like":
                try:
                    driver.find_element_by_xpath("//*[@aria-label='Like']").click()
                    print("Picture liked")
                except Exception as e:
                    print(e)


def usernames_list():
    """
    Removes all the duplicate usernames from file.txt
    """
    with open("file.txt", 'r') as file:
        lines = file.read()
        all_usernames = [lines]  # A list containing all the usernames, including the duplicates
        for usernames in all_usernames:
            # Here I am converting the single string of all usernames into strings of usernames
            all_split_usernames = usernames.split(",")

        final_followers_list = []
        for names in all_split_usernames:
            if names not in final_followers_list:
                final_followers_list.append(names)

        with open("usernames.txt", 'a') as new_file:
            new_file.write(",".join(final_followers_list))


if __name__ == '__main__':
    a = Instabot('Username', "Password")
    a.login()
    a.photo_follow_comment()
    a.unfollow()
    # a.like_latest_posts()

    usernames_list()
