# GitHub 上可借鉴的设计模式

查阅日期：2026-10-30。以下为实际读过 README 和相关源码后的摘要，链接为当时默认分支，后续可能变化。本轮未安装插件、运行这些项目或复制其代码；外部示例不是用户试打验证。

## 1. CustomSupportsReborn：把支撑形状参数化

来源：[README](https://github.com/Slashee-the-Cow/CustomSupportsReborn/blob/master/README.md)、[CustomSupportsReborn.py](https://github.com/Slashee-the-Cow/CustomSupportsReborn/blob/master/CustomSupportsReborn.py)。

文档提供柱、方柱、管、两点间线形支撑和扶壁等形状，也支持向内/向外渐缩及尺寸限制；管形渐缩可以维持壁厚。可借鉴的是把“形状、顶/底尺寸、渐缩、壁厚、支承点”分开设计，而不是只放大一根柱。

关键源码观察：创建的网格设为 `support_mesh=True`、`support_mesh_drop_down=False`。这属于切片器解释的支撑网格；不能等同于奥利奥 STL 中作为普通模型实体打印的两个圆环。

迁移时先问清输出类别：
- 普通几何支撑：接触区与间隙由实体几何和实际模型路径决定。
- 切片支撑网格/修改器：由切片器继续解释其支撑语义和设置。

本次学到的参数体系可以迁移；切片器对特定标记的行为不能当成所有 CAD/STL 的通用行为。

## 2. OpenScad-Suspended-Hole：用局部桥接过渡处理大小孔交界

来源：[README](https://github.com/OrsoEric/OpenScad-Suspended-Hole/blob/Master/README.md)、[suspended_hole.scad](https://github.com/OrsoEric/OpenScad-Suspended-Hole/blob/Master/suspended_hole.scad)。

针对较大沉孔/螺母腔上接较小孔的悬空交界，源码在孔的负体积中安排宽、窄两段局部过渡；并提供四种开关组合的 `test_bench()`。这比泛称“加支撑”更具体：通过几层几何过渡改变第一批线条的桥接条件。

迁移建议：遇到此类孔先检查能否只在交界处增加桥接台阶/过渡，而不填满螺母腔。保护通孔净空、螺母装配包络和工具路径，用实际层高检查过渡落在哪几层。

源码使用 `gn_layer_height`，部分位置也直接依赖该全局量。不要把原项目默认 0.2 当作通用尺寸，也不要未经复核把这类孔口过渡称为“必须拆除的支撑膜”。README 展示作者的打印测试块，用户自己的条件仍需验证。

## 3. BOSL2：限制圆角底部的悬垂

来源：[shapes3d.scad](https://github.com/BelfrySCAD/BOSL2/blob/master/shapes3d.scad)，查找 `cuboid` 的 `teardrop` 参数和 `teardrop()`。

`cuboid` 的底部圆角可在达到指定的相对竖直方向角度时转成倒角；`teardrop()` 提供适合可打印孔的泪滴挤出形状。这是通过局部截面处理改善打印的具体实现。

迁移建议：当朝下圆角起始处过于陡峭时，可以保留上部圆弧并调整底部起点/斜面；水平孔可比较泪滴或受限孔顶。角度须说明参照方向，不能把某个默认角度直接认作机器能力。功能孔形变化需核对装配要求。

## 纳入经验库的方式

这些条目目前都是“外部文档/源码观察 → 待在用户模型中验证的候选”。实际使用后另建案例或补原案例，记录几何、工艺、结果，再决定是否提升为技能中的常用判断。避免把项目 README 整段搬进 SKILL.md。
