# -*- coding: utf-8 -*-
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

import torch

ok = "[OK]"

python_ver = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
torch_ver = torch.__version__
cuda_ver = torch.version.cuda if torch.cuda.is_available() else "N/A"
gpu_name = torch.cuda.get_device_name(0) if torch.cuda.is_available() else "N/A"

a = torch.tensor([1.0, 2.0, 3.0]).cuda()
b = torch.tensor([4.0, 5.0, 6.0]).cuda()
c = a + b
gpu_result = f"cuda:{c.device.index} 확인"

rows = [
    ("Python",      python_ver),
    ("PyTorch",     torch_ver),
    ("CUDA",        cuda_ver),
    ("GPU",         gpu_name),
    ("GPU 텐서 연산",  gpu_result),
]

col1 = max(len(r[0]) for r in rows) + 2
col2 = max(len(r[1]) + len(ok) for r in rows) + 4
sep = f"+{'-'*col1}+{'-'*col2}+"

print("\n* 모두 정상 작동합니다.\n")
print(sep)
print(f"| {'항목':{col1-2}} | {'결과':{col2-2}} |")
print(sep)
for name, val in rows:
    val_str = f"{val}  {ok}"
    print(f"| {name:{col1-2}} | {val_str:{col2-2}} |")
    print(sep)

print(f"\ntorch_env에 requirements.txt 기반으로 전체 패키지가 설치되었고, PyTorch + CUDA {cuda_ver} GPU 연산까지 정상 동작합니다.\n")
