---
title: LeetCode  Integer To Roman
layout: post
tags: [LeetCode,Java]
date: 2017-10-16 14:08:24 +0800
comments: true
author: onecoder
thread_key: 1916
---
# Problem

Given an integer, convert it to a roman numeral.

Input is guaranteed to be within the range from 1 to 3999.

跟[Roman To Integer][1]是对应问题。即将整数转换成对应的罗马数字。罗马数字规则见wiki：[罗马数字规则][2]

<!--break-->

# Java 实现（个人解法）

``` java

package com.coderli.leetcode.algorithms.medium;

/**
 * Given an integer, convert it to a roman numeral.
 * <p>
 * Input is guaranteed to be within the range from 1 to 3999
 *
 * @author li.hzh
 */
public class IntegerToRoman {

    public static void main(String[] args) {
        IntegerToRoman integerToRoman = new IntegerToRoman();
        System.out.println(integerToRoman.intToRoman(1));
        System.out.println(integerToRoman.intToRoman(10));
        System.out.println(integerToRoman.intToRoman(90));
        System.out.println(integerToRoman.intToRoman(1437));
    }

    public String intToRoman(int num) {
        int times = 1;
        String result = "";
        while (num > 0) {
            int tempIntValue = num % 10;
            num /= 10;
            String tempStrValue = "";
            if (tempIntValue == 5) {
                switch (times) {
                    case 1:
                        result = tempStrValue = "V";
                        break;
                    case 2:
                        result = "L" + result;
                        break;
                    case 3:
                        result = "D" + result;
                        break;
                }
            } else if (tempIntValue % 5 <= 3) {
                int length = tempIntValue;
                switch (times) {
                    case 1:
                        if (tempIntValue > 5) {
                            tempStrValue = "V";
                            length = tempIntValue - 5;
                        }
                        for (int i = 0; i < length; i++) {
                            tempStrValue += "I";
                        }
                        result = tempStrValue + result;
                        break;
                    case 2:
                        if (tempIntValue > 5) {
                            tempStrValue = "L";
                            length = tempIntValue - 5;
                        }
                        for (int i = 0; i < length; i++) {
                            tempStrValue += "X";
                        }
                        result = tempStrValue + result;
                        break;
                    case 3:
                        if (tempIntValue > 5) {
                            tempStrValue = "D";
                            length = tempIntValue - 5;
                        }
                        for (int i = 0; i < length; i++) {
                            tempStrValue += "C";
                        }
                        result = tempStrValue + result;
                        break;
                    case 4:
                        for (int i = 0; i < tempIntValue; i++) {
                            tempStrValue += "M";
                        }
                        result = tempStrValue + result;
                        break;
                }
            } else {
                switch (times) {
                    case 1:
                        result = tempIntValue < 5 ? "IV" + result : "IX" + result;
                        break;
                    case 2:
                        result = tempIntValue < 5 ? "XL" + result : "XC" + result;
                        break;
                    case 3:
                        result = tempIntValue < 5 ? "CD" + result : "CM" + result;
                        break;
                }
            }
            times++;
        }
        return result;
    }

}


```

## 分析

上面解法其实受到了罗马转整数问题的惯性思维。把思维限制到了罗马数字只能用基础的I、V、X等元素上。罗马数字的规则不再介绍了。思路其实跟罗马转数字一致，抓住罗马数字其实也是个位、十位、百位等一位一位组合起来的，因此我们一位一位的生成对应的罗马数字即可。

正因为罗马数字也是一位一位对应的，因此网上流传一个简便的写法，代码很简洁：

```java

public static String change(int num) {
		String [][]str = 
			{
		            {"","I","II","III","IV","V","VI","VII","VIII","IX"},
		            {"","X","XX","XXX","XL","L","LX","LXX","LXXX","XC"},
		            {"","C","CC","CCC","CD","D","DC","DCC","DCCC","CM"},
		            {"","M","MM","MMM"}
			};
		String roman = (str[3][num / 1000 % 10])+(str[2][num / 100 % 10])+(str[1][num / 10 % 10])+(str[0][num % 10]);
		
		return roman;


```

把个十百千各位可能罗马字符准备好，然后直接计算整数对应位上的值，取出数组中对应索引位的罗马值拼到一起就可以了。


  [1]: http://www.coderli.com/leetcode-roman-to-integer/
  [2]: https://zh.wikipedia.org/wiki/%E7%BD%97%E9%A9%AC%E6%95%B0%E5%AD%97