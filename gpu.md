# AWS GPU 实例完整信息库

> 最后更新：2025-12-21
> 版本：v1.2

---

## P 系列 - 通用 GPU 计算实例

### P6e 系列（NVIDIA GB200 Grace Blackwell UltraServers）- Global

#### u-p6e-gb200x36
- **EC2 实例名称**: u-p6e-gb200x36
- **GPU 型号**: NVIDIA GB200 Grace Blackwell Superchip
- **GPU 数量**: 36 (在单个 NVLink 域内)
- **GPU 总显存**: 6,660 GB (13.4 TB HBM3e for 72x)
- **vCPU**: 1,296 (NVIDIA Grace CPU, ARM-based)
- **系统内存**: 8,640 GiB
- **网络带宽**: 14,400 Gbps (14.4 Tbps EFAv4)
- **EBS 带宽**: 540 Gbps
- **实例存储**: 202.5 TB NVMe SSD
- **计算性能**: 180 PetaFLOPS (FP8, non-sparse)
- **发布时间**: 2024年12月
- **可用区域**: us-east-1-dfw-2a (达拉斯本地扩展区)
- **Workload类型**: 训练
- **适用场景**:
  - 超大规模AI模型训练 (万亿参数级别)
  - 混合专家模型 (Mixture of Experts)
  - 多模态大模型训练
  - 生成式AI应用 (代码生成、视频/图像生成、语音识别)
- **技术特点**:
  - NVIDIA NVLink-C2C 互连技术，GPU与CPU紧密集成
  - 支持 NVIDIA GPUDirect RDMA
  - AWS Nitro System 技术支持
  - 可扩展至数万个 GPU (EC2 UltraClusters)
- **购买方式**: EC2 Capacity Blocks for ML
- **集成服务**:
  - Amazon SageMaker Hyperpod
  - Amazon EKS (支持拓扑感知路由)
  - Amazon FSx for Lustre

#### u-p6e-gb200x72
- **EC2 实例名称**: u-p6e-gb200x72
- **GPU 型号**: NVIDIA GB200 Grace Blackwell Superchip
- **GPU 数量**: 72 (在单个 NVLink 域内)
- **GPU 总显存**: 13,320 GB (13.4 TB HBM3e)
- **vCPU**: 2,592 (NVIDIA Grace CPU, ARM-based)
- **系统内存**: 17,280 GiB
- **网络带宽**: 28,800 Gbps (28.8 Tbps EFAv4)
- **EBS 带宽**: 1,080 Gbps
- **实例存储**: 405 TB NVMe SSD
- **计算性能**: 360 PetaFLOPS (FP8, non-sparse)
- **发布时间**: 2024年12月
- **可用区域**: us-east-1-dfw-2a (达拉斯本地扩展区)
- **Workload类型**: 训练
- **适用场景**:
  - 最大规模AI模型训练 (万亿参数以上)
  - 需要最高计算密度的分布式训练
  - 复杂多模态模型处理
- **技术特点**:
  - 单一 NVLink 域内最大 GPU 配置
  - 最高网络吞吐量 28.8 Tbps
  - 405 TB 本地存储，适合大数据集缓存
- **购买方式**: EC2 Capacity Blocks for ML

#### p6e-gb200.36xlarge
- **EC2 实例名称**: p6e-gb200.36xlarge
- **GPU 型号**: NVIDIA GB200 Grace Blackwell Superchip
- **GPU 数量**: 4
- **GPU 总显存**: 740 GB HBM3e
- **vCPU**: 144
- **系统内存**: 960 GiB
- **网络带宽**: 1,600 Gbps EFAv4
- **EBS 带宽**: 60 Gbps
- **实例存储**: 22.5 TB NVMe SSD
- **GPU Peer to Peer**: 1,800 GB/s NVLink
- **GPUDirect RDMA**: 支持
- **发布时间**: 2025年
- **Workload类型**: 训练
- **适用场景**:
  - 中大规模模型训练
  - 多模态模型部署

---

### P6 系列（NVIDIA B200）- Global

