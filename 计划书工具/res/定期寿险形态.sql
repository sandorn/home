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

 Date: 17/04/2019 12:20:31
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for 定期寿险形态
-- ----------------------------
DROP TABLE IF EXISTS `定期寿险形态`;
CREATE TABLE `定期寿险形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `产品` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `投保年龄` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `保障期间` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `等待期` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `身故责任` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `全残责任` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `其他责任` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 定期寿险形态
-- ----------------------------
BEGIN;
INSERT INTO `定期寿险形态` VALUES (1, '弘康人寿', '大白定期寿险', '20-50岁', '10/20/30年/至60岁/至70岁', '疾病365天;\n意外180天', '保额', '/', '生命末期：提前60%保额豁免保费'), (2, '中华人寿', '怡恒', '18-50岁', '30年/保至60/65/70/75岁', '180天', '保额', '保额', '/'), (3, '恒安标准', '爱的延续', '18-60岁', '10/15/20/30年/至55/60/65/70岁', '180天', '保额', '保额', '无息返还：等待期内身故或全残返还已交保费'), (4, '君康人寿', '爱特保', '18-65岁', '至70岁', '90天', '疾病：18-40岁，保额与已交保费160%取大;\n41-60岁，保额与已交保费140%取大\n;61岁以上，保额与已交保费120%取大\n;意外：100倍保额', '疾病：18-40岁，保额与已交保费160%取大;\n41-60岁，保额与已交保费140%取大\n;61岁以上，保额与已交保费120%取大\n;意外：100倍保额', '/');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
