from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time
import os

def read_config(file_path):
    config = {}
    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split('=', 1)
            config[key] = value
    return config

# Xác định thư mục gốc và file config
base_dir = os.path.dirname(os.path.abspath(__file__))
config_file_path = os.path.join(base_dir, "config.txt")
config = read_config(config_file_path)

# Khởi tạo Selenium WebDriver
options = Options()
options.add_argument("--disable-gpu")
options.add_argument("--disable-extensions")
options.add_argument("--log-level=3")
options.add_argument("--incognito")
options.add_argument("window-size=1920x1080")

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)
driver.set_page_load_timeout(180)

email = config['email']
password = config['password']

# Mở trang web khảo sát
url = "https://student.uit.edu.vn/sinhvien/phieukhaosat"
driver.get(url)

# Đăng nhập
email_field = driver.find_element(By.NAME, "name")
password_field = driver.find_element(By.NAME, "pass")
email_field.send_keys(email)
password_field.send_keys(password)

# Chờ người dùng đăng nhập
input("[INFO] Vui lòng đăng nhập và nhấn Enter để tiếp tục...")

# Lấy danh sách khảo sát chưa thực hiện
survey_links = []
try:
    rows = driver.find_elements(By.XPATH, "//*[@id='block-system-main']/div/table/tbody/tr")
    for row in rows:
        try:
            survey_link = row.find_element(By.XPATH, "./td[2]/strong/a").get_attribute("href")
            status = row.find_element(By.XPATH, "./td[3]").text.strip()
            if status == "(Chưa khảo sát)":
                survey_links.append(survey_link)
        except Exception as e:
            continue
except Exception as e:
    print(f"[ERROR] Lỗi khi lấy danh sách khảo sát: {e}")

print(f"[INFO] Tìm thấy {len(survey_links)} khảo sát chưa thực hiện.")

# Tự động thực hiện từng khảo sát
for index, link in enumerate(survey_links):
    try:
        print(f"[INFO] Đang thực hiện khảo sát {index + 1}/{len(survey_links)}: {link}")
        driver.get(link)
        next_click_count = 0  # Đếm số lần bấm nút "Tiếp theo"

        while next_click_count < 4:  # Chỉ bấm nút "Tiếp theo" 4 lần
            try:
                if next_click_count == 2:
                    try:
                        mandatory_divs = driver.find_elements(By.CLASS_NAME, "list-radio.mandatory")
                        if len(mandatory_divs) >= 2:
                            # Chọn radio với value="A3" trong div đầu tiên
                            radios_a3 = mandatory_divs[0].find_elements(By.CLASS_NAME, "radio")
                            for radio in radios_a3:
                                if radio.get_attribute("value") == "A3":
                                    print(f"[CLICK] Chọn radio với value = A3")
                                    radio.click()
                                    time.sleep(0.2)
                                    break

                            # Chọn radio với value="A4" trong div thứ hai
                            radios_a4 = mandatory_divs[1].find_elements(By.CLASS_NAME, "radio")
                            for radio in radios_a4:
                                if radio.get_attribute("value") == "A4":
                                    print(f"[CLICK] Chọn radio với value = A4")
                                    radio.click()
                                    time.sleep(0.2)
                                    break
                        else:
                            print("[ERROR] Không tìm thấy đủ div 'list-radio mandatory'.")
                    except Exception as e:
                        print(f"[ERROR] Lỗi khi chọn radio trong 'list-radio mandatory': {e}")
                if next_click_count == 3:
                    radio1 = driver.find_elements(By.CLASS_NAME, "radio")
                    for checkradio in radio1:
                        try:
                            if checkradio.get_attribute("value") == "MH04":
                                print(f"[CLICK] Luôn chọn radio với value: MH04")
                                checkradio.click()
                                time.sleep(0.2)
                        except Exception:
                            continue
                # Bấm nút "Tiếp theo"
                next_button = WebDriverWait(driver, 10).until(
                    EC.element_to_be_clickable((By.ID, "movenextbtn"))
                )
                next_button.click()
                print(f"[INFO] Đã bấm nút 'Tiếp theo' lần {next_click_count + 1}.")
                next_click_count += 1
                time.sleep(1.5)  # Đợi trang tải
            except Exception:
                break

        # Sau lần bấm thứ 4, bấm nút "Gửi"
        try:
            submit_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.ID, "movesubmitbtn"))
            )
            submit_button.click()
            print("[INFO] Đã bấm nút 'Gửi'.")
            time.sleep(2)
        except Exception as e:
            print(f"[ERROR] Lỗi khi bấm nút 'Gửi': {e}")

        # Quay lại trang khảo sát chính
        driver.get("https://student.uit.edu.vn/sinhvien/phieukhaosat")
        print(f"[INFO] Khảo sát {index + 1} hoàn thành và đã quay lại trang chính.")
    except Exception as e:
        print(f"[ERROR] Lỗi khi thực hiện khảo sát {index + 1}: {e}")

# Kết thúc
print("[INFO] Hoàn thành tất cả khảo sát.")
driver.quit()