#### p6-b200.48xlarge
- **EC2 实例名称**: p6-b200.48xlarge
- **GPU 型号**: NVIDIA B200 Tensor Core GPU
- **GPU 数量**: 8
- **每GPU显存**: 180GB HBM3e
- **GPU 显存带宽**: 8 TB/s (每GPU)
- **vCPU**: 192 (Intel Xeon Scalable 第5代 Emerald Rapids)
- **系统内存**: 2,048 GB
- **网络带宽**: 3,200 Gbps (EFAv4)
- **EBS 带宽**: 100 Gbps
- **实例存储**: 8 x 3.84TB NVMe SSD (30.7 TB 总量)
- **发布时间**: 2024年（2025年5月GA）
- **Workload类型**: 训练
- **适用场景**: 超大规模AI训练(>1T参数)、多模态模型训练
- **价格参考** (us-east-1, 估算):
  - 按需: ~$113.93/小时
  - **注意**: 实际价格以AWS官网为准

#### p6-b300.48xlarge
- **EC2 实例名称**: p6-b300.48xlarge
- **GPU 型号**: NVIDIA B300 Blackwell Ultra
- **GPU 数量**: 8
- **GPU 总显存**: 2.1 TB HBM3e (2100 GB)
- **每GPU显存**: 262GB HBM3e
- **vCPU**: 192
- **系统内存**: 4 TB
- **网络带宽**: 6,400 Gbps EFA + 300 Gbps ENA
- **实例存储**: 30 TB NVMe SSD
- **发布时间**: 2025年
- **Workload类型**: 训练
- **适用场景**: 顶级训练性能、需要更大系统内存的场景
- **价格参考** (us-west-2):
  - 按需: ~$142.42/小时
  - **注意**: 实际价格以AWS官网为准

---

### P5 系列（NVIDIA H100/H200）- Global

#### p5en.48xlarge
- **EC2 实例名称**: p5en.48xlarge
- **GPU 型号**: NVIDIA H200 Tensor Core GPU (Enhanced Networking)
- **GPU 数量**: 8
- **每GPU显存**: 141GB HBM3e
- **GPU 显存带宽**: 4.8 TB/s (每GPU)
- **vCPU**: 192 (Intel Xeon Scalable 第4代)
- **系统内存**: 2,048 GB
- **网络带宽**: 3,200 Gbps (EFAv3)
- **EBS 带宽**: 100 Gbps
- **实例存储**: 8 x 3.8TB NVMe SSD (30.4 TB)
- **发布时间**: 2024年
- **Workload类型**: 训练/推理
- **适用场景**: 大模型训练(100B-1T参数)、超大模型推理(70B-480B参数)、分布式训练
- **价格参考** (us-east-1):
  - 按需: ~$63.30/小时

#### p5e.48xlarge
- **EC2 实例名称**: p5e.48xlarge
- **GPU 型号**: NVIDIA H200 Tensor Core GPU
- **GPU 数量**: 8
- **每GPU显存**: 141GB HBM3e
- **GPU 显存带宽**: 4.8 TB/s (每GPU)
- **vCPU**: 192 (AMD EPYC 第3代)
- **系统内存**: 2,048 GB
- **网络带宽**: 1,600 Gbps (EFA)
- **EBS 带宽**: 80 Gbps
- **实例存储**: 8 x 3.8TB NVMe SSD
- **发布时间**: 2024年
- **Workload类型**: 训练/推理
- **适用场景**: 超大模型推理(>100B参数)、高显存训练
- **价格参考** (us-east-1):
  - 按需: ~$68.00/小时

#### p5.48xlarge
- **EC2 实例名称**: p5.48xlarge
- **GPU 型号**: NVIDIA H100 Tensor Core GPU
- **GPU 数量**: 8
- **每GPU显存**: 80GB HBM3
- **GPU 显存带宽**: 3.35 TB/s (每GPU)
- **vCPU**: 192 (AMD EPYC 第3代)
- **系统内存**: 2,048 GB
- **网络带宽**: 3,200 Gbps (EFA v2)
- **EBS 带宽**: 80 Gbps
- **实例存储**: 8 x 3.8TB NVMe SSD
- **发布时间**: 2023年
- **Workload类型**: 训练/推理
- **适用场景**: 通用大规模训练(10B-100B参数)、中大型推理(20B-70B参数)、AI研发、HPC
- **价格参考** (us-east-1):
  - 按需: ~$58.00/小时
  - Spot: ~$17.40/小时
  - 1年预留: ~$38.50/小时

