
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
* 参数：

	    pos1: typing.Callable[[], glm.vec3] | glm.vec3 | Actor,
        pos2: typing.Callable[[], glm.vec3] | glm.vec3 | Actor,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        duration: float = 0,
        alpha: typing.Callable[[BaseOmen], float] | float = None,
        min_distance: float = None,
        max_distance: float = None,
        step_distance: float = 1,

---
#### 方法名：draw_knock_predict_circle
* 描述：添加一个击退位置的预测路径（箭头形状）
* 参数：


	    radius: typing.Callable[[], float] | float,
        pos: typing.Callable[[], glm.vec3] | glm.vec3 | Actor,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        duration: float = 0,
        alpha: typing.Callable[[BaseOmen], float] | float = None,
        actor: Actor = None,
        knock_distance: int = True,

---
#### 方法名：draw_decay
* 描述：添加一个距离衰减的扩散效果
* 参数：

	    radius: typing.Callable[[BaseOmen], float] | float,
        pos: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3 | Actor,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        label: typing.Callable[[BaseOmen], str] | str = '',
        label_color: typing.Callable[[BaseOmen], tuple[float, float, float,]] | tuple[float, float, float,] = None,
        duration: float = 0,
        alpha: typing.Callable[[BaseOmen], float] | float = None,
        min_radius: typing.Callable[[BaseOmen], float] | float = None,
        draw_icon: typing.Callable[[BaseOmen], bool] | bool = True,

---
#### 方法名：draw_share
* 描述：添加一个分摊效果
* 参数：


	    radius: typing.Callable[[BaseOmen], float] | float,
        pos: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3 | Actor,
        facing: typing.Callable[[BaseOmen], float] | float | Actor = 0,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        label: typing.Callable[[BaseOmen], str] | str = '',
        label_color: typing.Callable[[BaseOmen], tuple[float, float, float,]] | tuple[float, float, float,] = None,
        duration: float = 0,
        alpha: typing.Callable[[BaseOmen], float] | float = None,

---
#### 方法名：draw_circle
* 描述：添加一个圆形的绘制
* 备注：inner_radius表示内径距离，默认为0，想要绘制月环inner_radius填写数值。
* 参数：

	    radius: typing.Callable[[BaseOmen], float] | float,
        pos: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3 | Actor,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        label: typing.Callable[[BaseOmen], str] | str = '',
        label_color: typing.Callable[[BaseOmen], tuple[float, float, float,]] | tuple[float, float, float,] = None,
        duration: float = 0,
        inner_radius: typing.Callable[[BaseOmen], float] | float = 0,
        alpha: typing.Callable[[BaseOmen], float] | float = None,

---
#### 方法名：draw_rect
* 描述：添加一个矩形的绘制
* 参数：

	    width: typing.Callable[[BaseOmen], float] | float,
        length: typing.Callable[[BaseOmen], float] | float,
        pos: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3 | Actor,
        facing: typing.Callable[[BaseOmen], float] | float | Actor = None,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        label: typing.Callable[[BaseOmen], str] | str = '',
        label_color: typing.Callable[[BaseOmen], tuple[float, float, float,]] | tuple[float, float, float,] = None,
        duration: float = 0,
        arg=0,  # 0:normal, 1:include back, 2:cross
        alpha: typing.Callable[[BaseOmen], float] | float = None,

---
#### 方法名：draw_fan
* 描述：添加一个扇形的绘制
* 参数：

	    degree: typing.Callable[[BaseOmen], float] | float,
        radius: typing.Callable[[BaseOmen], float] | float,
        pos: typing.Callable[[BaseOmen], glm.vec3] | glm.vec3 | Actor,
        facing: typing.Callable[[BaseOmen], float] | float | Actor = None,
        color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        surface_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        line_color: typing.Callable[[BaseOmen], glm.vec4 | str] | glm.vec4 | str = None,
        label: typing.Callable[[BaseOmen], str] | str = '',
        label_color: typing.Callable[[BaseOmen], tuple[float, float, float,]] | tuple[float, float, float,] = None,
        duration: float = 0,
        alpha: typing.Callable[[BaseOmen], float] | float = None,


---
 #### 方法名：draw_line
* 描述：添加一个直线的绘制
* 参数：

	    source: Actor | glm.vec3 | typing.Callable[[BaseOmen], glm.vec3],
        target: Actor | glm.vec3 | typing.Callable[[BaseOmen], glm.vec3],
        color: glm.vec4,
        width: int = 3,
        duration=0

