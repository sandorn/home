/*
 * @Description  : 头部注释
 * @Develop      : VSCode
 * @Author       : sandorn sandorn@live.cn
 * @Date         : 2024-10-14 09:40:58
 * @LastEditTime : 2025-03-17 11:22:35
 * @FilePath     : /CODE/test/rust.rs
 * @Github       : https://github.com/sandorn/home
 */
use std::io::{self, Write};
fn main() {
    // 将字符串提取为常量，便于管理和维护
    const GREETING: &str = "Hello, world!中文";

    // 使用 write! 输出内容，并捕获潜在的错误
    if let Err(e) = write!(io::stdout(), "{}", GREETING) {
        // 捕获潜在的打印错误并输出到标准错误流
        eprintln!("Failed to print greeting: {}", e);
    }
}

fn main0() {
    println!("Hello, world!中文");
}
