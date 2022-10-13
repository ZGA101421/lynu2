# **实现某高校健康上报功能demo**
* 此代码展示为部分功能
* 随机体温
* 配置文件配置多个账号密码 例如
``` json
{
  "users": [
    {
      "username": "学号",
      "password": "密码"
    },
    {
      "username": "学号",
      "password": "密码"
    },
    {
      "username": "学号",
      "password": "密码"
    }
  ]
}
```
* 通过账号密码获得jwt 无需抓包
* 上报数据采用个人打卡历史最新数据
* 使用 [pushplus](http://www.pushplus.plus)推送功能
* 位置发生改变后，仅需自己手动打卡


***

打卡时间可进行自定义参考[腾讯云 定时触发器说明](https://cloud.tencent.com/document/product/583/9708)
修改`serverless.yml cronExpression 字段```
```yaml
events:
    - timer:
        name: lynu-8a6383441
        parameters:
          cronExpression: 0 0/25 6 * * * * #cron 表达式
          enable: true
          qualifier: $DEFAULT
```

体验版小程序仅支持部分人员体验

以上仅作开发交流
