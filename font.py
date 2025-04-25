import platform
import matplotlib.pyplot as plt

def set_korean_font():
    if platform.system() == 'Windows':
        plt.rc('font', family='Malgun Gothic')
    elif platform.system() == 'Darwin':
        plt.rc('font', family='AppleGothic')
    else:
        plt.rc('font', family='NanumGothic')

    plt.rcParams['axes.unicode_minus'] = False  # 마이너스 깨짐 방지
