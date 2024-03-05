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
        add(123, 456),
        multiply(12, 12)
    );
}

fn five() -> i32 {
    3 + 2
}

fn add(a: i32, b: i32) -> i32 {
    let c = a + b;
    c
}

fn multiply(a: i32, b: i32) -> i32 {
    a * b
}
