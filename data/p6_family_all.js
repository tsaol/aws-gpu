// Auto-generated P6 Family data from instances.vantage.sh
// Last updated: 2025-12-21
// Includes: p6-b200, p6-b300, p6e-gb200

var instanceData = [
  {
    "name": "p6-b200.48xlarge",
    "apiName": "p6-b200.48xlarge",
    "gpu": "NVIDIA B200 Blackwell",
    "gpuCount": 8,
    "gpuMemory": "1432 GB HBM3e",
    "vcpu": 192,
    "memory": "2048 GiB",
    "network": "3200 Gbps EFAv4",
    "storage": "8 x 3.84 TB NVMe SSD",
    "pricing": {
      "us-east-1": {
        "onDemand": 113.9328
      },
      "us-east-1-atl-1": {
        "onDemand": 113.9328
      },
      "us-east-2": {
        "onDemand": 113.9328
      },
      "us-west-2": {
        "onDemand": 113.9328
      }
    },
    "availability": [
      "us-east-1",
      "us-east-1-atl-1",
      "us-east-2",
      "us-west-2"
    ],
    "generation": "current",
    "family": "GPU instance",
    "ebsBandwidth": "100 Gbps",
    "gpuInterconnect": "1800 GB/s NVLink",
    "gpuDirectRDMA": true,
    "source": "merged",
    "isNew": true,
    "year": "2025"
  },
  {
    "name": "p6-b300.48xlarge",
    "apiName": "p6-b300.48xlarge",
    "gpu": "NVIDIA B300 Blackwell",
    "gpuCount": 8,
    "gpuMemory": "192 GB HBM3e",
    "vcpu": 192,
    "memory": "4096 GB",
    "network": "6400 Gigabit",
    "storage": "EBS Only",
    "pricing": {
      "us-west-2": {
        "onDemand": 142.416
      }
    },
    "availability": [
      "us-west-2"
    ],
    "generation": "current",
    "family": "GPU instance",
    "isNew": true,
    "year": "2025"
  },
  {
    "name": "p6e-gb200.36xlarge",
    "apiName": "p6e-gb200.36xlarge",
    "gpu": "NVIDIA GB200 Grace Blackwell",
    "gpuCount": 4,
    "gpuMemory": "740 GB HBM3e",
    "vcpu": 144,
    "memory": "960 GiB",
    "network": "1600 Gbps EFAv4",
    "storage": "22.5 TB NVMe SSD",
    "pricing": {},
    "availability": [],
    "generation": "preview",
    "family": "GPU instance",
    "ebsBandwidth": "60 Gbps",
    "gpuInterconnect": "1800 GB/s NVLink",
    "gpuDirectRDMA": true,
    "source": "merged",
    "isNew": true,
    "year": "2025"
  }
];