---

### P4 系列（NVIDIA A100）- Global

#### p4d.24xlarge
- **EC2 实例名称**: p4d.24xlarge
- **GPU 型号**: NVIDIA A100 Tensor Core GPU (40GB)
- **GPU 数量**: 8
- **每GPU显存**: 40GB HBM2
- **GPU 显存带宽**: 1.6 TB/s (每GPU)
- **vCPU**: 96 (Intel Xeon Scalable)
- **系统内存**: 1,152 GB
- **网络带宽**: 400 Gbps (EFA)
- **EBS 带宽**: 19 Gbps
- **实例存储**: 8 x 1TB NVMe SSD
- **发布时间**: 2020年
- **Workload类型**: 训练/推理
- **适用场景**: 预算有限的训练、中小型模型(<20B参数)、研发测试
- **价格参考** (us-east-1):
  - 按需: ~$32.77/小时
  - Spot: ~$9.83/小时
  - 3年预留: ~$18.50/小时

#### p4de.24xlarge
- **EC2 实例名称**: p4de.24xlarge
- **GPU 型号**: NVIDIA A100 Tensor Core GPU (80GB)
- **GPU 数量**: 8
- **每GPU显存**: 80GB HBM2e
- **vCPU**: 96
- **系统内存**: 1,152 GB
- **网络带宽**: 400 Gbps (EFA)
- **发布时间**: 2020年
- **Workload类型**: 训练/推理
- **适用场景**: 需要更大显存的A100场景
- **价格参考** (us-east-1):
  - 按需: ~$40.97/小时

---

### P3 系列（NVIDIA V100）- Global, China

#### p3.2xlarge
- **EC2 实例名称**: p3.2xlarge
- **GPU 型号**: NVIDIA Tesla V100
- **GPU 数量**: 1
- **每GPU显存**: 16GB HBM2
- **vCPU**: 8
- **系统内存**: 61 GB
- **网络带宽**: 最高 10 Gbps
- **价格参考**: ~$3.06/小时

#### p3.8xlarge
- **EC2 实例名称**: p3.8xlarge
- **GPU 型号**: NVIDIA Tesla V100
- **GPU 数量**: 4
- **每GPU显存**: 16GB HBM2
- **vCPU**: 32
- **系统内存**: 244 GB
- **网络带宽**: 10 Gbps
- **价格参考**: ~$12.24/小时

#### p3.16xlarge
- **EC2 实例名称**: p3.16xlarge
- **GPU 型号**: NVIDIA Tesla V100
- **GPU 数量**: 8
- **每GPU显存**: 16GB HBM2
- **vCPU**: 64
- **系统内存**: 488 GB
- **网络带宽**: 25 Gbps
- **发布时间**: 2017年
- **Workload类型**: 训练/推理
- **适用场景**: 传统深度学习、教学、成本敏感场景
- **价格参考**: ~$24.48/小时
- **状态**: 老一代，不推荐新项目

#### p3dn.24xlarge
- **EC2 实例名称**: p3dn.24xlarge
- **GPU 型号**: NVIDIA Tesla V100 (32GB)
- **GPU 数量**: 8
- **每GPU显存**: 32GB HBM2
- **vCPU**: 96
- **系统内存**: 768 GB
- **网络带宽**: 100 Gbps
- **实例存储**: 2 x 900GB NVMe SSD
- **价格参考**: ~$31.21/小时

---

### H20 系列（NVIDIA H20）- China

#### H20(光环)
- **EC2 实例名称**: H20(光环)
- **GPU 型号**: NVIDIA H20
- **GPU 数量**: 8
- **每GPU显存**: 96GB
- **vCPU**: 2
- **系统内存**: 2,048 GB
- **网络带宽**: 20Mb/月起
- **实例存储**: 4 × 3.84TB NVMe SSD
- **发布时间**: 2025年
- **Workload类型**: 训练/推理
- **适用场景**: Qwen 235B/32B/30B、中小尺寸模型、行业专属模型
- **价格参考**: 销售询价
- **网络接入**: DX 专线、互联网、VPN
- **交付时间**: 约 2 周
- **供应商**: 光环新网

