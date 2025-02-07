import pyautogui  # Used for getting the current cursor position
from screeninfo import get_monitors  # Fetches monitor information like resolution and dimensions
import base64
import ctypes  # Provides access to Windows API for screen dimensions
import keyboard  # Used for detecting key presses
import subprocess  # Enables running external processes
import psutil  # Used for system and process utilities
import matplotlib.pyplot as plt  # For plotting cursor movement
import tkinter as tk  # GUI library for creating input forms
from tkinter import ttk  # Themed widgets for tkinter
import tempfile  # For creating temporary files
import os  # Provides utilities for interacting with the operating system
import threading  # Used for running tasks in parallel
import time  # For adding delays
import numpy as np

from widgets import ParallelogramSelector

# Initialize AutoHotkey interface
# Retrieve screen dimensions using Windows API
user32 = ctypes.windll.user32
SCREEN_WIDTH = user32.GetSystemMetrics(0)  # Screen width in pixels
SCREEN_HEIGHT = user32.GetSystemMetrics(1)  # Screen height in pixels
# Global variables for tablet dimensions in millimeters
TABLET_WIDTH_MM = 0
TABLET_HEIGHT_MM = 0

ICON = b'''AAABAAEAQEAAAAEAIAAoQgAAFgAAACgAAABAAAAAgAAAAAEAIAAAAAAAAEAAAMMOAADDDgAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAABkVEgAZFBIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgVEgAYFRIAGBUSABgUEgAXFRIAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAQjYzACkgIABIPDgAXU1IAGxbVwC+lHQAuJByAGpZVQBsWFAAjYB8AOrm5QDt6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7OnoAOzp6ADs6egA7enoAPHt7ACyrawAU0lGAAAAAABCNzMAAAAAAAAAAAAAAAAAAAAAADAnJgBRQz8ARDg1UEw/O6dLPjqybVZGsWpURbFKPjqxSz05sVhNSrGCfHuxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfnyxg358sYN+fLGDfn2yc2xqqR8AAFiJfnsAAAAAAAwMDAAAAAAAAAAAAAAAAABHOzcAQjYzQ1VGQf9hUEr/WUtI/8CUb/+6j23/WEtI/1tIQf+Hfnv/8/Pz//b29v/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vX1//b19f/29fX/9vb2//Py8v+zsLD/BQAAUlJIRQAUEwsAAAAAAAAAAAAAAAAATUA8AEo9OY1fTkn/ZFNN/1pMSf/ImXP/wZRw/1lMSf9cSUH/i4OA//7+/v//////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////7Ovr/1xTUJ2Jg4EAEQ8NAAAAAAAAAAAAAAAAAE5BPABLPjqTX09J/2NSTP9aTEn/x5lz/8CTcP9ZTEn/XEhB/4uCf//9/fz//////////////////////////////////////////////////////////////////////////////////v7+//7+/v/+/v7//v7+/////v////7////+//////////7////+///////+/v7//v7+//7+/v/+/v7//////////////////////////////////////////////////////////////////////////////////////+7t7f9nX12gnpeWABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/WkxJ/8eZc//Ak3D/WUxJ/1xIQf+Lgn///f38///////////////////////////////////////////////////////////////////////+/v7//v7+//7+/v/////////////////+/v///Pv///v5/v/6+P7/+/n+//z7///+/v///////////////////v7+//7+/v/+/v7////////////////////////////////////////////////////////////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/1pMSf/HmXP/wJNw/1lMSf9cSEH/i4J///39/P////////////////////////////////////////////////////////////7+/v/+/v7////+////////////+ff+/+rg+//Zx/n/yq72/7+a9P+5j/T/t4r0/7mP9P+8mfL/wqjs/9TD8f/n3/f/+Pb9///////////////+//7+/v/+/v7/////////////////////////////////////////////////////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9aTEn/x5lz/8CTcP9ZTEn/XEhB/4uCf//9/fz///////////////////////////////////////////////////////7+/v/+/v7////////////v6vr/zbrv/7WL7/+rcfP/pWXy/6Vl8f+maPH/p2ry/6hr8v+navL/nV3o/5VS4f+VUuH/nmTm/7GI6//Pu/L/8Or7/////////////v7+//7+/v///////////////////////////////////////////////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/WkxJ/8iZc//BlHD/WUxJ/1xIQf+Lgn///f38//////////////////////////////////////////////////7+/v////////////fz///Mt/D/n2vj/5NN4f+bXOX/qG3x/6pw8v+qcPL/qnDy/6pw8v+rcfP/pmzu/5th4v+bYeP/nGLk/59j5/+cXuf/mFTm/6Nv6P/Kte3/9PH6/////////////v7+///////////////////////////////////////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/1pMSf/ElnH/vZFu/1lMSf9cSEH/i4J///39/P////////////////////////////////////////////7+/v///////////+rd//+4jPT/lFDh/5ld4v+bYuP/m2Hi/6Np6/+qcPL/qnDy/6hu8P+obvD/qG7w/59l5/+bYeP/m2Hj/55k5v+hZ+n/pWvt/6Zt7v+jaOz/m1jo/7GG7v/m2vv////////////+/v7/////////////////////////////////////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9iUUz/dF1R/3NcUf9iUUz/XEhB/4uCf//9/fz///////////////////////////////////////7+/v///////v7//97K/v+zd/z/nF3n/5pg4v+bYeP/m2Hj/5th4/+cYuT/qG7w/6pw8v+jaev/n2Tl/59k5v+fZOb/nWPk/51j5P+gZuj/oGbo/6Zs7v+rcfP/qnDy/6tx8/+oafP/pGjt/9LC7//+/v////////7+/v///////////////////////////////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2BQS/9gUEv/Y1JM/1xIQf+Lgn///f38//////////////////////////////////7+/v///////v7+/8257/+naPL/qGzx/5ph4v+bYeP/m2Hj/5th4/+bYeP/mmDi/6Fn6f+qcfP/qG7w/6Bl5/+fZOb/n2Tm/5xi5P+fZef/oGbo/6Bm6P+hZ+n/qW/x/6pw8v+qcPL/qXDy/5ld4v+QTdz/y7js//7+/////////v7+///////////////////////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P////////////////////////////7+/v///////////9XE8/+WVeL/nGDl/51j5f+bYeP/mV/h/5he4P+YXuD/mF7g/5he4P+bYeP/pm3v/6tx8/+iZ+n/n2Tm/51i5P+dY+X/oGbo/59l5/+fZef/nmTl/6Bn6P+qcPL/q3Hz/6Np6/+WXd7/lVrf/5JP3v/Twu/////////////+/v7/////////////////////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz///////////////////////7+/v/+/v7//////+PZ+P+fYuj/nGDl/5th4/+bYeP/m2Hj/5pg4f+WXN7/llze/5Zc3v+YXuD/mmDi/59m5/+mbe7/nWLk/51i5P+cYuT/oGXn/59l5/+bYeP/m2Hj/5th4/+bYeL/p23v/6lv8f+dY+X/mmDi/5th4/+ZXeL/mVzi/+LZ9v///////v7+//7+/v///////////////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2NSTP9jUkz/Y1JM/1xIQf+Lgn///f38///////////////////////+/v7///////Xy/P+uhOv/nF3n/6Bm6P+cYuT/m2Hj/5th4/+bYeP/mF7g/5Zc3v+XXd//mmDi/5th4/+bYeP/nWPl/5th4/+bYeP/nmTm/6Bm6P+gZuj/nWPl/5th4/+bYeP/mmDi/59m5/+iaOr/m2Hi/5th4/+bYeP/m2Hj/5dX4v+pgOX/9PH6///////+/v7////////////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P/////////////////+/v7////////////NuPH/mVXm/59l5/+gZuj/nmTm/5th4/+bYeP/m2Hj/5pg4v+WXN7/mV/h/5th4/+bYeP/m2Hj/5th4/+bYeP/nGLk/6Bm6P+gZuj/oGbo/59l5/+bYeP/m2Hj/5th4/+bYeP/m2Hj/5th4/+bYeP/m2Hj/5th4/+aYOL/mFTk/8+69P////////////7+/v//////////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz//////////////////v7+///////x6/z/qnXv/6Ro7f+mbO7/pGrs/59m6P+cYuT/m2Hj/5th4/+bYeP/mmDi/5th4/+bYeP/m2Hj/5th4/+bYeP/m2Hj/59k5v+gZuj/oGbo/6Bm6P+cYuT/mF7g/5th4/+bYeP/m2Hj/5th4/+bYeP/m2Hj/5th4/+dY+X/m2Hj/6Jm6/+3gfv/8uz+///////+/v7//////////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2NSTP9jUkz/Y1JM/1xIQf+Lgn///f38/////////////v7+////////////1L74/6hl9f+udPX/rXP1/6Rq7P+gZuj/n2Xm/5th4/+bYeP/m2Hj/5th4/+bYeP/m2Hj/5th4/+bYeP/m2Hj/51j5f+gZuj/oGbo/6Bm6P+fZef/l13f/5Zc3v+ZYOH/m2Hj/5th4/+bYeP/m2Hj/5th4/+bYeP/pmzu/6pw8f+pcPH/pWLy/9a/+v////////////7+/v/////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P////////////7+/v//////+Pb9/7OK7v+pa/T/rXP1/6hv8P+gZuj/oGbo/6Bl6P+dYuX/m2Dj/5th4/+bYeP/m2Hj/5th4/+bYOP/ml/j/5tg4/+gZuj/oWfp/6Fn6f+hZ+n/oGbo/59k5v+eY+b/nmLm/5tg4/+bYOP/m2Hj/5th4/+bYeP/mmDi/6Fn6f+qcPL/qnDy/6dp8v+/lPv/+vf////////+/v7/////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz///////////////7//////+jf+P+gZuf/pmvv/61z9P+iaer/nmLn/5ta5/+eYej/n2Pn/5dX4v+WV+L/m2Hj/5th4/+YWeL/mFji/5tg4/+eYeb/nVvo/59h6f+iZ+n/omfp/6Bj6f+eW+j/oGLp/6Jn6f+cYOX/llXi/5dY4v+bYuP/mV3i/5la5P+eX+j/p2zv/6pw8v+kaOz/rXP0/+3i/////////////////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2NSTP9jUkz/Y1JM/1xIQf+Lgn///f38///////////////////////VxPP/mljn/6Fn6f+la+3/nmHn/6Rv6f/OufL/6N/5/+zl+v/f0/X/tpbp/5dW4v+YWuL/vaHr/+Ta9v/t5/n/6+P5/9bE9P+sfOv/oGLp/6Bi6P+pdur/0r7z/+jf+f/u5/r/6uL5/93R9P+8oOv/lVTi/7WU6f/k2vf/39L2/6t47P+mau//omfp/59d6//byPz////////////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P/////////////////+/v//xKrv/5tZ5/+gZuj/n2Xo/59j6P/f0vb///////v6/v/18fz///////n2/f+7ner/kUXh/9LA8P/9/f//9vL9//v5/v//////6uH5/6d06v+fX+j/4dX3////////////+vj+//7+////////49n2/5JI4f/Kte7///////////+xh+z/oGHp/6Jo6f+dWuj/x6zy//7+////////////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz//////////////////Pr+/7iV7f+cXOf/oGfo/5xb5/+9ne7///////r4/v+4lO3/oGXo/9zO9f//////6eL4/5th4/+kdOT/rofo/6Bj6P+whOz/9fH8//////+9nO7/sITs//z7/v//////y7Tx/6dz6v/czfX//////+HW9f+WUuL/uZfs/+Xb+P/g0/b/qXfq/6Bk6f+iZ+n/nl7o/7mV7f/8+v7//////////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2NSTP9jUkz/Y1JM/1xIQf+Lgn///f38//////////////////r5/v+xiOv/nV/n/6Bm6P+aWOf/1MPz///////n3vj/nFvn/5lW5/+7m+3//fv+//n3/f+pf+b/lVDi/59l5/+5lu3/1sT0//v5/v//////uZXt/76d7v/+/v//9vL8/6Zw6v+ZUOf/1sT0///////h1vX/nF3l/6Rt6v+5le7/tIzs/6Jm6f+iZ+n/omfp/59g6P+vh+j/+vj9///////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P/////////////////6+P3/rYPq/5xf5v+fZef/m1nn/9nK9P//////4tf3/5xc5/+cXOf/tpPt//r5/v/9/P7/rIPm/6Z25v/p4fn////////////+/f7/3s/2/59h6f/DpfD///////Tv/P+mcOn/nFjn/9fF9P//////4tf3/5tX5/+5le3//fz+//Lt+/+mcOr/oWXp/6Jo6f+dX+b/p37j//n4/f//////////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz/////////////////+/n+/7mP9P+oa/L/q3Lz/51b6f/PuvH//////+3m+v+eYOf/lUnm/8Gl7//+/v//9vP9/6Ju5//NuPH///////j2/f/QvPP/tY3t/55d6P+cV+j/xKbw///////08Pz/qXPt/6Bd7P/Yxvb//////+TY+f+fXOz/vp3w//7+///28fz/qHPq/6Fk6f+iZ+n/llfg/6mC4v/6+P3//////////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2NSTP9jUkz/Y1JM/1xIQf+Lgn///f38//////////////////z7///Hof7/tHb//7F3+f+eYOj/sorr//r5/v//////0r/z/7yc7f/r5Pn//////+DU9v+YUOb/z7vy///////x7fv/t5Dv/8Kf9v/Cpe//nVvo/8Om8P//////9PD7/6l07v+lY/L/2sj5///////l2fv/pGHx/7+f8f/+/v//9vP8/6h26v+gZOn/oWbo/5dW4f+0kuj/+/r+///////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P/////////////////+/v//0LP+/7Bx/P+rcfL/pGrs/5tb5//MtvH/+/n+/////////////////+zl+v+ug+r/m1rn/62B6v/v6fr/////////////////8ev7/6Np6f/CpfD///////by/P+mcer/omDv/9vJ+f//////5tv7/6Bc7f+/oe////7///f0/f+qeer/oGTp/6Zs7f+jYe7/yaz0//7+////////////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz//////////////////////97K//+ra/f/q3H0/6hv8P+hZ+r/n2Hq/7mV7//TwPX/18b0/8iw8P+ndun/nV7n/6Bn6P+dX+f/qn3q/8y08v/Zx/f/1cD2/8Kh8v+iZ+n/roHr/8648v/GrPD/o2np/6Jl6/+9l/T/1L74/8Kh9P+dWen/wqXv///////49f3/q3vq/6Jl6/+obe//o2Hu/9jG9//////////+/////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2NSTP9jUkz/Y1JM/1xIQf+Lgn///f38//////////////7+///////r4f7/q3Lz/6lu8v+qcPL/qnDy/6pv8v+naPH/n17s/5pY5v+bWOf/nmHo/6Bm6P+gZuj/oGbo/55g6P+hX+z/o2Hu/6Ng7v+kZO//pWrs/6Bj6P+dWej/nVvo/6Jm6f+iZ+n/pGfu/6Vk8v+iY+z/nVro/8Wq8P//////+fb9/61+7P+laO7/p2vv/6ht7v/p4Pr///////7+/v/////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P////////////7+/v//////+fb+/7iO9P+nafL/qnDy/6pw8v+qcPL/qG7w/6Bn6P+gZuj/oGbo/6Bm6P+gZuj/oGbo/6Bm6P+kaev/qG3v/6ht7/+obe//qG3v/6ds7v+jaOr/omfp/6Jn6f+kaev/pWrs/6Zs7v+obfD/omjp/5xZ6P/HrvH///////z6/v+xhO7/p2rw/6hp8f+5jvP/+fb+///////+/v7/////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz////////////+/v7////+///////Uvvj/pGHx/6px8v+qcPL/qnDy/6Rq7P+fZuj/oGbo/6Bm6P+fZef/n2Xn/59l5/+hZ+n/p2zu/6ht7/+obe//qG3v/6ht7/+obe//pWrs/6Fm6P+hZuj/pmzu/7B2+P+tc/X/o2jq/6Jn6f+gYej/tIzs/9fG9f/Tv/T/rXjv/61x9P+ycf//2cL//////////////v7+/////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2NSTP9jUkz/Y1JM/1xIQf+Lgn///f38//////////////////7+/v//////8ev8/6548v+pbfL/qnDy/6hu8P+hZ+n/oWfp/6Fn6f+hZ+n/oWbo/59k5v+fZef/pGrs/6ht7/+obe//qG3v/6ht7/+obe//qG3v/6lv8f+nbe//p23u/6dt7/+udPb/rHL0/6Vq7P+iZ+n/omjp/6Bj6f+dWuj/oWDs/6hs7/+nau//toD6//Pt/////////v7+///////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P/////////////////+/v7////////////Ru/f/pWPx/6pw8v+kaev/omfp/6Jn6f+iZ+n/omfp/6Jn6f+fZef/omjq/6ds7v+obe//p23u/6dt7v+nbe7/p23u/6ds7v+pb/H/rXT2/61z9f+tc/X/rXP1/61z9f+kauv/oWbo/6Fm6P+hZuj/o2jq/6ds7v+nbO7/ol/u/9G69v////////////7+/v//////////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz///////////////////////7+/v//////9vL9/7eL9P+jZO7/omfp/6Jn6f+iZ+n/omfp/6Jn6f+hZuj/n2bn/59l5/+gZuj/oGbo/6Bm6P+gZuj/oGbo/6Bm6P+gZuf/oGXn/6lu8P+tc/b/rXP1/61z9f+scvT/rnT2/6509v+udPb/rnT2/691+P+wdvj/rW/3/7uO+P/28v3///////7+/v///////////////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2NSTP9jUkz/Y1JM/1xIQf+Lgn///f38///////////////////////+/v7//v7+///////m2vr/omTq/6Bj6P+iZ+n/omfp/6Jn6f+hZuj/n2Xn/6Jo6v+hZuj/n2Tl/59k5v+fZOb/nmPl/55j5f+eY+X/nmPl/55i5P+hZ+j/rHL0/61z9f+scvP/pWrs/7J4+v+2fP7/tnz+/7Z8/v+2fP7/tHj+/7V5/v/p3P////////7+/v/+/v7////////////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P////////////////////////////7+/v///////////9bF9P+eXOj/oWTp/6Jn6f+iZ+n/o2nr/6Rq7P+obu//pmvt/59k5v+fZOb/n2Tm/6Rp6/+lauz/pWrr/6Vq7P+kaev/n2Tm/6Zs7v+udPb/p2zu/6Bl5/+obu//tXv9/7V7/f+1e/3/tHn9/7Jz/f/dyv7////////////+/v7/////////////////////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz//////////////////////////////////v7+///////+/v//0Lvz/55c6P+gY+n/oWbo/6dt7v+0ePv/rnP1/6ht7/+jaOr/n2Tm/59j5f+tc/X/t33//7d9/v+3ff//rXP1/55j5f+jaOr/q3Hz/6Np6/+hZuj/omfp/6919/+2fP7/tHj9/7Jz/f/Ywf7//v7////////+/v7//////////////////////////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2NSTP9jUkz/Y1JM/1xIQf+Lgn///f38///////////////////////////////////////+/v7///////7+///XxfT/oGPo/5xc5/+iaOr/rnT1/6lu8P+obe//p2zu/6Bl5/+eY+X/o2jp/7V7/f+4fv//tXv9/6Jo6f+fZOb/p2zu/6hu7/+lauz/omfp/6Fm5/+ma+3/snT8/7R5/f/dyv7//v7////////+/v7////////////////////////////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P////////////////////////////////////////////7+/v///////////+TZ9/+uhOv/qGf0/6tv9P+nbe7/qG3v/6ht7/+kaev/n2Tm/55j5f+qcPL/uX///6pw8v+eY+X/o2nq/6ht7/+obe//p2zu/6Np6v+laO3/pWPx/7uO+P/p3P//////////////////////////////////////////////////////////////////7u3t/2ZeXJ+clpUAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz//////////////////////////////////////////////////v7+////////////9vL9/9e+/v+2gPv/o1/v/6Vm7v+na+//p2zu/6Fm6P+eZOX/oWfo/6519f+hZuj/oWbo/6Vr7P+lauz/pGfs/6Nj7P+fWuz/rnjy/9e+/v/28v3//////////////////////////////////////////////////////////////////////+7t7f9mXlyfnJaVABAQDAAAAAAAAAAAAAAAAABOQTwASz46kl9PSf9jUkz/Y1JM/2NSTP9jUkz/Y1JM/1xIQf+Lgn///f38///////////////////////////////////////////////////////+/v7//v7/////////////8+z//9S++P+2jPH/qG3v/6Rh7/+gXuv/m1rl/5xd5f+dXub/nF3l/6Fh7P+hXuz/oF3r/6Vq7P+2i/D/0732//Hr/P/////////////////////////////////////////////////////////////////////////////////u7e3/Zl5cn5yWlQAQEAwAAAAAAAAAAAAAAAAATkE8AEs+OpJfT0n/Y1JM/2NSTP9jUkz/Y1JM/2NSTP9cSEH/i4J///39/P////////////////////////////////////////////////////////////7+/v//////////////////////+fb+/+ng+v/Zxvf/ya30/7mV7f+wh+n/rYLp/7KJ6/+9mPL/yKzz/9fF9f/p4Pr/+fb+///////////////////////+/v7/////////////////////////////////////////////////////////////////7u3t/2deXJ+dl5UAEBAMAAAAAAAAAAAAAAAAAE5BPABLPjqSX09J/2NSTP9jUkz/Y1JM/2NSTP9jUkz/XEhB/4uCf//9/fz////////////////////////////////////////////////////////////////////////////+/v7///////////////////////7+///8+v7/+vn+//r4/f/6+f7//Pv+//7+/////////////////////////v7+//7+/v///////////////////////////////////////////////////////////////////////////+7u7f9kW1mgl5GPABEPDAAAAAAAAAAAAAAAAABLPjoARzo2a1tLRv9kU03/ZFNN/2RTTP9kU0z/ZFNM/11JQv+Mg4D///////////////////////////////////////////////////////////////////////////////////////7+/v/+/v7//v7+/////v/////////////////////////////////////////+//7+/v/+/v7//v7+///////////////////////////////////////////////////////////////////////////////////////V1NP/PCokfGVdWwASCgwAAAAAAAAAAAAAAAAAQzczADQrKAxMPzujVEVB9FVGQfRVRkH0VUZB9FVGQfRRQTz0amBd9LGurfSzsK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LKwr/SysK/0srCv9LOwr/Srp6bycmtpqwAAABE2JSAAEgwMAAAAAAAAAAAAAAAAAEY6NgBBNjIAdGBaAC4lJB4vJiQkLyYkIy8mJCMvJiQjMysqIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAjAAAAIwAAACMAAAAkAAAAHP///wAAAAAARzs3AAAAAAAAAAAAAAAAAAAAAAAAAAAAQjYzAEA1MgA/NDAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAD4zMAA+MzAAPjMwAEA0MQA/NDEAQjczAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA////////////////////////////////////////////////////////////////////////////////////////////////8AAAAAAAAA/gAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH4AAAAAAAAAfgAAAAAAAAB+AAAAAAAAAH+AAAAAAAAB////////////////////////////////////////////////////////////////////////////////////////////////8='''

