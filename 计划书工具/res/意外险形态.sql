/*
 Navicat Premium Data Transfer

 Source Server         : localhost
 Source Server Type    : MySQL
 Source Server Version : 80015
 Source Host           : localhost:3306
 Source Schema         : baoxianjihuashu

 Target Server Type    : MySQL
 Target Server Version : 80015
 File Encoding         : 65001

 Date: 17/04/2019 12:21:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for 意外险形态
-- ----------------------------
DROP TABLE IF EXISTS `意外险形态`;
CREATE TABLE `意外险形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `产品名称` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `被保人年龄` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `缴费方式` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `航空保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `火车保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `轮船保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `公交车保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `其它公共交通保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `自驾乘保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `一般意外` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `疾病身故或全残` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `满期生存保险金` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 意外险形态
-- ----------------------------
BEGIN;
INSERT INTO `意外险形态` VALUES (1, '君康人寿', '君康安行保', '18-55周岁', '1/5/10年', '20倍保额', '10倍保额', '10倍保额', '10倍保额', '10倍保额', '10倍保额', '1倍保额', '所交保费总和的160%', '所交保费总和的110%'), (2, '富德生命', '安行无忧两全保险(2017版)', '18-60周岁', '1/3/5/10年 ', '350万', '100万', '100万', '100万', '100万', '100万', '10万', '已交保费*年龄系数', '20年：已交保费110%\n30年：已交保费125%'), (3, '人保健康', '百万安行个人交通意外伤害', '18-60周岁', '5/10年', '200万', '100万', '100万', '100万', '100万', '200万', '20万', '已交保费105%与现价两者取大', '已交保费125%'), (4, '中华人寿', '中华行', '18-55周岁', '1/5/10年', '200万', '100万', '100万', '100万', '100万', '100万', '10万', '已交保费160%', '已交保费100%'), (5, '恒安标准', '百万畅行两全保险（计划二）', '18-55周岁', '10年', '100万', '100万', '100万', '100万', '100万', '100万', '20万', '已交保费160%', '已交保费125%');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
