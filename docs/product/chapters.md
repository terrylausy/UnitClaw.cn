## Page 1: 封面页
- **Page Type**: Cover
- **Page Title**: 货代邮件营销自动化流程
- **Page Subtitle**: 团队培训指引 | 2026年4月
- **Selected Template**: 
- **Content Structure**: 主标题 + 副标题 + 日期/版本信息
- **Content Density**: Light
- **Narrative Role**: 建立专业感，明确培训主题
- **Image Requirements**: 无
- **Page Weight**: Core page
- **Notes**: 使用商务风格设计

## Page 2: 目录页
- **Page Type**: TOC
- **Page Title**: 培训内容
- **Selected Template**: 
- **Content Structure**: 
  1. 流程概览
  2. 流程1：信息收集与飞书推送
  3. 流程2：自动邮件发送
  4. 流程3：飞书结果通知
  5. 日常操作指南
  6. 故障排查
- **Content Density**: Medium
- **Narrative Role**: 帮助学员了解培训结构
- **Image Requirements**: 无
- **Page Weight**: Secondary page

## Page 3: 流程概览
- **Page Type**: Content
- **Page Title**: 三大核心流程
- **Selected Template**: 
- **Content Structure**: 
  - 核心论点：系统包含三个自动化流程，实现从信息收集到邮件发送的全自动化
  - 证据1：流程1 - 每天10:00自动推送货代信息到飞书
  - 证据2：流程2 - 每天10:05自动发送30封邮件
  - 证据3：流程3 - 发送完成后自动飞书通知结果
  - 关键洞察：三个流程环环相扣，形成完整自动化闭环
- **Content Density**: Medium
- **Narrative Role**: 建立整体认知框架
- **Image Requirements**: 流程架构图 - 展示三个流程的关系和时序
- **Page Weight**: Core page

## Page 4: 流程1-信息收集
- **Page Type**: Content
- **Page Title**: 流程1：信息收集与飞书推送
- **Selected Template**: 
- **Content Structure**: 
  - 核心论点：每天自动收集30个新货代联系人并推送到飞书
  - 证据1：执行时间 - 每天10:00
  - 证据2：自动化ID - automation-2
  - 证据3：数据来源 - 预存的30家核心货代公司数据库
  - 关键洞察：飞书推送包含完整联系信息表格，便于团队查看
- **Content Density**: Medium
- **Narrative Role**: 介绍第一个自动化流程
- **Image Requirements**: 无
- **Page Weight**: Core page

## Page 5: 流程2-邮件发送
- **Page Type**: Content
- **Page Title**: 流程2：自动邮件发送
- **Selected Template**: 
- **Content Structure**: 
  - 核心论点：使用Henry@link-trans.com自动批量发送个性化邮件
  - 证据1：执行时间 - 每天10:05（飞书推送后5分钟）
  - 证据2：发送邮箱 - Henry@link-trans.com
  - 证据3：邮件特点 - 根据区域自动个性化内容
  - 证据4：每日发送量 - 30封邮件
  - 关键洞察：邮件内容包含公司介绍、合作价值、预约通话
- **Content Density**: Heavy
- **Narrative Role**: 介绍核心邮件发送流程
- **Image Requirements**: 无
- **Page Weight**: Core page

## Page 6: 联系人数据格式
- **Page Type**: Content
- **Page Title**: 联系人数据格式
- **Selected Template**: 
- **Content Structure**: 
  - 核心论点：daily_contacts.json是每日数据输入的关键文件
  - 必须字段：company_name（公司全称）、email（联系邮箱）、region（运作区域）
  - 可选字段：website（公司网站）、phone（联系电话）
  - 区域格式规范：城市/区域，如"New York/New Jersey"
  - 关键洞察：数据质量直接影响邮件个性化效果
- **Content Density**: Medium
- **Narrative Role**: 说明数据准备规范
- **Image Requirements**: JSON格式示例代码块
- **Page Weight**: Core page

