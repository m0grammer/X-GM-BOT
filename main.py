from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time
import pickle
import random

driver = webdriver.Firefox()
driver.maximize_window()
driver.get("about:preferences")
driver.execute_script("arguments[0].click();", driver.find_element(By.XPATH, "//*[@id='defaultZoom']"))
ActionChains(driver).click(driver.find_element(By.XPATH, "//*[@value='50']")).perform()

try:
    # Открываем страницу Twitter
    driver.get('https://twitter.com')
    time.sleep(10)

    # Для создания cookie
    # time.sleep(100)
    # pickle.dump(driver.get_cookies(), open(f"cookie", "wb"))

    # #Для использования cookie
    for cook in pickle.load(open(f"cookie", "rb")):
        driver.add_cookie(cook)

    time.sleep(10)

    driver.refresh()

    time.sleep(10)

    comments = 0

    while comments != 200:

        likeButtons = driver.find_elements(By.CSS_SELECTOR, '[data-testid="like"]')
        commentButtons = driver.find_elements(By.CSS_SELECTOR, '[data-testid="reply"]')
        for i in range(len(likeButtons)):
            if i != 4:
                try:
                    nextLikeButton = likeButtons[i]
                    nextLikeButton_1 = likeButtons[i + 1]
                    print("Post #" + str(comments) + " started")
                    # Обновляем координаты клика
                    x_offset = random.randint(-2, 2)
                    y_offset = random.randint(-2, 2)

                    # Создаем экземпляр ActionChains
                    actions = ActionChains(driver)

                    # Добавляем движение курсора с учетом смещения
                    actions.move_to_element_with_offset(likeButtons[i], x_offset, y_offset)

                    # Кликаем на кнопку
                    actions.click().perform()

                    print("Post was liked")
                    time.sleep(3)
                    driver.implicitly_wait(5)

                except Exception:
                    print(Exception)
                    print("Post wasn't liked")
                    driver.refresh()

                gms = 'gmList.txt'

                with open(gms, 'r', encoding='utf-8') as file:
                    lines = file.readlines()

                random_line = random.choice(lines).strip()

                try:
                    x_offset = random.randint(-5, 5)
                    y_offset = random.randint(-5, 5)
                    commentButton = commentButtons[i]
                    actions = ActionChains(driver)
                    actions.move_to_element_with_offset(commentButton, x_offset, y_offset)
                    actions.click().perform()
                    time.sleep(3)
                    driver.implicitly_wait(10)

                    inputComment = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetTextarea_0"]')
                    inputComment.send_keys(random_line)
                    time.sleep(3)
                    driver.implicitly_wait(10)

                    sentComment = driver.find_element(By.CSS_SELECTOR, '[data-testid="tweetButton"]')
                    actions = ActionChains(driver)
                    actions.move_to_element_with_offset(sentComment, x_offset, y_offset)
                    actions.click().perform()

                    print("Post was replied")
                    time.sleep(3)
                    # Добавляем задержку после клика
                    driver.implicitly_wait(2)
                    driver.execute_script("arguments[0].scrollIntoView(true);", nextLikeButton)
                except Exception:
                    print(Exception)
                    print("Post wasn't replied")
                    driver.refresh()

                print("\n")
            i += 1
            time.sleep(5)
            comments += 1

        else:
            driver.refresh()
            driver.implicitly_wait(10)
            likeButtons = driver.find_elements(By.CSS_SELECTOR, '[data-testid="like"]')
            commentButtons = driver.find_elements(By.CSS_SELECTOR, '[data-testid="reply"]')


finally:
    driver.quit()