#### H20(西云)
- **EC2 实例名称**: H20(西云)
- **GPU 型号**: NVIDIA H20
- **GPU 数量**: 8
- **每GPU显存**: 141GB
- **vCPU**: 2
- **系统内存**: 2,048 GB
- **网络带宽**: 20Mb/月起
- **实例存储**: 4 × 3.84TB NVMe SSD
- **发布时间**: 2025年
- **Workload类型**: 训练/推理
- **适用场景**: DeepSeek、Kimi K2 等大模型（单台即可运行满血版）
- **价格参考**: 销售询价
- **网络接入**: DX 专线、互联网、VPN
- **交付时间**: 约 2 周
- **供应商**: 西云算力

---

## G 系列 - 图形密集型实例

### G6 系列（NVIDIA L4/L40S） - Global

#### g6.xlarge
- **EC2 实例名称**: g6.xlarge
- **GPU 型号**: NVIDIA L4 Tensor Core GPU
- **GPU 数量**: 1
- **每GPU显存**: 24GB GDDR6
- **vCPU**: 4
- **系统内存**: 16 GB
- **网络带宽**: 最高 10 Gbps
- **EBS 带宽**: 最高 10 Gbps
- **发布时间**: 2024年
- **Workload类型**: 推理
- **适用场景**: AI视频生成、实时推理、虚拟工作站、图形渲染
- **价格参考**: ~$1.16/小时

#### g6.2xlarge
- **EC2 实例名称**: g6.2xlarge
- **GPU 型号**: NVIDIA L4
- **GPU 数量**: 1
- **每GPU显存**: 24GB GDDR6
- **vCPU**: 8
- **系统内存**: 32 GB
- **价格参考**: ~$1.52/小时

#### g6.48xlarge
- **EC2 实例名称**: g6.48xlarge
- **GPU 型号**: NVIDIA L4
- **GPU 数量**: 8
- **每GPU显存**: 24GB GDDR6
- **vCPU**: 192
- **系统内存**: 768 GB
- **价格参考**: ~$9.28/小时

---

### G6e 系列（NVIDIA L40S）- Global

#### g6e.xlarge
- **EC2 实例名称**: g6e.xlarge
- **GPU 型号**: NVIDIA L40S Tensor Core GPU
- **GPU 数量**: 1
- **每GPU显存**: 48GB GDDR6
- **vCPU**: 4
- **系统内存**: 32 GB
- **网络带宽**: 最高 20 Gbps
- **EBS 带宽**: 最高 5 Gbps
- **实例存储**: 250GB NVMe SSD
- **发布时间**: 2024年
- **Workload类型**: 推理
- **适用场景**: 大模型推理(13B参数)、AI视频生成、空间计算、3D渲染
- **价格参考**: ~$1.86/小时

#### g6e.2xlarge
- **EC2 实例名称**: g6e.2xlarge
- **GPU 型号**: NVIDIA L40S
- **GPU 数量**: 1
- **每GPU显存**: 48GB GDDR6
- **vCPU**: 8
- **系统内存**: 64 GB
- **网络带宽**: 最高 20 Gbps
- **价格参考**: ~$2.24/小时

#### g6e.48xlarge
- **EC2 实例名称**: g6e.48xlarge
- **GPU 型号**: NVIDIA L40S
- **GPU 数量**: 8
- **每GPU显存**: 48GB GDDR6
- **vCPU**: 192
- **系统内存**: 1,536 GB
- **网络带宽**: 400 Gbps
- **EBS 带宽**: 60 Gbps
- **实例存储**: 7.6TB NVMe SSD
- **发布时间**: 2024年
- **Workload类型**: 推理
- **适用场景**: 大规模AI推理、空间计算、数字孪生、高性能3D渲染
- **价格参考**: ~$30.13/小时

---

### G5 系列（NVIDIA A10G） - Global, China