# AutoHotkey script to hide the system cursor
HIDE_CURSOR_SCRIPT = '''
#NoEnv
#Persistent
#SingleInstance Force
SetWorkingDir %A_ScriptDir%

if not A_IsAdmin
{
    Run *RunAs "%A_ScriptFullPath%"
    ExitApp
}

VarSetCapacity(AndMask, 128, 0xFF)
VarSetCapacity(XorMask, 128, 0)

CursorIDs := [32512, 32650, 32515, 32649, 32651, 32513, 32648, 32646, 32643, 32645, 32642, 32644, 32516, 32514]

Loop % CursorIDs.Length()
{
    CursorID := CursorIDs[A_Index]
    CursorHandle := DllCall("CreateCursor", "Ptr", 0, "Int", 0, "Int", 0, "Int", 32, "Int", 32, "Ptr", &AndMask, "Ptr", &XorMask)
    DllCall("SetSystemCursor", "Ptr", CursorHandle, "Int", CursorID)
}
ExitApp
'''

# AutoHotkey script to restore the system cursor
SHOW_CURSOR_SCRIPT = '''
#NoEnv
#Persistent
#SingleInstance Force
SetWorkingDir %A_ScriptDir%

DllCall("SystemParametersInfo", "UInt", 0x57, "UInt", 0, "Ptr", 0, "UInt", 0)
ExitApp
'''

