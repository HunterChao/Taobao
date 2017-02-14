####1、数据库配置
mysql.txt是数据库配置文件，共设置8个字段。goods_id：商品id号 ；shop_id：店铺id号 ；shop_loc：店铺地址 ；shop_name：店铺名称 ；goods_title：商品名称 ；view_sales：商品销量 ；view_price：商品价格 ；comment_url：店铺链接。 商品id号唯一，设为主键；
####2、抓取规则
程序从连衣裙类型页面作为爬取首页，根据抓取的店铺id号和商品id号进入二级页面抓取信息，根据从二级页面提取到的店铺id号和商品id号进行下一级抓取；
####3、程序调用
api.py为接口，程序从_init_.py运行；
####4、抓取示例
![](https://github.com/HunterChao/Taobao/blob/master/Taobao/mysql.png)
