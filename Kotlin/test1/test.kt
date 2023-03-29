class Greeter(val name: String) {
   fun greet() {
      println("Hello, $name")
   }
}

fun main() {
   Greeter("World!").greet()
   val tr = Greeter("HHHHHHHHHHH!")
   tr.greet()
   // 创建一个对象不用 new 关键字
}
