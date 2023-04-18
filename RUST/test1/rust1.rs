// fn print_char(value: &str) {
//     println!("a is {}", value);
// }

// fn main1() {
//     let x = "11112222 hello,world!";
//     print_char(x);
// }

// fn main2() {
//     let x = 5;

//     let y = {
//         let x = 3;
//         x + 1
//     };

//     println!("x 的值为 : {}", x);
//     println!("y 的值为 : {}", y);
// }

fn main() {
    println!(
        "程序运算的值为: {}    {}    {}",
        five(),
        add(11, 22),
        乘法(12, 23)
    );
}

fn five() -> i32 {
    5
}

fn add(a: i32, b: i32) -> i32 {
    let _ = a + b;
    999 //不可加分号
}

fn 乘法(a: i32, b: i32) -> i32 {
    return a * b;
}
