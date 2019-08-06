#!/bin/python3

import math
import os
import random
import re
import sys


# Complete the matrixRotation function below.
def matrixRotation(m,n,matrix,r):
    layers=[]

    for i in range(min((m,n)) // 2):

        # Layers loop
        xlim=(i,n - i)
        ylim=(i,m - i)
        layer_length=2 * (m + n - (4 * i)) - 4
        rotate=r % layer_length

        # Unwrap layer
        # Step1:
        list1=[matrix[a][xlim[0]] for a in range(ylim[0],ylim[1])]
        l1=len(list1)
        # Step2:
        list2=matrix[ylim[1] - 1][xlim[0] + 1: xlim[1] - 1]
        l2=len(list2)
        # Step3:
        list3=[matrix[a][xlim[1] - 1] for a in range(ylim[1] - 1,ylim[0] - 1,-1)]
        l3=len(list3)
        # Step4:
        list4=matrix[ylim[0]][xlim[1] - 2: xlim[0]: -1]
        l4=len(list4)

        layer=list1 + list2 + list3 + list4

        # Scroll layer
        scroll(layer,rotate)

        # ReWrap Layer
        # 1
        count=0
        for a in range(ylim[0],ylim[1]):
            matrix[a][xlim[0]]=layer[count]
            count+=1

        # 2
        for a in range(xlim[0] + 1,xlim[1] - 1):
            matrix[ylim[1] - 1][a]=layer[count]
            count+=1

        # 3
        for a in range(ylim[1] - 1,ylim[0] - 1,-1):
            matrix[a][xlim[1] - 1]=layer[count]
            count+=1

        # 4
        for a in range(xlim[1] - 2,xlim[0],-1):
            matrix[ylim[0]][a]=layer[count]
            count+=1

    # print out
    for row in matrix:
        for item in row:
            print(item,end=" ")
        print()


def scroll(l,n):
    for i in range(n):
        prev=l[-1]
        for i in range(len(l)):
            prev,l[i]=l[i],prev


if __name__ == '__main__':
    mnr=input().rstrip().split()

    m=int(mnr[0])

    n=int(mnr[1])

    r=int(mnr[2])

    matrix=[]

    for _ in range(m):
        matrix.append(list(map(int,input().rstrip().split())))

    matrixRotation(m,n,matrix,r)
