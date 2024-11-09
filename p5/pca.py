from scipy.io import loadmat
import numpy as np
from scipy.linalg import eigh
import matplotlib.pyplot as plt


def load_and_center_dataset(filename):
    dataset = loadmat(filename)
    x = dataset['fea']
    x=x.astype('float64')
    x=x - np.mean(x, axis=0)
    return x


def get_covariance(dataset):
    matrix=np.zeros((len(dataset[0]),len(dataset[0])))
    for x in dataset:
        transpose= np.transpose(np.matrix(x))
        cur=np.dot(transpose, np.matrix(x))
        matrix=np.add(cur,matrix)
    
    return matrix/(len(dataset)-1)# the return type is a matrix somehow array plus matrix is a matrix
        


def get_eig(S, m):
    result=eigh(S)
    eigen_vectors=result[1]
    eigen_values=result[0]
    idx = eigen_values.argsort()[::-1]
    eigen_values = eigen_values[idx]
    eigen_vectors = eigen_vectors[:,idx]
    diagonal=np.diag(eigen_values)
    diagonal=diagonal[:m]#slicing
    diagonal=np.transpose(diagonal)
    tpose= np.transpose(np.matrix(eigen_vectors))
    tpose=tpose[:m]
    tpose=np.transpose(tpose)
    
    return diagonal,tpose
def project_image(image, U):
    eigen_vectors=np.matrix(U)
    image=np.matrix(image)
    tpose=np.transpose(eigen_vectors)
    product=np.dot(image, eigen_vectors)
    product=np.dot(product,tpose)
    return product

    
def display_image(orig, proj):
    orig=orig.reshape(32,32)
    proj=proj.reshape(32,32) 
    plt.figure(figsize=(22, 5))
    orig_image=plt.subplot(131)
    orig_image.set_title("Original")
    proj_image=plt.subplot(132)
    proj_image.set_title("Projection")
    colorbar1=orig_image.imshow(np.transpose(orig),aspect='equal')
    colorbar2=proj_image.imshow(np.transpose(proj),aspect='equal')
    plt.colorbar(colorbar1,ax=orig_image)
    plt.colorbar(colorbar2,ax=proj_image)
    
    plt.show()
"""
Spyder Editor

This is a temporary script file.
"""