## Page 7: 邮件内容模板
- **Page Type**: Content
- **Page Title**: 邮件内容模板
- **Selected Template**: 
- **Content Structure**: 
  - 核心论点：邮件内容经过精心设计，突出Linktrans核心优势
  - 邮件主题：Exploring a strategic trans-Pacific partnership | Linktrans Asset-Based Logistics
  - 核心卖点1：直接美国资产控制 - 7+自营仓库，80万+平方英尺
  - 核心卖点2：行业领先清关 - 2.3%查验率，提前4天完成清关
  - 核心卖点3：定制白标服务 - 24/7双语团队，品牌化服务
  - 行动号召：预约周六上午10点EST通话
- **Content Density**: Heavy
- **Narrative Role**: 展示邮件营销内容策略
- **Image Requirements**: 无
- **Page Weight**: Core page

## Page 8: 流程3-结果通知
- **Page Type**: Content
- **Page Title**: 流程3：飞书结果通知
- **Selected Template**: 
- **Content Structure**: 
  - 核心论点：邮件发送完成后立即推送飞书通知，无论成功与否
  - 通知内容1：发送日期和整体状态（全部成功/部分成功/全部失败）
  - 通知内容2：成功/失败数量统计
  - 通知内容3：失败联系人列表（如有）
  - 通知内容4：无联系人时的特殊提示
  - 关键洞察：实时反馈让团队第一时间掌握营销效果
- **Content Density**: Medium
- **Narrative Role**: 介绍结果通知机制
- **Image Requirements**: 飞书通知卡片样式示意图
- **Page Weight**: Core page

## Page 9: 日常操作指南
- **Page Type**: Content
- **Page Title**: 日常操作指南
- **Selected Template**: 
- **Content Structure**: 
  - 核心论点：团队只需在每天9:30-9:45完成数据准备
  - 步骤1（9:30）：收集30个新货代联系人信息
  - 步骤2（9:45）：将联系人写入daily_contacts.json
  - 步骤3（10:00）：【自动】飞书推送报告
  - 步骤4（10:05）：【自动】批量发送邮件
  - 步骤5（10:10）：【自动】飞书通知发送结果
  - 关键洞察：人工仅需15分钟准备，其余全自动
- **Content Density**: Heavy
- **Narrative Role**: 指导日常操作流程
- **Image Requirements**: 时间线流程图
- **Page Weight**: Core page

## Page 10: 故障排查
- **Page Type**: Content
- **Page Title**: 故障排查
- **Selected Template**: 
- **Content Structure**: 
  - 核心论点：掌握常见问题及解决方案，确保系统稳定运行
  - 问题1：飞书未收到通知 → Webhook失效 → 检查Webhook配置
  - 问题2：邮件发送失败 → SMTP认证失败 → 检查邮箱授权码
  - 问题3：无联系人通知 → 文件未创建 → 检查daily_contacts.json
  - 问题4：部分发送失败 → 邮箱地址无效 → 检查邮箱格式
  - 关键洞察：大部分问题可通过检查配置文件解决
- **Content Density**: Medium
- **Narrative Role**: 提供问题解决指南
- **Image Requirements**: 无
- **Page Weight**: Secondary page

## Page 11: 关键要点总结
- **Page Type**: Content
- **Page Title**: 关键要点总结
- **Selected Template**: 
- **Content Structure**: 
  - 核心论点：掌握三大要点，确保自动化流程顺利运行
  - 要点1：每天9:45前完成daily_contacts.json数据准备
  - 要点2：确保联系人邮箱格式正确，区域信息完整
  - 要点3：关注飞书通知，及时处理发送失败情况
  - 要点4：SMTP授权码过期需及时更新
  - 行动号召：开始你的自动化邮件营销之旅
- **Content Density**: Medium
- **Narrative Role**: 总结培训要点，强化记忆
- **Image Requirements**: 无
- **Page Weight**: Core page

## Page 12: 结束页
- **Page Type**: Ending
- **Page Title**: 谢谢观看
- **Page Subtitle**: Questions?
- **Selected Template**: 
- **Content Structure**: 感谢语 + 联系方式 + Q&A提示
- **Content Density**: Light
- **Narrative Role**: 结束培训，开放提问
- **Image Requirements**: 无
- **Page Weight**: Secondary page
