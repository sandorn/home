/***
 * @Description  : 头部注释
 * @Develop      : VSCode
 * @Author       : sandorn sandorn@live.cn
 * @Date         : 2024-06-21 10:23:39
 * @LastEditTime : 2024-06-21 10:34:31
 * @FilePath     : /CODE/RUST/pachong/src/main.rs
 * @Github       : https://github.com/sandorn/home
 ***/
extern crate reqwest;
extern crate serde;
extern crate serde_json;

use reqwest::Client;
use serde::{Deserialize, Serialize};
use serde_json::{json, Value};

#[derive(Debug, Deserialize, Serialize)]
struct Data {
    username: String,
    total_fans: i32,
    total_videos: i32,
    // ...
}

fn main() {
    let client = Client::new();
    let proxy_host = "duoip";
    let proxy_port = 8000;

    let proxy = format!("http://{}:{}/", proxy_host, proxy_port);
    let client = client.proxy(reqwest::Proxy::http(proxy.as_str()).unwrap());

    let data = get_data_from_douyin(&client);

    println!("{:?}", data);
}

fn get_data_from_douyin(client: &Client) -> Data {
    let url = "http://www.douyin.com/api/v2/user/get_info?access_token=your_access_token";
    let response = client.get(url).send().unwrap();
    let json: Value = response.json().unwrap();
    let data = json["data"].as_object().unwrap();
    Data {
        username: data["username"].as_str().unwrap().to_string(),
        total_fans: data["total_fans"].as_i64().unwrap() as i32,
        total_videos: data["total_videos"].as_i64().unwrap() as i32,
        // ...
    }
}
