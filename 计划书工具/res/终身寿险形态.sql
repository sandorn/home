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

 Date: 17/04/2019 12:22:00
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for 终身寿险形态
-- ----------------------------
DROP TABLE IF EXISTS `终身寿险形态`;
CREATE TABLE `终身寿险形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `产品名称` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `投保范围` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `交费年期` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `等待期` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `身故保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `全残保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 终身寿险形态
-- ----------------------------
BEGIN;
INSERT INTO `终身寿险形态` VALUES (1, '泰康人寿', '尊享世家终身寿险', '30天-75周岁', '1/3/5/10/15/20年', '90天', '18岁前：已交保费与现价取大;\n18岁后：保额', '/'), (2, '弘康人寿', '弘利相传终身寿险', '30天-65周岁', '1/3/5/10/15/20年', '180天', '保额', '保额'), (3, '中英人寿', '爱永恒终身寿险', '30天-70周岁', '1/3/5/10/15/20年', '/', '18岁前：已交保费与现价\n;18岁后：保额', '18岁前：已交保费与现价\n;18岁后：保额'), (4, '中荷人寿', '家业常青D款', '30天-75周岁', '1/3/5/10年', '', '18岁前，已交保费与现价取大;\n18-61岁，保额、现价与已交保费160%三者取大;\n62岁后，保额、现价与已交保费120%三者取大', '/'), (5, '中荷人寿', '家业常青E款', '30天-75周岁', '1/3/5/10年', '', '18岁前，已交保费与现价取大;\n18-61岁，保额与已交保费160%取大;\n62岁后，保额、现价与已交保费120%三者取大', '/'), (6, '恒安标准', '臻悦人生', '30天-65周岁', '1/5/10/15/20年', '180天', '18岁前，已交保费与现价取大;\n18岁后，保额', '18岁前，已交保费与现价取大\n;18岁后，保额');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
