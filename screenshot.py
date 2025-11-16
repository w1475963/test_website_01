import random
import time

from playwright.sync_api import sync_playwright


def take_screenshots(url, count=5, interval=5):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            channel="msedge",  # 使用Edge浏览器
            headless=True,  # 无头模式（后台运行）
            args=[
                # Edge专用User-Agent
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36 Edge/120.0.0.0",
                "--window-size=1920,1080",  # 桌面窗口尺寸
                "--disable-blink-features=AutomationControlled",  # 消除自动化检测特征
                "--no-sandbox",
                "--disable-dev-shm-usage",
            ],
        )

        page = browser.new_page()
        page.set_viewport_size({"width": 1920, "height": 1080})

        # 打开网页并模拟真实用户行为（增加抗检测能力）
        page.goto(url, wait_until="domcontentloaded")  # 等待内容加载
        time.sleep(random.uniform(2, 4))  # 随机等待（避免固定间隔）

        # 模拟用户浏览：随机滚动页面
        # for _ in range(random.randint(1, 3)):
        #     page.mouse.wheel(0, random.randint(300, 800))  # 随机滚动
        #     time.sleep(random.uniform(1, 1.5))

        # 连续截图（间隔5秒+随机波动）
        for i in range(count):
            screenshot_path = f"edge-screenshot-{i + 1}.png"
            page.screenshot(path=screenshot_path, full_page=True)  # 截全屏
            print(f"已保存截图：{screenshot_path}")

            # 间隔（基础5秒 + 0-1秒随机波动，避免固定间隔被检测）
            # if i < count - 1:
            #     time.sleep(interval + random.uniform(0, 1))

        browser.close()


# 调用：替换为目标URL
take_screenshots(
    url="https://the-learning-room.netlify.app",
    count=10,
    interval=5,
)
