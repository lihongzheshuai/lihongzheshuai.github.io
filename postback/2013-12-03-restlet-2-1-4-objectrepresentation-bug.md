---
layout: post
title: Restlet 2.1.4中 匪夷所思的ObjectRepresentation的构造函数
date: 2013-12-03 22:26
author: onecoder
tags: true
tags: [Restlet]
thread_key: 1562
---
<a href="http://www.coderli.com">OneCoder</a>使用Restlet最新版2.1.4开发样例，却一直抛出异常：

>
Exception in thread "main" java.lang.IllegalArgumentException : The serialized representation must have this media type: application/x-java-serialized-object or this one: application/x-java-serialized-object+xml<br/>
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; at org.restlet.representation.ObjectRepresentation.<init>(ObjectRepresentation.java:203)<br/>
		&nbsp;&nbsp;&nbsp;&nbsp; at org.restlet.representation.Objec	tRepresentation.<init>(ObjectRepresentation.java:114)


<!--break-->

无论怎么设置MediaType都无效，无奈只能查看次构造函数的源码：


```java
public ObjectRepresentation(Representation serializedRepresentation,
            final ClassLoader classLoader) throws IOException,
            ClassNotFoundException, IllegalArgumentException {
        super(MediaType.APPLICATION_JAVA_OBJECT);


        if (serializedRepresentation.getMediaType().equals(
                MediaType. APPLICATION_JAVA_OBJECT)) {
            if (!VARIANT_OBJECT_BINARY_SUPPORTED ) {
                throw new IllegalArgumentException(
                        "SECURITY WARNING: The usage of ObjectInputStream when "
                                + "deserializing binary presentations from unstrusted "
                                + "sources can lead to malicious attacks. As pointed "
                                + "here (https://github.com/restlet/restlet-framework-java/issues/778), "
                                + "the ObjectInputStream class is able to force the JVM to execute unwanted "
                                + "Java code. Thus, the support of such format has been disactivated "
                                + "by default. You can activate this support by turning on the following system property: "
                                + "org.restlet.representation.ObjectRepresentation.VARIANT_OBJECT_BINARY_SUPPORTED." );
            }
            setMediaType(MediaType.APPLICATION_JAVA_OBJECT );
            InputStream is = serializedRepresentation.getStream();
            ObjectInputStream ois = null;
            if (classLoader != null) {
                ois = new ObjectInputStream(is) {
                    @Override
                    protected Class<?> resolveClass(
                            java.io.ObjectStreamClass desc)
                            throws java.io.IOException,
                            java.lang.ClassNotFoundException {
                        return Class
                                . forName(desc.getName(), false, classLoader);
                    }
                };
            } else {
                ois = new ObjectInputStream(is);
            }


            this.object = (T) ois.readObject();


            if (is.read() != -1) {
                throw new IOException(
                        "The input stream has not been fully read.");
            }


            ois.close();
        } else if (VARIANT_OBJECT_XML_SUPPORTED
                && serializedRepresentation.getMediaType().equals(
                        MediaType.APPLICATION_JAVA_OBJECT_XML )) {
            if (!VARIANT_OBJECT_XML_SUPPORTED ) {
                throw new IllegalArgumentException(
                        "SECURITY WARNING: The usage of XMLDecoder when "
                                + "deserializing XML presentations from unstrusted "
                                + "sources can lead to malicious attacks. As pointed "
                                + "here (http://blog.diniscruz.com/2013/08/using-xmldecoder-to-execute-server-side.html), "
                                + "the XMLDecoder class is able to force the JVM to "
                                + "execute unwanted Java code described inside the XML "
                                + "file. Thus, the support of such format has been "
                                + "disactivated by default. You can activate this "
                                + "support by turning on the following system property: "
                                + "org.restlet.representation.ObjectRepresentation.VARIANT_OBJECT_XML_SUPPORTED." );
            }
            setMediaType(MediaType.APPLICATION_JAVA_OBJECT_XML );
            InputStream is = serializedRepresentation.getStream();
            java.beans.XMLDecoder decoder = new java.beans.XMLDecoder(is);
            this.object = (T) decoder.readObject();


            if (is.read() != -1) {
                throw new IOException(
                        "The input stream has not been fully read.");
            }


            decoder.close();
        }
        throw new IllegalArgumentException(
                "The serialized representation must have this media type: "
                        + MediaType.APPLICATION_JAVA_OBJECT .toString()
                        + " or this one: "
                        + MediaType.APPLICATION_JAVA_OBJECT_XML .toString());
    }
```

惊呆的发现，最后的throw new IllegalArgumentException 逻辑被赤裸裸的暴露在外面，也就是不论上面走的是if还是else，最终都会走到这里抛出异常结束。这不免让我一头雾水，回头查看2.1.2版本的源码，发现抛出异常的代码是写在最后的else块里的，这可就大不相同了。

我只能以我目前粗浅的了解，怀疑这是restlet的一个粗心的bug，我已经给restlet发了邮件咨询了该问题，等待回复中。目前，我也只能降到2.1.2版本的restlet进行开发，在2.1.2版上无此问题。

注：已确认是bug。
