from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from multiprocessing import Process

NUM_PROCESSES = 10
DELAY = 5

print("Pollbot: Spam a pollev.com poll")
reps = int(input("Input number of repetitions: "))
name = input("Input Name of Presenter: ")
option = input("Poll option: ")

url = "https://pollev.com/" + name


def exec(num_reps):
    num_reps = int(num_reps)
    for i in range(num_reps):
        options = Options()
        options.add_argument("--headless")
        browser = webdriver.Firefox(options=options)
        wait = WebDriverWait(browser, DELAY)
        browser.get(url)
        try:
            cont = wait.until(EC.element_to_be_clickable(
                (By.CLASS_NAME, 'pec-response-screen-name__create')))
            cont.click()
        except:
            print("Unable to click choice.")

        try:
            choice = wait.until(EC.element_to_be_clickable(
                (By.XPATH, f"(//button[@class='component-response-multiple-choice__option__vote'])[{option}]")))
            choice.click()
        except:
            print("Unable to click choice.")
        browser.quit()


if __name__ == '__main__':
    processes = []
    remain = reps % NUM_PROCESSES
    for i in range(NUM_PROCESSES):
        num_reps = int(reps/NUM_PROCESSES)
        if remain > 0:
            num_reps += 1
            remain -= 1
        processes.append(Process(target=exec, args=(num_reps,)))
        processes[-1].start()

    for i in range(len(processes)):
        processes[i].join()
    print("Finished")