#### g5.xlarge
- **EC2 实例名称**: g5.xlarge
- **GPU 型号**: NVIDIA A10G Tensor Core GPU
- **GPU 数量**: 1
- **每GPU显存**: 24GB GDDR6
- **vCPU**: 4
- **系统内存**: 16 GB
- **网络带宽**: 最高 10 Gbps
- **EBS 带宽**: 最高 10 Gbps
- **发布时间**: 2021年
- **Workload类型**: 推理
- **适用场景**: 小模型实时推理(<20B)、图形渲染、视频转码、虚拟桌面、游戏流式传输
- **价格参考**: ~$1.006/小时
- **Spot 价格**: ~$0.30/小时

#### g5.2xlarge
- **EC2 实例名称**: g5.2xlarge
- **GPU 型号**: NVIDIA A10G
- **GPU 数量**: 1
- **每GPU显存**: 24GB GDDR6
- **vCPU**: 8
- **系统内存**: 32 GB
- **价格参考**: ~$1.212/小时

#### g5.4xlarge
- **EC2 实例名称**: g5.4xlarge
- **GPU 型号**: NVIDIA A10G
- **GPU 数量**: 1
- **每GPU显存**: 24GB GDDR6
- **vCPU**: 16
- **系统内存**: 64 GB
- **价格参考**: ~$1.624/小时

#### g5.12xlarge
- **EC2 实例名称**: g5.12xlarge
- **GPU 型号**: NVIDIA A10G
- **GPU 数量**: 4
- **每GPU显存**: 24GB GDDR6
- **vCPU**: 48
- **系统内存**: 192 GB
- **价格参考**: ~$5.672/小时

#### g5.48xlarge
- **EC2 实例名称**: g5.48xlarge
- **GPU 型号**: NVIDIA A10G
- **GPU 数量**: 8
- **每GPU显存**: 24GB GDDR6
- **vCPU**: 192
- **系统内存**: 768 GB
- **价格参考**: ~$16.288/小时

---

### G5g 系列（NVIDIA T4G + AWS Graviton2）- Global

#### g5g.xlarge
- **EC2 实例名称**: g5g.xlarge
- **GPU 型号**: NVIDIA T4G Tensor Core GPU
- **GPU 数量**: 1
- **每GPU显存**: 16GB GDDR6
- **总显存**: 16 GB
- **vCPU**: 4 (AWS Graviton2)
- **系统内存**: 8 GB
- **网络带宽**: 最高 10 Gbps
- **发布时间**: 2021年
- **适用场景**: Android 游戏流、ARM 原生应用、移动游戏、成本优化推理
- **价格参考**: ~$0.42/小时

#### g5g.2xlarge
- **EC2 实例名称**: g5g.2xlarge
- **GPU 数量**: 1
- **vCPU**: 8
- **系统内存**: 16 GB
- **价格参考**: ~$0.556/小时

#### g5g.4xlarge
- **EC2 实例名称**: g5g.4xlarge
- **GPU 数量**: 1
- **vCPU**: 16
- **系统内存**: 32 GB
- **价格参考**: ~$0.828/小时

#### g5g.8xlarge
- **EC2 实例名称**: g5g.8xlarge
- **GPU 数量**: 1
- **vCPU**: 32
- **系统内存**: 64 GB
- **价格参考**: ~$1.372/小时

#### g5g.16xlarge
- **EC2 实例名称**: g5g.16xlarge
- **GPU 数量**: 2
- **vCPU**: 64
- **系统内存**: 128 GB
- **价格参考**: ~$2.744/小时

---

### G4dn 系列（NVIDIA T4） - Global, China

#### g4dn.xlarge
- **EC2 实例名称**: g4dn.xlarge
- **GPU 型号**: NVIDIA T4 Tensor Core GPU
- **GPU 数量**: 1
- **每GPU显存**: 16GB GDDR6
- **vCPU**: 4
- **系统内存**: 16 GB
- **网络带宽**: 最高 25 Gbps
- **实例存储**: 125GB NVMe SSD
- **发布时间**: 2019年
- **Workload类型**: 推理
- **适用场景**: 经济型推理、小模型部署、开发测试、视频转码
- **价格参考**: ~$0.526/小时
- **Spot 价格**: ~$0.16/小时

