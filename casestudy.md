# AWS GPU 客户案例

## 案例一：斯曼森 - 法律大模型微调

**公司**: 斯曼森（AI科技企业）

**场景**: 法律咨询服务 - "鳀鲸"法律模型

**使用服务**: Amazon Nova Pro + SageMaker + Qwen1.5 7B

**方案亮点**:
- 使用 Amazon Nova 进行数据扩增，生成超过 6000 条微调数据
- 基于 Qwen1.5 7B 进行 LoRA 微调
- 部署于宁夏区域

**效果提升**:
| 指标 | 对照模型 | 鳀鲸模型 | 提升 |
|------|---------|---------|------|
| 案情识别准确率 | 90% | 99% | +9% |
| 问题相关性/完整性 | 70% | 92% | +22% |
| 专业人员满意度 | 60% | 90% | +30% |

**原文**: https://aws.amazon.com/cn/blogs/china/smartions-use-amazon-nova-to-create-a-big-model-of-chinese-laws/

---

## 案例二：云学堂 - 代码生成大模型

**公司**: 云学堂（Nasdaq: YXT，企业培训SaaS）

**场景**: Java 代码智能生成与补全

**使用服务**: Amazon SageMaker + DeepSeek Coder 6.7B

**方案亮点**:
- 基于业务代码库使用 AST 技术提取代码，生成 FIM 数据集
- 数据集超过亿级 tokens（67%业务代码 + 20% GitHub + 13%自然语言）
- 使用 DeepSpeed Zero-3 分布式训练
- 结合 PiSSA、LoRA 和全参数微调

**效果提升**:
| 指标 | 基础模型 | 微调后 | 提升 |
|------|---------|--------|------|
| CodeBleu | 38.96 | 56.07 | +44% |
| ngram匹配 | 15.32 | 31.86 | +108% |
| syntax匹配 | 47.14 | 65.06 | +38% |

**原文**: https://aws.amazon.com/cn/blogs/china/yxt-innovative-practice-of-fine-tuning-large-models-and-enabling-code-generation-based-on-amazon-sagemaker/
