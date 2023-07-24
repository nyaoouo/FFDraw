# 本地化

例子

```python
from ff_draw.gui.i18n import i18n
#文件头部必须import这么写


Action_list = i18n.reg(en='Action list', zh='实体表')
#添加一个本地化变量

print(i18n(Action_list))
#返回'Action list'或'实体表'
```

通常前2行的内容放在你插件文件的头部，或者另外做个本地化的文件

后续每次要调用本地化字符就都是 `i18n(XXXX)` 返回中文字符串或英文字符串