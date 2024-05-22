import undetected_chromedriver as uc
import os
import time
import base64
from selenium.webdriver.common.by import By
import requests

# Ask user to input names of celebrities
celebrities = input("Enter the names of celebrities (separated by commas): ").split(',')

main_folder = r"D:\fahad\Skill_Set\Skill_2_Machine_Learning_for_Data_Science\Projects\Project_2_Face_Detection_Classification_Project\Model\Scraped Pictures"
os.makedirs(main_folder, exist_ok=True)
driver = uc.Chrome()

for celebrity in celebrities:
    celeb_folder = os.path.join(main_folder, celebrity.strip())  # Remove leading/trailing whitespaces
    os.makedirs(celeb_folder, exist_ok=True)
    name = celebrity.replace(" ", "+")
    link = f"https://www.google.com/search?q={name}&sca_esv=586607062&rlz=1C1JJTC_enPK1018PK1018&tbm=isch&sxsrf=AM9HkKmfgV0bNvt9V_tlEX4Z83gQ1fU3WA:1701349163481&source=lnms&sa=X&ved=2ahUKEwi7ypzE4-uCAxWeQvEDHbPABdEQ_AUoAnoECAUQBA&biw=1517&bih=686&dpr=0.9"
    driver.get(link)
    time.sleep(5)

    # Scroll down to the end of the page
    while True:
        # Get the current height of the page
        before_scroll_height = driver.execute_script("return document.body.scrollHeight;")
        
        # Scroll to the bottom
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            driver.find_element(By.CLASS_NAME,"LZ4I").click()
            time.sleep(10)
        except:
            pass
        
        # Wait for a short time to let the page load
        time.sleep(10)
        
        # Get the new height after scrolling
        after_scroll_height = driver.execute_script("return document.body.scrollHeight;")
        
        # Break the loop if there is no more content to load
        if before_scroll_height == after_scroll_height:
            break

    # Extract image URLs and download each image
    elements = driver.find_elements(By.CLASS_NAME, "eA0Zlc")
    for i, element in enumerate(elements, start=1):
        

        a = element.find_element(By.CLASS_NAME, "H8Rx8c")
        b = a.find_element(By.CLASS_NAME, "YQ4gaf")
        src = b.get_attribute("src")
        
        # Check if src is not None before processing
        if src is not None:
            # Download image
            if src.startswith('data:image'):
                # Handle base64 encoded images
                data = src.split(',')[1]  # Extract base64 data part
                image_data = base64.b64decode(data)
                image_path = os.path.join(celeb_folder, f"{celebrity}_image_{i}.jpg")
                with open(image_path, 'wb') as f:
                    f.write(image_data)
            else:
                response = requests.get(src)
                if response.status_code == 200:
                    image_path = os.path.join(celeb_folder, f"{celebrity}_image_{i}.jpg")
                    with open(image_path, 'wb') as f:
                        f.write(response.content)

    # Wait for a short time before quitting the driver
    time.sleep(5)

driver.quit()
