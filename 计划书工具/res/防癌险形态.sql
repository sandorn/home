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

 Date: 17/04/2019 12:20:46
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for 防癌险形态
-- ----------------------------
DROP TABLE IF EXISTS `防癌险形态`;
CREATE TABLE `防癌险形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `保险公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `产品名称` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `投保范围` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `交费期间` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `保险期间` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `等待期` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `原位癌` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `轻症保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `癌症保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `身故保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `全残保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `特定癌症` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 防癌险形态
-- ----------------------------
BEGIN;
INSERT INTO `防癌险形态` VALUES (1, '恒安标准', '老年恶性肿瘤危重疾病保险B款', '50-75周岁', '5/10/15/20年', '终身', '180天', '50%保额', '/', '保额', '已交保费与现价取大', '已交保费与现价取大', '/'), (2, '复星保德信', '孝顺康恶性肿瘤疾病保险A款', '50-75岁', '5/10/15/20年', '终身', '180天', '/', '/', '保额', '已交保费与现价取大', '/', '/'), (3, '恒安标准', '一生无忧恶性肿瘤危重疾病保险', '30天-49周岁', '1/5/10/15/20年', '终身', '180天', '25%保额', '/', '保额', '已交保费与现价取大', '已交保费与现价取大', '/'), (4, '中英人寿', '附加爱无限恶性肿瘤疾病保险', '30天-60周岁', '1/3/5/10/15/19/20年', '终身', '90天', '/', '已交保费', '保额', '现价', '/', '/'), (5, '人保健康', '北肿防癌管家个人疾病保险（B款）', '28天-60周岁', '1/5/10/15/20/30年', '终身', '180天', '/', '/', '保额', '已交保费与现价取大', '/', '轻度恶性肿瘤：10%保额（北大肿瘤100%比例、其他90%比例）'), (6, '人保健康', '北肿防癌管家个人疾病保险（A款）', '28天-60周岁', '1/5/10/15/20/30年', '保至80周岁', '180天', '/', '/', '保额', '已交保费与现价取大', '/', '轻度恶性肿瘤：10%保额'), (7, '中荷人寿', '乐无忧恶性肿瘤疾病保险', '46-75岁', '5/10/20年', '终身', '180天', '/', '/', '保额', '已交保费', '已交保费', '20%保额');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