def hide_cursor():
    """Hides the system cursor using an AutoHotkey script."""
    try:
        # Create temporary script file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ahk') as tf:
            tf.write(HIDE_CURSOR_SCRIPT.encode())
            temp_script = tf.name
        
        # Execute script
        subprocess.Popen([r"C:\Program Files\AutoHotkey\AutoHotkey.exe", temp_script])
        
        # Clean up temp file after a short delay
        def cleanup():
            time.sleep(1)
            try:
                os.unlink(temp_script)
            except:
                pass
        threading.Thread(target=cleanup).start()
        
        return True
    except Exception as e:
        print(f"Error hiding cursor: {e}")
        return False

def show_cursor():
    """Restores the system cursor using an AutoHotkey script."""
    try:
        # Create temporary script file 
        with tempfile.NamedTemporaryFile(delete=False, suffix='.ahk') as tf:
            tf.write(SHOW_CURSOR_SCRIPT.encode())
            temp_script = tf.name
        
        # Execute script
        subprocess.Popen([r"C:\Program Files\AutoHotkey\AutoHotkey.exe", temp_script])
        
        # Clean up temp file after a short delay
        def cleanup():
            time.sleep(1)
            try:
                os.unlink(temp_script)
            except:
                pass
        threading.Thread(target=cleanup).start()
        
        return True
    except Exception as e:
        print(f"Error showing cursor: {e}")
        return False

