/***
 * @Description  : 头部注释
 * @Develop      : VSCode
 * @Author       : sandorn sandorn@live.cn
 * @Date         : 2024-06-24 11:33:11
 * @LastEditTime : 2024-06-25 10:02:35
 * @FilePath     : /CODE/RUST/ui/src/main.rs
 * @Github       : https://github.com/sandorn/home
 ***/
extern crate ferris_says;

use ferris_says::say; // from the previous step
use std::io::{stdout, BufWriter};

fn main() {
    let stdout = stdout();
    let message = String::from("Hello fellow Rustaceans!");
    let width = message.chars().count();

    let mut writer = BufWriter::new(stdout.lock());
    let message = String::from_utf8(message.as_bytes().to_vec()).unwrap();
    say(&message, width, &mut writer).unwrap();
    // say("Hello fellow Rustaceans!", 24, &mut writer).unwrap();
}
