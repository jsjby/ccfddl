#!/usr/bin/env python3
import datetime
import re

def compute_countdown(month, day):
    """
    根据指定的月、日构造截止时间（截止时刻设为 23:59:59），
    如果当年已过，则使用下一年。返回倒计时文本。
    """
    now = datetime.datetime.now()
    target_year = now.year
    try:
        target_dt = datetime.datetime(target_year, month, day, 23, 59, 59)
    except ValueError:
        return None
    if target_dt < now:
        target_dt = datetime.datetime(target_year + 1, month, day, 23, 59, 59)
    delta = target_dt - now
    if delta.total_seconds() <= 0:
        return "时间已到"
    days = delta.days
    hours, rem = divmod(delta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    return f"还剩 {days} 天 {hours} 小时 {minutes} 分钟 {seconds} 秒"

def update_deadlines(readme_file='README.md'):
    """
    扫描 Markdown 文件中所有形如 [截止：xx.xx] 的标记，
    将其替换为带有动态倒计时的文本。
    如果原来有 ~~ 删除线格式，也保留该格式。
    """
    with open(readme_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # 匹配模式：可选的前置删除线 (~~)，接着 [截止：，日期格式 xx.xx，]，可选的后置删除线
    pattern = r'(?P<tilde>~~)?\[截止：(?P<date>\d{1,2}\.\d{1,2})\](?P<tilde2>~~)?'

    def replacer(match):
        tilde = match.group('tilde') or ''
        tilde2 = match.group('tilde2') or ''
        date_str = match.group('date')
        try:
            month, day = map(int, date_str.split('.'))
        except Exception as e:
            return match.group(0)  # 解析失败保持原样
        countdown_text = compute_countdown(month, day)
        if countdown_text is None:
            return match.group(0)
        return f"{tilde}[截止：{countdown_text}]{tilde2}"

    new_content = re.sub(pattern, replacer, content)
    
    with open(readme_file, 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Markdown 中所有截止标记已更新。")

if __name__ == "__main__":
    update_deadlines()