#### g4dn.2xlarge
- **EC2 实例名称**: g4dn.2xlarge
- **GPU 型号**: NVIDIA T4
- **GPU 数量**: 1
- **每GPU显存**: 16GB GDDR6
- **vCPU**: 8
- **系统内存**: 32 GB
- **实例存储**: 225GB NVMe SSD
- **价格参考**: ~$0.752/小时

#### g4dn.12xlarge
- **EC2 实例名称**: g4dn.12xlarge
- **GPU 型号**: NVIDIA T4
- **GPU 数量**: 4
- **每GPU显存**: 16GB GDDR6
- **vCPU**: 48
- **系统内存**: 192 GB
- **实例存储**: 900GB NVMe SSD
- **价格参考**: ~$3.912/小时

---

## Inf 系列 - AWS Inferentia 推理加速器

### Inf2 系列 - Global

#### inf2.xlarge
- **EC2 实例名称**: inf2.xlarge
- **加速器**: AWS Inferentia2 芯片
- **加速器数量**: 1
- **vCPU**: 4
- **系统内存**: 16 GB
- **网络带宽**: 最高 15 Gbps
- **发布时间**: 2022年
- **Workload类型**: 推理
- **适用场景**: 小模型批量推理(<20B)、Transformer模型、BERT、DistilBERT
- **价格参考**: ~$0.76/小时
- **成本优势**: 比G5节省50%推理成本

#### inf2.8xlarge
- **EC2 实例名称**: inf2.8xlarge
- **加速器数量**: 1
- **vCPU**: 32
- **系统内存**: 64 GB
- **价格参考**: ~$1.97/小时

#### inf2.24xlarge
- **EC2 实例名称**: inf2.24xlarge
- **加速器数量**: 6
- **vCPU**: 96
- **系统内存**: 192 GB
- **价格参考**: ~$6.49/小时

#### inf2.48xlarge
- **EC2 实例名称**: inf2.48xlarge
- **加速器数量**: 12
- **vCPU**: 192
- **系统内存**: 384 GB
- **价格参考**: ~$12.98/小时

---

### Inf1 系列 - Global, China

#### inf1.xlarge
- **EC2 实例名称**: inf1.xlarge
- **加速器**: AWS Inferentia (第一代)
- **加速器数量**: 1
- **vCPU**: 4
- **系统内存**: 8 GB
- **价格参考**: ~$0.368/小时
- **状态**: 建议升级到 Inf2

#### inf1.2xlarge
- **EC2 实例名称**: inf1.2xlarge
- **加速器数量**: 1
- **vCPU**: 8
- **系统内存**: 16 GB
- **价格参考**: ~$0.584/小时

---

## Trn 系列 - AWS Trainium 训练加速器

### Trn2 系列 - Global

#### trn2.48xlarge
- **EC2 实例名称**: trn2.48xlarge
- **加速器**: AWS Trainium2 (第二代)
- **加速器数量**: 16
- **加速器内存**: 1.5TB HBM
- **vCPU**: 192
- **系统内存**: 2TB
- **网络带宽**: 3.2 Tbps (EFA v3)
- **实例存储**: 4 x 1.92TB NVMe SSD
- **发布时间**: 2024年
- **Workload类型**: 训练 + 推理
- **适用场景**: 万亿参数级模型训练和推理、生成式AI
- **价格参考**: ~$35.76/小时 (Capacity Blocks)
- **性能提升**: 比Trn1快4倍,内存带宽4倍,内存容量3倍
- **计算能力**: 20.8 petaflops FP8


### Trn1 系列 - Global

#### trn1.2xlarge
- **EC2 实例名称**: trn1.2xlarge
- **加速器**: AWS Trainium (第一代)
- **加速器数量**: 1
- **加速器内存**: 32GB
- **vCPU**: 8
- **系统内存**: 32 GB
- **网络带宽**: 最高 12.5 Gbps
- **EBS 带宽**: 最高 10 Gbps
- **价格参考**: ~$1.34/小时

#### trn1.32xlarge
- **EC2 实例名称**: trn1.32xlarge
- **加速器数量**: 16
- **加速器内存**: 512GB (总)
- **vCPU**: 128
- **系统内存**: 512 GB
- **网络带宽**: 800 Gbps (EFA)
- **实例存储**: 2TB NVMe SSD
- **发布时间**: 2022年
- **Workload类型**: 训练
- **适用场景**: 中大型模型训练、NLP模型(BERT、GPT等)
- **价格参考**: ~$21.50/小时
- **成本优势**: 比P4节省30%训练成本

