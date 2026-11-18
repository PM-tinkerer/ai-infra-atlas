# 智算架构图谱 · AI Infra Atlas

从大模型执行原理到大规模异构服务平台的推理优化课程，共 12 章。内容兼顾技术原理、数量级估算、工程边界与产品决策。

## 阅读

下载项目后，用浏览器打开 [notes/index.html](notes/index.html)。页面包含课程导航、章节全景图、正文和可放大的交互图表；图片及图表已内嵌，支持离线阅读与单文件分享。正文中的外部来源链接需联网访问。

完整课程框架与章节目标见 [COURSE.md](COURSE.md)。

| 阶段 | 章节 |
| --- | --- |
| 理解一次推理如何在硬件上发生 | 1. 大模型推理原理；2. GPU 架构；3. 性能模型与度量 |
| 理解一张卡和一个推理引擎如何变快 | 4. 计算与精度优化；5. KV Cache 与长上下文；6. 推理引擎与生成调度 |
| 从单个引擎走向多卡、多厂商与服务平台 | 7. 多 GPU 与多节点推理；8. 国产 GPU 与 AI 加速器全景；9. 分布式 Serving 与异构纳管 |
| 让平台在海量请求下高效、稳定且经济 | 10. 多层调度与容量规划；11. 稳定性与多租户保障；12. 评测、成本与产品决策 |

## 文件结构

```text
COURSE.md                  课程框架与章节目标
AGENTS.md                  项目协作和教学约定
NOTES_CONTENT_GUIDE.md      正文内容规范
PANORAMA_GUIDE.md           全景图内容与视觉规范
notes/
  index.html               离线阅读入口
  ch01.md … ch12.md         章节正文维护源
  assets/                  当前全景图及首页配图
  diagrams/chNN/           正文图表的 JSON 定义、HTML、SVG 和校验记录
  panorama-manifest.json   章节全景图资产清单与来源
  build_notes.py           局部更新笔记入口
  *.py                     首页、导航与布局模块
```

## 维护与生成

笔记生成使用 Python 3.10 或更新版本，只依赖标准库。在项目根目录运行：

```sh
# 更新指定章正文及目录
python3 notes/build_notes.py --chapter ch02

# 更新首页和章节布局，保留现有正文
python3 notes/build_notes.py --site

# 按资产清单更新指定章全景图
python3 notes/build_notes.py --panoramas ch02
```

构建脚本在现有 `notes/index.html` 上局部更新；该文件也应纳入版本管理。正文与图片更新后同步提交生成的 HTML，保留页面中的人工修改。全景图映射见 `notes/panorama-manifest.json`。

图表的可编辑定义与交互 HTML、SVG 预览按同名文件配套保留。图表 HTML 已生成，阅读与日常笔记构建无需安装额外工具。从图表 HTML 重新提取 SVG 时，需自行安装 Playwright 及其 Chromium：

```sh
npm install --no-save --package-lock=false playwright
npx playwright install chromium
node notes/diagrams/export_previews.cjs ch02
```

`CHROME_PATH` 环境变量可指定已有 Chrome/Chromium 的可执行文件路径。修改图表定义后，需要使用 Archify 重新生成和校验对应 HTML，再导出预览、更新章节。

## 内容约定

数值算例按正文说明区分教学假设、理论估算与实测；硬件参数及软件支持范围以相邻的一手来源、版本和测试条件为准。课程内容会随技术演进更新。

图表目录中的质量记录描述当时的检查结果。项目保留当前内容与维护源；旧版资产、制作过程材料和全景图历史校验记录不随项目发布。
