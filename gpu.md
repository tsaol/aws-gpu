# AWS GPU 实例详细信息

> 最后更新: 2026-01-21
> 数据来源: [instances.vantage.sh](https://instances.vantage.sh/)

## 目录

- [P 系列（训练型）](#p-系列)
- [G 系列（推理/图形）](#g-系列)
- [Inferentia 系列（推理）](#inf-系列)
- [Trainium 系列（训练）](#trn-系列)

---

### P 系列（训练型）

#### p6e-gb200.36xlarge
- **EC2 实例名称**: p6e-gb200.36xlarge
- **GPU 型号**: NVIDIA GB200 Grace Blackwell
- **GPU 数量**: 4
- **每GPU显存**: 740 GB HBM3e
- **vCPU**: 144
- **系统内存**: 960 GiB
- **网络带宽**: 1600 Gbps EFAv4
- **存储**: 22.5 TB NVMe SSD
- **发布时间**: 2025年

#### p6-b300.48xlarge
- **EC2 实例名称**: p6-b300.48xlarge
- **GPU 型号**: NVIDIA B300 Blackwell
- **GPU 数量**: 8
- **每GPU显存**: 262 GB HBM3e
- **vCPU**: 192
- **系统内存**: 4096 GB
- **网络带宽**: 6400 Gigabit
- **存储**: 3800 GB (8 × 475 GB SSD)
- **发布时间**: 2025年
- **Workload类型**: 训练/推理
- **适用场景**: 顶级训练性能、需要更大系统内存的场景
- **特性**: NVLink 5、第五代 Tensor Core、更大系统内存

#### p6-b200.48xlarge
- **EC2 实例名称**: p6-b200.48xlarge
- **GPU 型号**: NVIDIA B200 Blackwell
- **GPU 数量**: 8
- **每GPU显存**: 180 GB HBM3e
- **vCPU**: 192
- **系统内存**: 2048 GiB
- **网络带宽**: 3200 Gbps EFAv4
- **存储**: 8 x 3.84 TB NVMe SSD
- **发布时间**: 2025年
- **Workload类型**: 训练/推理
- **适用场景**: 下一代 AI 训练、超大模型推理、科学计算
- **特性**: NVLink 5、第五代 Tensor Core、8 TB/s 显存带宽
- **价格参考**: ~$113.93/小时

#### p5en.48xlarge
- **EC2 实例名称**: p5en.48xlarge
- **GPU 型号**: NVIDIA H200
- **GPU 数量**: 8
- **每GPU显存**: 141 GB HBM3e
- **vCPU**: 192
- **系统内存**: 2048 GiB
- **网络带宽**: 3200 Gbps EFAv3
- **存储**: 8 x 3.84 TB NVMe SSD
- **发布时间**: 2024年
- **Workload类型**: 训练/推理
- **适用场景**: 大规模 LLM 训练、高性能推理、分布式训练
- **特性**: EFAv3 网络、3200 Gbps 带宽、NVLink 4
- **价格参考**: ~$63.30/小时

#### p5e.48xlarge
- **EC2 实例名称**: p5e.48xlarge
- **GPU 型号**: NVIDIA H200
- **GPU 数量**: 8
- **每GPU显存**: 141 GB HBM3e
- **vCPU**: 192
- **系统内存**: 2048 GiB
- **网络带宽**: 3200 Gbps EFAv2
- **存储**: 8 x 3.84 TB NVMe SSD
- **发布时间**: 2024年
- **Workload类型**: 训练/推理
- **适用场景**: 大模型训练、高性能推理
- **特性**: EFA 网络、1600 Gbps 带宽

#### p5.48xlarge
- **EC2 实例名称**: p5.48xlarge
- **GPU 型号**: NVIDIA H100
- **GPU 数量**: 8
- **每GPU显存**: 80 GB HBM3
- **vCPU**: 192
- **系统内存**: 2048 GiB
- **网络带宽**: 3200 Gbps EFAv2
- **存储**: 8 x 3.84 TB NVMe SSD
- **发布时间**: 2023年
- **Workload类型**: 训练/推理
- **适用场景**: 大规模 LLM 训练、生成式 AI、科学计算
- **特性**: EFAv2 网络、3200 Gbps 带宽、NVLink 4
- **价格参考**: ~$55.04/小时

#### p4de.24xlarge
- **EC2 实例名称**: p4de.24xlarge
- **GPU 型号**: NVIDIA A100
- **GPU 数量**: 8
- **每GPU显存**: 80 GB HBM2e
- **vCPU**: 96
- **系统内存**: 1152 GiB
- **网络带宽**: 400 Gbps EFA
- **存储**: 8 x 1 TB NVMe SSD
- **发布时间**: 2021年
- **Workload类型**: 训练
- **适用场景**: 大模型训练、需要更大显存的场景
- **特性**: 80GB 显存、EFA 网络、NVLink
- **价格参考**: ~$27.45/小时

#### p4d.24xlarge
- **EC2 实例名称**: p4d.24xlarge
- **GPU 型号**: NVIDIA A100
- **GPU 数量**: 8
- **每GPU显存**: 40 GB HBM2
- **vCPU**: 96
- **系统内存**: 1152 GiB
- **网络带宽**: 400 Gbps EFA
- **存储**: 8 x 1 TB NVMe SSD
- **发布时间**: 2020年
- **Workload类型**: 训练
- **适用场景**: ML/DL 训练、自然语言处理、计算机视觉
- **特性**: EFA 网络、400 Gbps 带宽、NVLink
- **价格参考**: ~$21.96/小时

#### p3dn.24xlarge
- **EC2 实例名称**: p3dn.24xlarge
- **GPU 型号**: NVIDIA V100
- **GPU 数量**: 8
- **每GPU显存**: 32 GB HBM2
- **vCPU**: 96
- **系统内存**: 768 GB
- **网络带宽**: 100 Gigabit
- **存储**: 900 GB (2 × 450 GB SSD)
- **发布时间**: 2018年
- **价格参考**: ~$31.21/小时

#### p3.16xlarge
- **EC2 实例名称**: p3.16xlarge
- **GPU 型号**: NVIDIA V100
- **GPU 数量**: 8
- **每GPU显存**: 16 GB HBM2
- **vCPU**: 64
- **系统内存**: 488 GB
- **网络带宽**: 25 Gigabit
- **存储**: EBS Only
- **发布时间**: 2017年
- **价格参考**: ~$24.48/小时

#### p2.16xlarge
- **EC2 实例名称**: p2.16xlarge
- **GPU 型号**: NVIDIA K80
- **GPU 数量**: 8
- **每GPU显存**: 12 GB GDDR5
- **vCPU**: 64
- **系统内存**: 732 GB
- **网络带宽**: 20 Gigabit
- **存储**: EBS Only
- **发布时间**: 2016年
- **价格参考**: ~$14.40/小时

---

### G 系列（推理/图形）

#### g7e.12xlarge
- **EC2 实例名称**: g7e.12xlarge
- **GPU 型号**: NVIDIA RTX PRO 6000 Blackwell
- **GPU 数量**: 2
- **每GPU显存**: 96 GB GDDR7
- **vCPU**: 48
- **系统内存**: 512 GB
- **网络带宽**: 400 Gigabit
- **存储**: 3800 GB SSD
- **发布时间**: 2025年
- **价格参考**: ~$8.29/小时

#### g6e.12xlarge
- **EC2 实例名称**: g6e.12xlarge
- **GPU 型号**: NVIDIA L40S
- **GPU 数量**: 4
- **每GPU显存**: 48 GB GDDR6
- **vCPU**: 48
- **系统内存**: 384 GB
- **网络带宽**: 100 Gigabit
- **存储**: 1900 GB (2 × 950 GB SSD)
- **发布时间**: 2024年
- **Workload类型**: 推理
- **适用场景**: 大模型推理(13B参数)、AI视频生成、3D渲染
- **特性**: L40S GPU、48GB 显存、第四代 Tensor Core
- **价格参考**: ~$10.49/小时

#### g6.12xlarge
- **EC2 实例名称**: g6.12xlarge
- **GPU 型号**: NVIDIA L4
- **GPU 数量**: 4
- **每GPU显存**: 24 GB GDDR6
- **vCPU**: 48
- **系统内存**: 192 GB
- **网络带宽**: 40 Gigabit
- **存储**: 940 GB (4 × 235 GB SSD)
- **发布时间**: 2023年
- **Workload类型**: 推理
- **适用场景**: 成本优化推理、视频转码、图形渲染
- **特性**: L4 GPU、24GB 显存、性价比高
- **价格参考**: ~$4.60/小时

#### g5g.16xlarge
- **EC2 实例名称**: g5g.16xlarge
- **GPU 型号**: ARM Mali-G78MP12
- **GPU 数量**: 2
- **每GPU显存**: 4 GB
- **vCPU**: 64
- **系统内存**: 128 GB
- **网络带宽**: 25 Gigabit
- **存储**: EBS Only
- **发布时间**: 2021年
- **价格参考**: ~$2.74/小时

#### g5.12xlarge
- **EC2 实例名称**: g5.12xlarge
- **GPU 型号**: NVIDIA A10G
- **GPU 数量**: 4
- **每GPU显存**: 24 GB GDDR6
- **vCPU**: 48
- **系统内存**: 192 GB
- **网络带宽**: 40 Gigabit
- **存储**: 3800 GB SSD
- **发布时间**: 2021年
- **Workload类型**: 推理
- **适用场景**: ML 推理、图形渲染、游戏流
- **特性**: A10G GPU、24GB 显存、高性价比
- **价格参考**: ~$5.67/小时

#### g4ad.16xlarge
- **EC2 实例名称**: g4ad.16xlarge
- **GPU 型号**: AMD Radeon Pro V520
- **GPU 数量**: 4
- **每GPU显存**: 8 GB GDDR6
- **vCPU**: 64
- **系统内存**: 256 GB
- **网络带宽**: 25 Gigabit
- **存储**: 1200 GB (2 × 600 GB SSD)
- **发布时间**: 2020年
- **价格参考**: ~$3.47/小时

#### g4dn.12xlarge
- **EC2 实例名称**: g4dn.12xlarge
- **GPU 型号**: NVIDIA T4
- **GPU 数量**: 4
- **每GPU显存**: 16 GB GDDR6
- **vCPU**: 48
- **系统内存**: 192 GB
- **网络带宽**: 50 Gigabit
- **存储**: 900 GB SSD
- **发布时间**: 2019年
- **价格参考**: ~$3.91/小时

---

### Inferentia 系列（推理）

#### inf2.24xlarge
- **EC2 实例名称**: inf2.24xlarge
- **GPU 型号**: AWS Inferentia2
- **GPU 数量**: 6
- **每GPU显存**: 32 GB HBM
- **vCPU**: 96
- **系统内存**: 384 GB
- **网络带宽**: 50 Gigabit
- **存储**: EBS Only
- **发布时间**: 2023年
- **价格参考**: ~$6.49/小时

#### inf1.24xlarge
- **EC2 实例名称**: inf1.24xlarge
- **GPU 型号**: AWS Inferentia
- **GPU 数量**: 16
- **每GPU显存**: 8 GB
- **vCPU**: 96
- **系统内存**: 192 GB
- **网络带宽**: 100 Gigabit
- **存储**: EBS Only
- **发布时间**: 2019年
- **价格参考**: ~$4.72/小时

---

### Trainium 系列（训练）

#### trn2.48xlarge
- **EC2 实例名称**: trn2.48xlarge
- **GPU 型号**: AWS Trainium2
- **GPU 数量**: 16
- **每GPU显存**: 96 GB HBM3
- **vCPU**: 192
- **系统内存**: 2048 GB
- **网络带宽**: 16x 200 Gigabit
- **存储**: 1900 GB (4 × 475 GB SSD)
- **发布时间**: 2024年

#### trn1n.32xlarge
- **EC2 实例名称**: trn1n.32xlarge
- **GPU 型号**: AWS Trainium
- **GPU 数量**: 16
- **每GPU显存**: Unknown
- **vCPU**: 128
- **系统内存**: 512 GB
- **网络带宽**: 16x 100 Gigabit
- **存储**: 1900 GB (4 × 475 GB SSD)
- **发布时间**: 2023年
- **价格参考**: ~$24.78/小时

#### trn1.2xlarge
- **EC2 实例名称**: trn1.2xlarge
- **GPU 型号**: AWS Trainium
- **GPU 数量**: 1
- **每GPU显存**: 32 GB HBM
- **vCPU**: 8
- **系统内存**: 32 GB
- **网络带宽**: Up to 12.5 Gigabit
- **存储**: 474 GB SSD
- **发布时间**: 2022年
- **价格参考**: ~$1.34/小时

---

## 注意事项

- 价格为 us-east-1 区域按需价格参考，实际以 AWS 官网为准
- GPU 显存、网络带宽等规格可能因实例大小而异
- 部分新实例可能处于预览状态，可用区域有限