附带部分基础参数表（抄的头子的api上的参考）
|     参数      |               类型               |                             描述                             |
| :-----------: | :------------------------------: | :----------------------------------------------------------: |
|    `radius`    |             `number`             |      图形的形状      |
| `shape_scale` |      `(number, number[3])`       | 一般用于使用特殊值（后详），为形状、比例的二元组，当存在时忽略 `shape` 和 `scale` 参数 |
|   `surface_color`   |     `number[3]`/`number[4]`      |       填充颜色的rgba值，如果输入长度为3，默认alpha为1        |
|    `line_color`     |     `number[3]`/`number[4]`      |       线条颜色的rgba值，如果输入长度为3，默认alpha为1        
|    `color`    | `string`/`number[3]`/`number[4]` | 输入为 `string` 时会套用预设配色（后详），否则等同于`surface`参数，当存在时忽略 `surface` 和 `line` 参数 |
|     `pos`     |           `number[3]`            | 图像在游戏3d空间里面的位置，对应 `[东西刻度，上下刻度，南北刻度]` |
|   `facing`    |             `number`             |               图像沿着y轴的旋转量，以rad为单位               |
|  `duration`   |             `number`             |           图像的存活时间，空则一直存在需要手动清除           |
|    `label`    |             `string`             |                     在指定位置显示的文字                     |
| `label_color` |           `number[3]`            |                        显示文字的颜色                        |
| `label_scale` |             `number`             |                        显示文字的比例                        |
|  `label_at`   |             `number`             | 显示文字的相对坐标的位置（[参见这里](./ff_draw/gui/text.py#L41)） |


## trigger部分
主要内容在utils/trigger.py中，用作触发绘制内容功能。
* 写法：在自定义py内，定义一个map变量（当在这张地图时触发），并且在map变量中添加一个装饰器函数。（用作触发条件）
* 例如：

> map_ex = raid_utils.MapTrigger.get(1096)
> 
> @map_ex.on_cast(31998)
> 
> def on_cast_xxxx(msg: NetworkMessage[zone_server.ActorCast]):

---

## 触发器条件

#### 触发条件：on_lockon
* 描述：头顶标记（icon）的触发条件，lockon内的数值填写可以查询godbert。
* 具体调用写法：
* ` def _recv_on_lockon(self, msg: ActorControlMessage[actor_control.SetLockOn]):`



---
#### 触发条件：on_cast
* 描述：boss读条触发的触发条件，cast内的数值填写可以查询godbert。
* 具体调用写法：
* `def _recv_on_cast(self, msg: NetworkMessage[zone_server.ActorCast]):`

---
#### 触发条件：on_effect
* 描述：技能效果
* 具体调用写法：
* `def _recv_on_effect(self, msg: NetworkMessage[zone_server.ActionEffect]):`
---
#### 触发条件：on_add_status
* 描述：新增的状态
* 具体调用写法：
* `def _recv_on_add_status(self, msg: ActorControlMessage[actor_control.AddStatus]):`
---  
#### 触发条件：  on_npc_spawn
* 描述：  npc生成的时候触发，例如小怪生成的时候。
* 具体调用写法：
* `def _recv_on_add_status_by_action(self, msg: AddStatusByActionMessage):`
---  
#### 触发条件：  on_object_spawn
* 描述：  某个目标对象生成的时候触发。
* 具体调用写法：
* `def _recv_on_npc_spawn(self, msg: NetworkMessage[zone_server.NpcSpawn | zone_server.NpcSpawn2]):`
---  
#### 触发条件：  on_actor_delete
* 描述：  监控actor，在actor消失的时候触发。
* 具体调用写法：
* `def _recv_on_actor_delete(self, msg: NetworkMessage[zone_server.ActorDelete]):`
---  
#### 触发条件：  on_npc_yell
* 描述：  监控npc的喊话，在喊话的时候触发，例如：巴哈奈尔台词
* 具体调用写法：
* `def _recv_on_npc_yell(self, msg: NetworkMessage[zone_server.NpcYell]):`
 ---  
#### 触发条件：   on_set_channel
* 描述：  连线机制的连线，比如说引导连线，绝欧米茄的P1连线大圈。
* 具体调用写法：
* `def _recv_on_set_channel(self, msg: ActorControlMessage[actor_control.SetChanneling]):`
 ---  
#### 触发条件：  on_actor_play_action_timeline
* 描述：  actor做一个动作触发，例如绝欧米茄P2二运男女连续技。
* 具体调用写法：
* ` def _recv_on_actor_play_action_timeline(self, msg: PlayActionTimelineMessage):`
 ---  
#### 触发条件：  on_map_effect
* 描述：地图的特效效果
* 具体调用写法：
* ` def _recv_on_map_effect(self, msg: NetworkMessage[zone_server.MapEffect]):`


## 具体的触发器参考可以参考头子写的副本绘制

例如：[火天王绘制实例](https://github.com/nyaoouo/FFDraw/blob/be64042094e8da138bdf9ed12ba3f55b0a36d393/plugins/raid_helper/ext4/mount_ordeals.py)


## 待编辑补充ing.....


