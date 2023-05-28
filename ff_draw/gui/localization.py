local_lang = ['en', 'zh']
local_list = [
    {'en': 'Panel', 'zh': '控制台'},
    {'en': 'Plugin', 'zh': '插件'},
    {'en': 'Style', 'zh': '风格'},
    {'en': 'setting', 'zh': '设置'},
    {'en': 'Enable plugin', 'zh': '启用插件'},
    {'en': 'Custom plugin path', 'zh': '自定义插件路径'},
    {'en': 'add', 'zh': '添加'},
    {'en': '*The path change takes effect after restarting FFDraw', 'zh': '*重启FFDraw后路径更改生效'},
    {'en': 'GUI', 'zh': '界面'},
    {'en': 'color', 'zh': '颜色'},
    {'en': 'opacity', 'zh': '透明度'},
    {'en': 'Omen draw', 'zh': '绘制'},
    {'en': 'Name', 'zh': '名称'},
    {'en': 'padding', 'zh': '填充'},
    {'en': 'Border', 'zh': '边框'},
    {'en': 'Normal', 'zh': '常规'},
    {'en': 'Language', 'zh': '语言'},
    {'en': 'Always drawing.', 'zh': '始终绘制'},
    {'en': 'Sniffer', 'zh': '日志输出'},
    {'en': 'Func parser', 'zh': '函数解析'},
    {'en': 'print compile', 'zh': '打印编译结果'},
]

local_list_pro = {}
for lang in local_lang:
    local_list_pro[lang] = {}
for i in local_list:
    if 'en' in i:  # 全部转小写
        i['en'] = i['en'].lower()
    for lang in local_lang:
        local_list_pro[lang][i[lang]] = {}
        for lang2 in local_lang:
            if lang != lang2:
                local_list_pro[lang][i[lang]][lang2] = i[lang2]


def localStr(text: str, lang: str, en_type=None):
    """返回当前text的另一种语言,无翻译则返回原text
    输入的text如果只含英文数字标点则匹配翻译时无视大小写\n
    en_type：
    None：默认小写
    0：开头大写
    1：全部大写
    """

    def format_en(t, _type):
        if _type == None:
            return t
        if _type == 0:
            re = t
            if t[0].isalpha():
                re = t[0].upper() + t[1:]
            return re
        if _type == 1:
            return t.upper()

    if text.isascii():
        low_text = text.lower()
    else:
        low_text = text
    for _lang in local_lang:
        if low_text in local_list_pro[_lang]:
            if lang in local_list_pro[_lang][low_text]:
                return format_en(local_list_pro[_lang][low_text][lang], en_type)
    return format_en(text, en_type)

