import numpy as np
import cv2
from scipy.special import gamma
#产生二维高斯核函数
#这个函数参考自：https://blog.csdn.net/qq_16013649/article/details/78784791
def gaussian_2d_kernel(kernel_size, sigma):
    kernel = np.zeros((kernel_size, kernel_size))
    center = kernel_size // 2
    if sigma == 0:
        sigma = ((kernel_size - 1) * 0.5 - 1) * 0.3 + 0.8
    s = 2 * (sigma ** 2)
    sum_val = 0
    for i in range(0, kernel_size):
        for j in range(0, kernel_size):
            x = i - center
            y = j - center
            kernel[i, j] = np.exp(-(x ** 2 + y ** 2) / s)
            sum_val += kernel[i, j]
    sum_val = 1 / sum_val
    return kernel * sum_val

#相关操作
def correlation(img,kernal):
    kernal_heigh = kernal.shape[0]
    kernal_width = kernal.shape[1]
    h = kernal_heigh // 2
    w = kernal_width // 2
    # 边界补全
    img = np.pad(img, ((h, h), (w, w)), 'constant')
    cor_heigh = img.shape[0] - kernal_heigh + 1
    cor_width = img.shape[1] - kernal_width + 1
    result = np.zeros((cor_heigh, cor_width), dtype=np.float64)
    for i in range(cor_heigh):
        for j in range(cor_width):
            result[i][j] = (img[i:i + kernal_heigh, j:j + kernal_width] * kernal).sum()
    return result

def estimate_GGD_parameters(vec):
    gam =np.arange(0.2,10.0,0.001)#产生候选的γ
    r_gam = (gamma(1/gam)*gamma(3/gam))/((gamma(2/gam))**2)#根据候选的γ计算r(γ)
    sigma_sq=np.mean((vec)**2)
    E=np.mean(np.abs(vec))
    r=sigma_sq/(E**2)#根据sigma^2和E计算r(γ)
    diff=np.abs(r-r_gam)
    gamma_param=gam[np.argmin(diff, axis=0)]
    return [gamma_param,sigma_sq]

def estimate_AGGD_parameters(vec):
    alpha =np.arange(0.2,10.0,0.001)#产生候选的α
    r_alpha=((gamma(2/alpha))**2)/(gamma(1/alpha)*gamma(3/alpha))#根据候选的γ计算r(α)
    sigma_l=np.sqrt(np.mean(vec[vec<0]**2))
    sigma_r=np.sqrt(np.mean(vec[vec>0]**2))
    gamma_=sigma_l/sigma_r
    u2=np.mean(vec**2)
    m1=np.mean(np.abs(vec))
    r_=m1**2/u2
    R_=r_*(gamma_**3+1)*(gamma_+1)/((gamma_**2+1)**2)
    diff=(R_-r_alpha)**2
    alpha_param=alpha[np.argmin(diff, axis=0)]
    const1 = np.sqrt(gamma(1 / alpha_param) / gamma(3 / alpha_param))
    const2 = gamma(2 / alpha_param) / gamma(1 / alpha_param)
    eta =(sigma_r-sigma_l)*const1*const2
    return [alpha_param,eta,sigma_l**2,sigma_r**2]


def brisque_feature(dis_image):
    dis_image=dis_image.astype(np.float32)#类型转换十分重要
    kernal=gaussian_2d_kernel(7,7/6)
    ux=correlation(dis_image,kernal)
    ux_sq=ux*ux
    sigma=np.sqrt(np.abs(correlation(dis_image**2,kernal)-ux_sq))
    mscn=(dis_image-ux)/(1+sigma)
    f1_2=estimate_GGD_parameters(mscn)
    H=mscn*np.roll(mscn,1,axis=1)
    V=mscn*np.roll(mscn,1,axis=0)
    D1=mscn*np.roll(np.roll(mscn,1,axis=1),1,axis=0)
    D2=mscn*np.roll(np.roll(mscn,-1,axis=1),-1,axis=0)
    f3_6=estimate_AGGD_parameters(H)
    f7_10=estimate_AGGD_parameters(V)
    f11_14=estimate_AGGD_parameters(D1)
    f15_18=estimate_AGGD_parameters(D2)
    return f1_2+f3_6+f7_10+f11_14+f15_18