def get_monitor_info():
    """Retrieves and prints information about all connected monitors."""
    monitors = get_monitors()
    print("Detected Monitors:")
    for i, m in enumerate(monitors):
        print(f"Monitor {i}: {m.width}x{m.height} at ({m.x}, {m.y})")
    return monitors

def set_tablet_dimensions(width=0, height=0):
    """Sets the tablet dimensions in millimeters."""
    try:
        global TABLET_WIDTH_MM, TABLET_HEIGHT_MM
        TABLET_WIDTH_MM = float(width)
        TABLET_HEIGHT_MM = float(height)
        print(f"Tablet dimensions: {TABLET_WIDTH_MM}x{TABLET_HEIGHT_MM}mm")
        return True
    except ValueError:
        print("Invalid input. Please enter valid numbers.")
        return False

def cursor_to_mm(x, y):
    """Converts cursor screen coordinates to tablet millimeter dimensions."""
    mm_x = (x / SCREEN_WIDTH) * TABLET_WIDTH_MM
    mm_y = (y / SCREEN_HEIGHT) * TABLET_HEIGHT_MM
    return mm_x, mm_y

def plot_cursor_positions(positions_x, positions_y, measurements):
    """Plots the cursor movement path and allows measuring selected areas."""

    # find figsize matching tablet proportions
    maxwidth = 12 # inches
    maxheight = 8
    padding = 1
    aspect_ratio = TABLET_HEIGHT_MM / TABLET_WIDTH_MM
    if aspect_ratio > (maxheight - 2 * padding) / (maxwidth - 2 * padding):
        width = (maxheight - 2 * padding) / aspect_ratio + 2 * padding
        height = maxheight
    else:
        width = maxwidth
        height = (maxwidth - 2 * padding) * aspect_ratio + 2 * padding

    fig = plt.figure(figsize=(width, height), facecolor='#2E2E2E')
    
    ax = fig.add_subplot(111, facecolor='#1E1E1E')
    ax.set_aspect('equal')
    plt.xlim(0, TABLET_WIDTH_MM)
    plt.ylim(0, TABLET_HEIGHT_MM)
    ax.plot(positions_x, positions_y, '#FF7EB8', alpha=0.7, linewidth=1.5)
    ax.invert_yaxis()

    icon_file = tempfile.NamedTemporaryFile(delete=False, suffix='.ico')
    icon_file.write(base64.b64decode(ICON))
    icon_file.close()
    fig.canvas.manager.window.wm_iconbitmap(icon_file.name)
    os.unlink(icon_file.name)


    ax.tick_params(axis='x', colors='white')
    ax.tick_params(axis='y', colors='white')
    plt.title('Cursor Movement Path (Click and drag to measure area)', color='white')
    plt.xlabel('X Position (mm)', color='white')
    plt.ylabel('Y Position (mm)', color='white')
    plt.grid(True, color='#444444')
    fig.canvas.manager.set_window_title('Your Area')

    def on_select(eclick, erelease):
        """Handles area selection on the plot and displays measurement details."""
        xc, yc = selector.corners
        corners = np.transpose((xc, yc))
        vec1 = corners[1] - corners[0]
        vec2 = corners[3] - corners[1]
        
        if is_rectangle((xc, yc), 1e-12):
            playfield_width = np.linalg.norm(vec1)
            playfield_height = np.linalg.norm(vec2)
            screen_width = playfield_width * 5/3
            screen_height = playfield_height * 5/4
            center = corners[0] + 1/2 * vec1 + 25/48 * vec2
            angle = np.arctan2(yc[1] - yc[0], xc[1] - xc[0])
        
            selection_text = (
                f"Selected Area:\n"
                f"Playfield Area: {playfield_width:.1f}x{playfield_height:.1f}mm\n"
                f"Screen Area: {screen_width:.1f}x{screen_height:.1f}mm\n"
                f"Center: X={center[0]:.1f}mm, Y={center[1]:.1f}mm\n"
                f"Rotation: {angle * 180 / np.pi:.1f}°"
            )
        else:
            selection_text = (
                "Not a rectangle."
            )
        
        if hasattr(ax, 'selection_text'):
            ax.selection_text.remove()
        ax.selection_text = ax.text(0.025, 0.96, selection_text,
            transform=ax.transAxes,
            verticalalignment='top',
            bbox=dict(facecolor='#2E2E2E', alpha=0.9, edgecolor='#FF7EB8', boxstyle='round,pad=1'),
            fontsize=10,
            family='monospace',
            color='white')
        plt.draw()
    
    selector = ParallelogramSelector(
        ax, on_select,
        useblit=True,
        interactive=True,
        drag_from_anywhere=True,
        props=dict(facecolor='#FF7EB8', edgecolor='#FF7EB8', alpha=0.5, fill=True)
    )
    
    ax.text(0.975, 0.96, measurements, 
            transform=ax.transAxes,
            verticalalignment='top',
            horizontalalignment='right',
            bbox=dict(
                facecolor='#2E2E2E',
                alpha=0.9,
                edgecolor='#FF7EB8',
                boxstyle='round,pad=1'
            ),
            fontsize=10,
            family='monospace',
            color='white')
    
    plt.show()

