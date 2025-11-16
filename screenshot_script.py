import random
import time

from playwright.sync_api import sync_playwright


def take_anti_bot_screenshots(url, count=5, interval=5):
    with sync_playwright() as p:
        # 1. 浏览器配置：伪装真实Chrome，消除无头特征
        browser = p.chromium.launch(
            headless=True,  # 保持无头（效率高），但优化参数
            args=[
                "--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",  # 真实Chrome User-Agent
                "--window-size=1920,1080",  # 模拟桌面窗口尺寸
                "--disable-blink-features=AutomationControlled",  # 关键：禁用“自动化控制”标识（规避检测）
                "--no-sandbox",  # GitHub Runner 需此参数（无沙箱环境）
                "--disable-dev-shm-usage",  # 解决内存不足问题
            ],
        )
        page = browser.new_page()
        # 2. 额外伪装：设置视口（与窗口尺寸一致）
        page.set_viewport_size({"width": 1920, "height": 1080})

        # 3. 打开网页：模拟真实加载（等待页面完全渲染）
        page.goto(url, wait_until="domcontentloaded")  # 等待DOM加载，而非仅网络空闲
        time.sleep(random.uniform(2, 4))  # 随机等待2-4秒（避免机械等待）

        # # 4. 模拟用户行为：滚动页面（模拟浏览）
        # page.mouse.wheel(0, random.randint(300, 800))  # 向下滚动300-800像素
        # time.sleep(random.uniform(1, 2))  # 滚动后停顿

        # 5. 循环截图（保留间隔，增加随机波动）
        for i in range(count):
            # 截图（可选：指定区域，更像用户截图习惯）
            screenshot_path = f"screenshot_{i + 1}.png"
            page.screenshot(path=screenshot_path, full_page=True)
            print(f"已保存截图：{screenshot_path}")

            # 间隔：基础5秒 + 0-1秒随机波动（避免固定间隔被识别）
            if i < count - 1:
                time.sleep(interval + random.uniform(0, 1))

        browser.close()


# 调用：替换为目标URL
take_anti_bot_screenshots(url="https://the-learning-room.netlify.app/welcome/video_welcome", count=5, interval=10)
