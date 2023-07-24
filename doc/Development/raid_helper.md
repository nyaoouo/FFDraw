文件头引用

```python
from raid_helper.utils import *
```

> 因为plugins文件夹已经放入sys.path中，因此plugins文件夹也可以当做根使用
>
> 直接 `from raid_helper.utils` 
>
> 而不用 `from plugins.raid_helper.utils`

# ***Raid_Helper 开发者文档***


> 本文档仅对个人理解阐述的注释等等内容 如有补充请在本文档添加 ByErrer
> 

## **drawings部分**

 主要内容在根目录下的utils/drawings.py中
 

 1. 自动绘制填充数据注释

| 名称 |绘制内容 |参数|
|:--:|:--:|:-------------:|
| circle_shape |绘制一个圆形  | 0x10000
| rect_shape |绘制一个矩形  |0x20000
| fan_shape |绘制一个矩形  |degree  
| donut_shape |绘制一个月环  |inner, outer

例子：

> special_actions[32033] = 0x50000 | 180 # 半场刀   
> special_actions[32037] = 0x10000 | int(.5 * 0xffff) # 月环
> 
> special_actions[34541] = raid_utils.donut_shape(6, 22)  
> special_actions[34543] = raid_utils.fan_shape(180)


---

## **2.基础图形绘制注释**



#### 方法名：draw_distance_line
* 描述：添加一个两个实体之间的直线
* 参数：[distanceline参数](https://github.com/nyaoouo/FFDraw/blob/e7032fddabf5fbfc1451e6f8153f9e65c147bbe4/plugins/raid_helper/utils/drawings.py#L77)

---
#### 方法名：draw_knock_predict_circle
* 描述：添加一个击退位置的预测路径（箭头形状）
* 参数：[knock predict circle 参数](https://github.com/nyaoouo/FFDraw/blob/e7032fddabf5fbfc1451e6f8153f9e65c147bbe4/plugins/raid_helper/utils/drawings.py#L149)

---
#### 方法名：draw_decay
* 描述：添加一个距离衰减的扩散效果
* 参数：[decay参数](https://github.com/nyaoouo/FFDraw/blob/e7032fddabf5fbfc1451e6f8153f9e65c147bbe4/plugins/raid_helper/utils/drawings.py#L218)

---
#### 方法名：draw_share
* 描述：添加一个分摊效果
* 参数：[share参数](https://github.com/nyaoouo/FFDraw/blob/e7032fddabf5fbfc1451e6f8153f9e65c147bbe4/plugins/raid_helper/utils/drawings.py#L286)

---
#### 方法名：draw_circle
* 描述：添加一个圆形的绘制
* 备注：inner_radius表示内径距离，默认为0，想要绘制月环inner_radius填写float。
* 参数：[circle参数](https://github.com/nyaoouo/FFDraw/blob/e7032fddabf5fbfc1451e6f8153f9e65c147bbe4/plugins/raid_helper/utils/drawings.py#L335)

---
#### 方法名：draw_rect
* 描述：添加一个矩形的绘制
* 参数：[rect参数](https://github.com/nyaoouo/FFDraw/blob/e7032fddabf5fbfc1451e6f8153f9e65c147bbe4/plugins/raid_helper/utils/drawings.py#L370)
---
#### 方法名：draw_fan
* 描述：添加一个扇形的绘制
* 参数：[fan参数](https://github.com/nyaoouo/FFDraw/blob/e7032fddabf5fbfc1451e6f8153f9e65c147bbe4/plugins/raid_helper/utils/drawings.py#L401)
---
#### 方法名：draw_fan
* 描述：添加一个扇形的绘制
* 参数：[fan参数](https://github.com/nyaoouo/FFDraw/blob/e7032fddabf5fbfc1451e6f8153f9e65c147bbe4/plugins/raid_helper/utils/drawings.py#L401)

---
 #### 方法名：draw_line
* 描述：添加一个直线的绘制
* 参数：[line参数](https://github.com/nyaoouo/FFDraw/blob/e7032fddabf5fbfc1451e6f8153f9e65c147bbe4/plugins/raid_helper/utils/drawings.py#L477C1-L477C1)

 