#### trn1n.32xlarge
- **EC2 实例名称**: trn1n.32xlarge
- **加速器数量**: 16
- **加速器内存**: 512GB
- **vCPU**: 128
- **系统内存**: 512 GB
- **网络带宽**: 1,600 Gbps (EFA) - 增强网络
- **Workload类型**: 训练
- **适用场景**: 分布式训练
- **价格参考**: ~$24.78/小时

---

## 按场景

### AI 训练场景

| 模型规模 | 首选实例 | 备选实例 | 经济型 | 中国区域 |
|---------|---------|---------|--------|---------|
| 超大模型 (>1T) | p6.48xlarge | p5en.48xlarge | - | H20(光环) |
| 大型模型 (100B-1T) | p5en.48xlarge | p5.48xlarge | p4d.24xlarge | H20(光环) |
| 中型模型 (10B-100B) | p5.48xlarge | p4d.24xlarge | trn1.32xlarge | H20(西云) |
| 小型模型 (<10B) | p4d.24xlarge | trn1.32xlarge | p3.16xlarge | H20(西云) |

### AI 推理场景

| 模型规模 | 实时推理 | 批量推理 | 中国区域 |
|---------|---------|---------|---------|
| 超大 (70B-480B+) | p5en.48xlarge | p5e.48xlarge | H20(光环) |
| 中大 (20B-70B) | p5.48xlarge | p4d.24xlarge | H20(光环) |
| 中型 (7B-20B) | g6e.xlarge | g6e.2xlarge | H20(西云) |
| 小型 (<7B) | g5.xlarge | inf2.xlarge | H20(西云) |

### 图形渲染场景

| 应用类型 | 推荐实例 |
|---------|---------|
| 顶级渲染 | g6e.xlarge, g6e.48xlarge |
| 高端渲染 | g6.xlarge, g6.48xlarge |
| 通用渲染 | g5.xlarge, g5.12xlarge |
| 经济型 | g4dn.xlarge |
---

## 性能对比

### 训练性能排序（相对分数）

1. p6.48xlarge (B200): 100
2. p5en.48xlarge (H200): 95
3. p5e.48xlarge (H200): 93
4. p5.48xlarge (H100): 90
5. p4d.24xlarge (A100): 75
6. trn1.32xlarge: 72
7. p3.16xlarge (V100): 60

### 推理性能排序（相对分数）

1. p6.48xlarge: 100
2. p5en.48xlarge: 95
3. p5.48xlarge: 90
4. p4d.24xlarge: 75
5. g6e.xlarge: 72
6. g6.xlarge: 70
7. g5.xlarge: 68
8. inf2.xlarge: 65
9. g4dn.xlarge: 55

### 中国区域H20系列对比

| 特性 | H20(光环) | H20(西云) |
|------|---------|---------|
| 每GPU显存 | 141GB | 96GB |
| GPU数量 | 8 | 8 |
| 适合模型规模 | 235B+ | 70B-235B |
| 主要用途 | 超大模型训练/推理 | 大模型推理 |
| 价格 | 销售询价 | 销售询价 |
| 成本效率 | 高 | 中等 |
| 发布时间 | 2025 | 2025 |

### G6e vs G6 vs G5 对比

| 特性 | G6e (L40S) | G6 (L4) | G5 (A10G) |
|------|------------|---------|-----------|
| 每GPU显存 | 48GB | 24GB | 24GB |
| 显存带宽 | 864 GB/s | 300 GB/s | 600 GB/s |
| 适合模型规模 | 7B-20B | 3B-7B | 3B-7B |
| 推理性能 | 最高 | 中等 | 中等 |
| 成本效率 | 高 | 最高 | 中等 |
| 发布时间 | 2024 | 2024 | 2021 |

---

## 数据来源

- AWS EC2 官方文档: https://aws.amazon.com/ec2/instance-types/
- AWS 定价页面: https://aws.amazon.com/ec2/pricing/
- NVIDIA GPU 规格: https://www.nvidia.com/data-center/
