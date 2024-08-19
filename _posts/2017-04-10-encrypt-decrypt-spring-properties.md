---
layout: post
title: Spring .properties配置文件加密
tags: [Spring]
categories: [Java技术研究]
date: 2017-04-10 15:56:26 +0800
comments: true
author: onecoder
thread_key: 1907
---
对于保存在.properties文件中的敏感信息，支持采用加密的方式保存。然后在程序中解密使用。

<!--break-->

# 实现方案
采用自定义PropertySourceLoader的方式，在.properties配置文件加载期，遍历值，遇到指定格式的值，则执行解密操作。具体代码如下：

```java
/**
 * @author li.hzh
 * @date 2017-04-10 13:46
 */
@Slf4j
public class EncryptPropertySourceLoader implements PropertySourceLoader, PriorityOrdered {
    
    private static final String ENC_PREFIX = "ENC@[";
    private static final String ENC_POSTFIX = "]";
    
    @Override
    public String[] getFileExtensions() {
        return new String[]{"properties"};
    }
    
    @Override
    public PropertySource<?> load(String name, Resource resource, String profile) throws IOException {
        if (profile == null) {
            Properties properties = PropertiesLoaderUtils
                                            .loadProperties(new EncodedResource(resource, "UTF-8"));
            if (!properties.isEmpty()) {
                decryptValue(properties);
                return new EncryptPropertiesSource(name, properties);
            }
        }
        return null;
    }
    
    private void decryptValue(Properties properties) {
        Set<Object> keys = properties.keySet();
        for (Object key : keys) {
            String value = (String) properties.get(key);
            if (isMatchEncrypt(value)) {
                String finalValue = value;
                try {
                    finalValue = decrypt(value);
                } catch (Exception e) {
                    log.error("Decrypt value [" + value + "] error", e);
                }
                properties.put(key, finalValue);
            }
        }
    }
    
    private boolean isMatchEncrypt(String value) {
        return value.startsWith(ENC_PREFIX) && value.endsWith(ENC_POSTFIX);
    }
    
    private String decrypt(String input) throws Exception {
        String encryptData = getEncryptData(input);
        return CodecUtil.decrypt(encryptData);
    }
    
    private String getEncryptData(String input) {
        return input.substring(ENC_PREFIX.length(), input.length() - ENC_POSTFIX.length());
    }
    
    @Override
    public int getOrder() {
        return HIGHEST_PRECEDENCE;
    }
}
```

CodecUtil即加解密工具类，这里实现自己的即可。EncryptPropertiesSource为复写的PropertiesSource类。

在META-INF/spring.factory中指定使用该类

```
org.springframework.boot.env.PropertySourceLoader=xxx.xxx.EncryptPropertySourceLoader
```

## 使用方法
将需要加密的值，加密后放在ENC@[密文]，即可。其余值不会被处理。
