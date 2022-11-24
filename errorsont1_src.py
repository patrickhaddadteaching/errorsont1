from ipywidgets import interact, interact_manual, widgets, Label
import numpy as np
import functools
from time import time, sleep
import matplotlib.pyplot as plt

def generate_biased_rnd_vector_bits(p_in,n_in):
    v_raw_rnd_bin=np.array(np.random.rand(n_in)<p_in,dtype=np.uint8)
    return v_raw_rnd_bin
  
  
raw_bytes=widgets.Textarea(value='',placeholder='',description='',disabled=True,layout=widgets.Layout(width='200px',height='200px'))
text_fontsize=12

myfont_dict = {'family': 'serif','color':  'darkblue','weight': 'normal','size': 16}

nb_p=10000
v_p=0.5*np.arange(1,nb_p+1,dtype=np.float64)/(nb_p+1)
v_h=-1*(np.log2(v_p)*(v_p)+np.log2(1-v_p)*(1-v_p))

def errorsont1(entropy_in,test_size,v_Th):

  Th_low=int(v_Th[0])
  Th_high=int(v_Th[1])

  nb_tests=100

  if entropy_in==1:
    p_target=0.5
  elif entropy_in==0:
    p_target=np.random.randint(0,2)
  else:
    rnd=np.random.randint(0,2)
    if rnd==0:
      p_target=v_p[np.where(v_h>entropy_in)[0][0]]
    else:
      p_target=1-v_p[np.where(v_h>entropy_in)[0][0]]

  v_in=generate_biased_rnd_vector_bits(p_target,int(nb_tests*test_size))

  s_line_raw=''
  for i in range(test_size*2):
    s_line_raw='%s%d'%(s_line_raw,v_in[i])
  raw_bytes.value=s_line_raw

  m_in=v_in.reshape(nb_tests,test_size)
  v_T1=m_in.sum(1)

  index_out_of_range=np.where(((v_T1<Th_low) | (v_T1>Th_high)))[0]
  nb_alarms=len(index_out_of_range)

  plt.figure(1,figsize=[7,3.5])
  plt.plot(v_T1,'g.')
  plt.plot([0,nb_tests],[Th_high,Th_high],'k')
  plt.text(0, Th_high-20,'High Threshold', fontsize=text_fontsize)
  plt.plot([0,nb_tests],[Th_low,Th_low],'k')
  plt.text(nb_tests-30, Th_low+5,'Low Threshold', fontsize=text_fontsize)
  plt.text(0,((max([v_T1.max(),Th_low,Th_high])+min([v_T1.min(),Th_low,Th_high]))*0.5),"Alarm {:d}% of the time".format(nb_alarms), fontdict=myfont_dict)
  
  if nb_alarms>0:
    plt.plot(index_out_of_range,v_T1[index_out_of_range],'r.')
  plt.tick_params(axis='x', which='both', bottom=False,top=False,labelbottom=False)
  plt.ylabel(r'$T_{1}$ values')
  plt.show()
    

im=interact(errorsont1,entropy_in=widgets.FloatSlider(value=0.5,min=0,max=1),test_size=widgets.IntSlider(value=512,min=0,max=1024),v_Th = widgets.IntRangeSlider(value = [int(512/2-50),int(512/2+50)], min = 0, max = 1024, step = 1 ))
im.widget.close()
im.widget.children[0].description='Entr. Target'
im.widget.children[1].description='Latency'
im.widget.children[2].description='Thresh.'

im.widget.children[0].layout=widgets.Layout(width='650px')
im.widget.children[1].layout=widgets.Layout(width='415px')
im.widget.children[2].layout=widgets.Layout(width='650px')
v_box_top=widgets.VBox([im.widget.children[0],im.widget.children[1],im.widget.children[2],widgets.HBox([im.widget.children[3],raw_bytes])])
