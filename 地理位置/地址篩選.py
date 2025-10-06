import re
addresslst = [
    "台北市大安區和平里12鄰復興南路一段390巷5弄7號、9號1樓",
    "新北市永和區秀朗里8鄰中正路535號2樓、535號3樓",
    "桃園市中壢區信義里3鄰中北路二段200號12樓之3、200號13樓"
]

for address in addresslst:
    # step1: 去掉「OO里」、「OO鄰」、「OO樓」
    cleaned = re.sub(r'[一-龥]{1,3}里|\d+鄰|\d+樓|[０-９]+樓', '', address)

    # step2: 若有重複門牌，只保留第一個號之後的內容
    cleaned = re.sub(r'(、|,|，)\s*\d+號.*', '', cleaned)

    # step3: 修整空白
    cleaned = cleaned.strip()

    print(cleaned)
