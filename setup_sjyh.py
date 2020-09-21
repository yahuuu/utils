#!/usr/bin/env python
# coding=utf-8

from setuptools import setup, find_packages

'''
# 3.5 更新说明：
1. 流程中添加logo检测模块， 
2. 更新分类模型在支票的准确率
3. 为011添加正则替换

# 3.4 更新说明：
1. 红色数字号码判断模块替换灰度阈值

# 3.3 更新说明：
1. 模板匹配增加模板图片
2. 新增识别票据类别
    u"通知储蓄存单":u"069",
    u"单位定期存单":u"016",
    u"现金支票":u"003",
    u"单位定期存款开户证实书":u"014",
    u"单位结构性存款开户证实书":u"088",
    u"盛京银行大额存单申请书":u"103",
    u"委托付款授权确认书":u"055",
    u"单位银行结算账户短信通知服务申请书":u"901",
    u"批量业务申请单":u"902",
    u"盛京银行个人结构性存款产品协议书":u"101",
    u"盛京银行开立资信证明申请书":u"093",
    u"预制卡":u"61",
    u"资信证明书（正本）":u"None"

# 3.2 更新说明：
1. 流程最后增加模板匹配
2. 新增加的类别为：065， 066， 532， 520 

# 3.1 更新说明：
1. billTypeWebService_v2_sub.py 添加 通用凭证 201映射
2. billTypeInfo.cfg	添加 通用凭证 类型
3. billTitleOCR.py 202行 修改轮廓 过滤条件 由0.6 换成 0.7 通用凭证-00000019.JPG
	
# 3.0 更新说明：
1. cnn 集成到版面识别前
2. 输出类型转化为代号
3. 语言升级到python3.6.2

# 2.1更新说明：
1. 增加了log
2. 修改了二值化方法
3. 结算业务申请书，有符号无符号判断
'''

setup(
    name="sjocr",  #pypi中的名称，pip或者easy_install安装时使用的名称，或生成egg文件的名称
    version="3.5",
    description=("This is a service of ocr for Bank of ShengJingJ."),
    package_dir={'sjocr': 'sjocr'},
    # packages=['sjocr',
    #           'sjocr/ocr_models',
    #           'sjocr/ocr_models/Tesseract_API',
    #           # 'sjocr/demos',
    #           # 'sjocr/demos/sjyh',
    #           #'sjocr/demos/sjyh/bankBillTypeOCR',
    #           #'sjocr/demos/sjyh/bankBillTypeOCR/commond',
    #           'sjocr/bankBillTypeOCR',
    #           'sjocr/bankBillTypeOCR/commond',
    #           'sjocr/bankBillTypeOCR/title_Type',
    #           'sjocr/tesseract_reg_online',
    #           'sjocr/tesseract_reg_online/utils'
    #           ],
    packages = find_packages( exclude=["test_img"]),
    
    include_package_data=True,
    package_data={'sjocr': [
			    'ocr_models/tessdata/*',
			    #'ocr_models/tessdata/configs/*',
			    #'ocr_models/tessdata/tessconfigs/*',
               'ocr_models/Tesseract_API/32bit/TesseractDLL3/*',
               'ocr_models/Tesseract_API/32bit/TesseractDLL4/*',
			   'ocr_models/Tesseract_API/TesseractDLL64/*',
               'ocr_models/Tesseract_API/64bit/TesseractDLL4/*',
               'ocr_models/Tesseract_API/linux/*',
               # 'demos/sjyh/bankBillTypeOCR/title_Type/*.cfg'
                'bankBillTypeOCR/title_Type/*.cfg',
                'tmpl_model/*',
                'paramConfig.conf',
                "reg_type_tmp.txt",
                "cnn_interface_sj/ApplicationFormClassification/checkpoints/*",
                "sjLogoMatch/model/*.png",
                "templateMatch/model/*.png"
			   ]
		 },

    # 需要安装的依赖
    install_requires=[
        'setuptools>=16.0',
    ],

    # long_description=read('README.md'),
    classifiers=[  # 程序的所属分类列表
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
    ],
    # 此项需要，否则卸载时报windows error
    zip_safe=False
)
