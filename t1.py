import sys

from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select

'''
第1部分：读取货币网页构建英文缩写与中文货币名称的对应字典
'''

# 空字典
mapping = {}
# 读取货币网页
driverCurrency = webdriver.Chrome()
driverCurrency.get("https://www.11meigui.com/tools/currency")
# 使用 XPath 往上级定位到包含 ‘国别’的 table 元素
tables = driverCurrency.find_elements('xpath','//table[.//td[contains(text(), "国别")]]')
# 定位了1个table，5个小table，只需要5个小table，分别是5个洲的数据，为方便查看写入txt
with open('currency.txt', 'w') as file:
    for table in tables[1:]:
        trs = table.find_elements('xpath','.//tr[position() >= 3]')
        if (trs):
            for tr in trs:
                td1 = tr.find_element('xpath', './/td[position() = 2]')
                file.write(td1.text + ' ')
                td2 = tr.find_element('xpath', './/td[position() = 5]')
                file.write(td2.text + '\n')
                mapping[td2.text] = td1.text

# print(mapping)
driverCurrency.quit()

'''
第2部分：读取银行网页
'''
# 处理命令行参数参数
args = sys.argv[1:]
date = args[0]
currency = args[1]

# 创建一个WebDriver实例，指定使用Chrome浏览器
driver = webdriver.Chrome()

# 访问目标网站
driver.get("https://www.boc.cn/sourcedb/whpj/")

# 定位起始时间和结束时间
startTime_input = driver.find_element("name","erectDate")
endTime_input = driver.find_element("name","nothing")

# 输入起始时间和结束时间
startTime_input.send_keys(date)
endTime_input.send_keys(date)

#定位货币种类
currency_input = driver.find_element("name","pjname")
select_currency = Select(currency_input)
try:
    select_currency.select_by_visible_text(mapping[currency])
except NoSuchElementException:
    print(f'{mapping[currency]}does not exist')
    driver.quit()
# 模拟按搜索按钮
button_parent = driver.find_element("id", "historysearchform")
search_button = button_parent.find_element("css selector", "input.search_btn")
search_button.click()

# 定位现汇卖出价
table_element = driver.find_element("xpath","//div[@class='BOC_main publish']/table")
# table_element = driver.find_element()
td_element = table_element.find_element("xpath","//table//tr[" + str(2) + "]/td[" + str(4) + "]")
td_content = td_element.text
print(td_content)

# 将结果写入txt
with open('result.txt', 'w') as file:
    # 将内容写入文件
    file.write(td_content)

# 输出成功提示
print("结果已写入 result.txt 文件")
# 关闭浏览器
driver.quit()