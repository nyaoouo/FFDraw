class I18N:
    lang = ['en', 'zh']

    def __init__(self):
        self.table = []
        self.current_lang = 0

    def reg(self, **kwargs):
        assert len(kwargs) > 0
        default = kwargs[next(iter(kwargs))]
        self.table.append([kwargs.get(l, default) for l in self.lang])
        return len(self.table) - 1

    def __call__(self, code, lang=None):
        if lang is None:
            lang = self.current_lang
        elif isinstance(lang, str):
            lang = self.lang.index(lang)
        return self.table[code][lang]


i18n = I18N()
Panel = i18n.reg(en='Panel', zh='控制台')
Plugin = i18n.reg(en='Plugin', zh='插件')
Style = i18n.reg(en='Style', zh='风格')
Setting = i18n.reg(en='Setting', zh='设置')
Enable_plugin = i18n.reg(en='Enable plugin', zh='启用插件')
Custom_plugin_path = i18n.reg(en='Custom plugin path', zh='自定义插件路径')
Delete = i18n.reg(en='delete', zh='删除')
Edit = i18n.reg(en='edit', zh='编辑')
Add = i18n.reg(en='add', zh='添加')
Reset = i18n.reg(en='reset', zh='重置')
Enable_changes_tooltip = i18n.reg(en='*The change takes effect after restarting FFDraw',
                                  zh='*重启FFDraw后更改生效')
GUI = i18n.reg(en='GUI', zh='界面')
Font_size = i18n.reg(en='Font size', zh='字体大小')
Font_path = i18n.reg(en='Font path', zh='字体路径')
Font_changes_tooltip = i18n.reg(en='*The font size and style changes will take effect after restarting FFDraw.',
                                zh='*重启FFDraw后生效字体的大小和样式更改')
Color = i18n.reg(en='color', zh='颜色')
Opacity = i18n.reg(en='opacity', zh='透明度')
Opacity_background = i18n.reg(en='background opacity', zh='背景透明度')
Omen_draw = i18n.reg(en='Omen draw', zh='绘制')
Name = i18n.reg(en='Name', zh='名称')
Padding = i18n.reg(en='padding', zh='填充')
Border = i18n.reg(en='Border', zh='边框')
Normal = i18n.reg(en='Normal', zh='常规')
Language = i18n.reg(en='Language', zh='语言')
Proxy = i18n.reg(en='Proxy', zh='网络代理')
Proxy_address = i18n.reg(en='address', zh='地址')
Proxy_port = i18n.reg(en='port', zh='端口')
Test = i18n.reg(en='test', zh='测试')
Always_drawing = i18n.reg(en='Always drawing', zh='始终绘制')
Sniffer = i18n.reg(en='Sniffer', zh='日志输出')
Func_parser = i18n.reg(en='Func parser', zh='函数解析')
Print_compile = i18n.reg(en='print compile', zh='打印编译结果')
