---
layout: post
title: Java 利用ASM读取变量值(Field value)问题研究
date: 2012-05-29 23:30 +0800
author: onecoder
comments: true
tags: [ASM, Spring,Java]
categories: [Java技术研究]
thread_key: 150
---
最近在学习Spring源码的过程中，遇到了spring-asm工程的重新打包的问题，于是突然就想研究一下asm这个开源字节码操作工具。秉承我的一贯风格，想到啥就立马学啥。 对于开源产品，我的一贯风格就是通过其官方提供的源码版本管理地址(svn/git等)，直接下载最新代码，构建Java工程，直接通过工程依赖的方式研究学习。（你说这样跟依赖jar包并且绑定源码比有啥好处？ 一般情况下差不多，最多就是，我可以随时更新代码，可以本地随意修改代码等等呵呵。个人喜好。）

废话不多说，进入正题。我当时想研究的主要问题，就是想尝试通过ASM读取到class文件中声明的变量及其值(其实ASM的主要功能应该是动态生成字节码)。其他东西，我认为是可以触类旁通的。所以，我简单阅读了一下其官方文档，发现其tree API还是非常简单易懂，好上手的。所以，立即动手，我先新建了一个待读取的类。叫ForReadClass，内容如下：

```java
/**
 * @author lihzh
 * @date 2012-4-21 下午10:18:46
 */
public class ForReadClass {

	final int init = 110;
	private final Integer intField = 120;
	public final String stringField = "Public Final Strng Value";
	public static String commStr = "Common String value";
	String str = "Just a string value";
	final double d = 1.1;
	final Double D = 1.2;
	
	public ForReadClass() {
	}
	
	public void methodA() {
		System.out.println(intField);
	}
}
```

然后编写读取类如下：

```java
   /**
	 * @param args
	 * @author lihzh
	 * @date 2012-4-21 下午10:17:22
	 */
	public static void main(String[] args) {
		try {
			ClassReader reader = new ClassReader("cn.home.practice.bean.ForReadClass");
			ClassNode cn = new ClassNode();
			reader.accept(cn, 0);
			System.out.println(cn.name);
			List<FieldNode> fieldList = cn.fields;
			for (FieldNode fieldNode : fieldList) {
				System.out.println("Field name: " + fieldNode.name);
				System.out.println("Field desc: " + fieldNode.desc);
				System.out.println("Filed value: " + fieldNode.value);
				System.out.println("Filed access: " + fieldNode.access);
        		}
		} catch (IOException e) {
			e.printStackTrace();
		}
	}
```
	
代码很简单，并且语义也很清晰。Tree API，顾名思义是根据Class的结构，一层层读取其中的信息。但是，当我打印出值的时候，结果却让我大跌眼镜。所有vlaue都是**null**。

> 注：第一次读取的时候ForReadClass中，只有三个变量，并且既不是final也不是基本数据类型
			
查看接口说明，发现其是从常量池中读取的值，并且要求filed类型必须是Integer/Double/....的。于是我又构造了几个final的和基本数据类型，如上所示。这次终于有值了。有值的都是 **final** 并且是基本数据类型的（String类型的必须是String s = "str"方式声明的，如果是new String("str")的也读取不到）
	
看似问题解决了一个，但是接下来的问题就是，那些非final和非基本数据类型的变量的值该如何获取呢？这个问题着实困扰了许久，google了一大顿（ps：还是翻墙的google）也没找到答案，网上用ASM的多是用其生成字节码。不死心我的决定自己研究。在网上的一篇博客中，我注意到一个样例，给出的是用MethodVisitor来改变一个变量的值。于是，我立即把目光从FieldNode转移到MethodNode之上。通过观察变异后class字节码，几番周折，有了如下代码：
	
```java
   /**
	 * @param args
	 * @author lihzh
	 * @date 2012-4-21 下午10:17:22
	 */
	public static void main(String[] args) {
		try {
			ClassReader reader = new ClassReader(
					"cn.home.practice.bean.ForReadClass");
			ClassNode cn = new ClassNode();
			reader.accept(cn, 0);
			List<MethodNode> methodList = cn.methods;
			for (MethodNode md : methodList) {
				System.out.println(md.name);
				System.out.println(md.access);
				System.out.println(md.desc);
				System.out.println(md.signature);
				List<LocalVariableNode> lvNodeList = md.localVariables;
				for (LocalVariableNode lvn : lvNodeList) {
					System.out.println("Local name: " + lvn.name);
					System.out.println("Local name: " + lvn.start.getLabel());
					System.out.println("Local name: " + lvn.desc);
					System.out.println("Local name: " + lvn.signature);
				}
				Iterator<AbstractInsnNode> instraIter = md.instructions.iterator();
				while (instraIter.hasNext()) {
					AbstractInsnNode abi = instraIter.next();
					if (abi instanceof LdcInsnNode) {
						LdcInsnNode ldcI = (LdcInsnNode) abi;
						System.out.println("LDC node value: " + ldcI.cst);
					}
				}
			}
			MethodVisitor mv = cn.visitMethod(Opcodes.AALOAD, "<init>", Type
					.getType(String.class).toString(), null, null);
			mv.visitFieldInsn(Opcodes.GETFIELD, Type.getInternalName(String.class), "str", Type
					.getType(String.class).toString());
			System.out.println(cn.name);
			List<FieldNode> fieldList = cn.fields;
			for (FieldNode fieldNode : fieldList) {
				System.out.println("Field name: " + fieldNode.name);
				System.out.println("Field desc: " + fieldNode.desc);
				System.out.println("Filed value: " + fieldNode.value);
				System.out.println("Filed access: " + fieldNode.access);
				if (fieldNode.visibleAnnotations != null) {
					for (AnnotationNode anNode : fieldNode.visibleAnnotations) {
						System.out.println(anNode.desc);
					}
				}
			}
		} catch (IOException e) {
			e.printStackTrace();
		} catch (SecurityException e) {
			e.printStackTrace();
		} catch (IllegalArgumentException e) {
			e.printStackTrace();
		}
	}
```

从AbstractInsnNode中，我终于取到了其他变量的值。
	
总结：之所以大费周章，主要还是因为我对Class字节码的不熟悉，网上之所以少有我遇到的问题，我想一方面是由于，我的使用场景与大多数人不同，另一方面可能是由于使用ASM的人大多对字节码还算了解，不会犯我这样的错误。：）
	
呵呵，总而言之，虽然耗费一定的时间，总归还有收获，心满意足。

