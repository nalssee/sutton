
import numpy as np
import matplotlib.pyplot as plt

# 20x20 행렬 생성 (-5에서 5까지의 정수)
matrix = np.random.randint(-5, 6, size=(20, 20))

# 등고선 그래프 생성
fig, ax = plt.subplots(figsize=(10, 8))

# discrete colormap 생성
cmap = plt.cm.get_cmap('RdBu_r', 11)  # 11 levels for -5 to 5

# pcolormesh를 사용하여 이산적인 값 표현
mesh = ax.pcolormesh(matrix, cmap=cmap, vmin=-5.5, vmax=5.5)

# 경계선 추가
ax.set_xticks(np.arange(0, 21, 1))
ax.set_yticks(np.arange(0, 21, 1))
ax.grid(True, which='major', color='k', linestyle='-', linewidth=0.5)

ax.set_title('20x20 Discrete Matrix Plot')
ax.set_xlabel('X-axis')
ax.set_ylabel('Y-axis')

# 컬러바 추가 및 설정
cbar = fig.colorbar(mesh, ticks=range(-5, 6))
cbar.set_label('Value')

plt.tight_layout()
plt.show()