
package com.hanhf.demo;
 
val PI = 3.14 // const field
var x = 0 // normal field
 
// function
fun sum1(a: Int, b: Int): Int {
    return a + b
}
 
// simple function
fun sum2(a: Int, b: Int) = a + b
 
// function without return values, Unit is omitted
fun printSum(a: Int, b: Int) {
    println("sum of $a and $b is ${a + b}")
}
 
// val vs var
fun lanDemo1() {
    val a: Int = 1
    val b = 2
    val c: Int
    c = 3
    x += 1
    var y = 5
    y += 1
}
 
// String
fun lanDemo2() {
    var a = 1
    val s1 = "a is $a"
    a = 2
    val s2 = "${s1.replace("is", "was")}, but now is $a"
    println(s2)
}
 
// if expression
fun maxOf(a: Int, b: Int) = if(a > b) a else b
 
// nullable return value
fun parseInt(str: String): Int? {
    return str.toIntOrNull();
}
 
fun printProduct(arg1: String, arg2: String) {
    val x = parseInt(arg1)
    val y = parseInt(arg2)
 
    if(x !=null && y != null) {
        println(x * y)
    } else {
        println("either $arg1 or $arg2 is not a number")
    }
}
 
// is
fun getStringLength1(obj: Any): Int? {
    if(obj is String) {
        return obj.length
    }
    return null
}
 
// !is
fun getStringLength2(obj: Any): Int? {
    if(obj !is String) return null
    return obj.length
}
 
// for
fun forDemo() {
    val items = listOf("apple", "banana", "kiwifruit")
    for(item in items) {
        println(item)
    }
}

// while
fun whileDemo() {
    val items = listOf("apple", "banana", "kiwifruit")
    var i = 0
    while(i < items.size) {
        println("item at $i is ${items[i]}")
        i++
    }
}
 
fun desc(obj: Any): String =
    when(obj) {
        1           -> "One"
        "Hello"     -> "Greeting"
        is Long     -> "Long"
        !is String  -> "Not a string"
        else        -> "Unknown"
    }
 
fun main(args: Array<String>) {
    /*
    var result1 = sum1(10, 20)
    println(result1)
    var result2 = sum2(30, 40)
    println(result2)
    printSum(50, 60)
    */
    // lanDemo2()
    /*
    printProduct("10", "abc")
    printProduct("10", "20")
    */
    // forDemo()
    // whileDemo()
    println(desc(2L))
}
