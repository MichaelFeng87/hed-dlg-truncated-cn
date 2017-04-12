### Description
Iulian V. Serban*, Alessandro Sordoni*, Yoshua Bengio1*, Aaron Courville* and Joelle Pineau 作为智能应答方面的代表，为该领域的研究做出了很大贡献，基于Ubuntu／Twitter／Movie对白等对话语料库，以及利用VHRED／HRED／Truncated BPTT等各种深度学习模型的工程化项目hed-dlg-truncated，取得了较好的应答对话效果。本项目hed-dlg-truncated-cn通过前期摸索，总结能快速运行demo的步骤，帮助有兴趣的同行方便上手和使用。更重要的是利用已有成果，构建面向中文的智能对话应用。
本项目计划主要分三个部分／阶段，而hed-dlg-truncated中所描述的具体细节本项目不再赘述。第一部分描述如何快速运行demo的步骤；原项目基于python2，因此第二部分拟进行python3改造；第三部分为进行中文智能应答对话。

第一部分：快速运行demo的步骤	

（1）安装theano，准备hed-dlg-truncated工程；

（2）demo步骤：

  	 (a)  cd hed-dlg-truncated-master
   
  	 #### 训练模型
   
   	 (b)  THEANO_FLAGS=mode=FAST_RUN,floatX=float32 python train.py --prototype prototype_test > Model_Output.txt
   
  	 ###  对测试问题进行应答对话
   
   	 (c)  python create-text-file-for-tests.py ./tests/models/1491890939.58_testmodel ./tests/data/ttest.dialogues.pkl --utterances_to_predict 2
  
  	 ps. 对于Ubuntu和Twitter的示例由于数据较大，本部分暂不做介绍。  
    
第二部分：兼容python3      

第三部分：中文智能应答对话  
      