def is_rectangle(corners, tolerance=1e-12):
    """
    Calculates whether the given array defines the corners of a rectangle
    in either clockwise or anti-clockwise order, up to a given relative tolerance.
    corners: array-like of shape (4, 2) or (2, 4)
    tolerance: relative to the distance between the first two points in corners
    """
    if np.shape(corners) == (4, 2):
        corners = np.array(corners)
    elif np.shape(corners) == (2, 4):
        corners = np.transpose(corners)
    else:
        raise ValueError('corners must be array-like of shape (2, 4) or (4, 2).')
    vec1 = corners[1] - corners[0]
    vec2 = corners[-1] - corners[0]
    absolute_tolerance = tolerance * np.linalg.norm(vec1)
    dotproduct_tolerance = tolerance * np.linalg.norm(vec1)**2

    if not np.abs(np.dot(vec1, vec2)) <= dotproduct_tolerance:
        return False
    if not np.linalg.norm(corners[2] - (corners[0] + vec1 + vec2)) <= absolute_tolerance:
        return False
    return True

def track_cursor_movement():
    """Tracks the cursor movement in real-time and calculates the tablet area used."""
    tracking = True
    last_x = last_y = 0
    max_mm_x = max_mm_y = float('-inf')
    min_mm_x = min_mm_y = float('inf')
    positions_x = []
    positions_y = []
    
    # Display monitor information
    get_monitor_info()
    # Hide the cursor during tracking
    hide_cursor()
    print("Tracking started! Press F6 to stop")

    try:
        while tracking:
            if keyboard.is_pressed('F6'):
                # Stop tracking when F6 is pressed
                tracking = False
                width = (max_mm_x - min_mm_x)
                height= (max_mm_y - min_mm_y)
                widthad = (max_mm_x - min_mm_x) * 1.66666666667
                heightad = (max_mm_y - min_mm_y) * 1.25
                center_x = min_mm_x + (max_mm_x - min_mm_x) / 2
                center_y = min_mm_y + (max_mm_y - min_mm_y) / 23/48
                measurements = (
                    f"Final Measurements:\n"
                    f"Area: {width:.1f}x{height:.1f}mm\n"
                    f"Adjusted Area: {widthad:.1f}x{heightad:.1f}mm\n"
                    f"Center: X={center_x:.1f}mm, Y={center_y:.1f}mm\n"
                    f"Min: {min_mm_x:.1f}x{min_mm_y:.1f}mm\n"
                    f"Max: {max_mm_x:.1f}x{max_mm_y:.1f}mm"
                )
                # Restore the cursor visibility
                show_cursor()
                # Plot the cursor positions
                plot_cursor_positions(positions_x, positions_y, measurements)
                break

            x, y = pyautogui.position()
            if (x != last_x) or (y != last_y):
                # Convert screen coordinates to tablet dimensions
                mm_x, mm_y = cursor_to_mm(x, y)
                positions_x.append(mm_x)
                positions_y.append(mm_y)

                max_mm_x = max(max_mm_x, mm_x)
                max_mm_y = max(max_mm_y, mm_y)
                min_mm_x = min(min_mm_x, mm_x)
                min_mm_y = min(min_mm_y, mm_y)

                last_x, last_y = x, y
    except KeyboardInterrupt:
        print("\nTracking stopped by user")

if __name__ == "__main__":
    # Set tablet dimensions before starting tracking
    set_tablet_dimensions()
    track_cursor_movement()
