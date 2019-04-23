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

 Date: 17/04/2019 12:21:16
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for 费率结构
-- ----------------------------
DROP TABLE IF EXISTS `费率结构`;
CREATE TABLE `费率结构`  (
  `ID` int(8) NOT NULL AUTO_INCREMENT,
  `产品名称` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `保险公司` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `产品大类` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `产品小类` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL,
  `字段1` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `字段2` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `字段3` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `字段4` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `字段5` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `字段6` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `字段7` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `字段8` varchar(64) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`, `产品名称`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 16 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 费率结构
-- ----------------------------
BEGIN;
INSERT INTO `费率结构` VALUES (1, '乐安心', '泰康人寿', '健康险', '重疾险', '性别', '年龄', '缴费期限', '费率', '', '', '', ''), (2, '安行保', '君康人寿', '意外险', '意外险', '保险期间', '年龄', '缴费期限', '费率', '', '', '', ''), (3, '百万保', '君康人寿', '医疗险', '百万医疗', '年龄', '费率', '', '', '', '', '', ''), (4, '北肿防癌B款', '人保健康', '健康险', '防癌险', '性别', '年龄', '缴费期限', '保险期间', '费率', '', '', ''), (5, '大白智能定期寿险', '弘康人寿', '寿险', '定期寿险', '性别', '年龄', '缴费期限', '保险期间', '费率', '', '', ''), (6, '中华福', '中华人寿', '健康险', '重疾险', '性别', '年龄', '缴费期限', '费率', '', '', '', ''), (7, '多倍保至尊版', '君康人寿', '健康险', '重疾险', '性别', '年龄', '缴费期限', '费率', '', '', '', ''), (8, '爱守护', '中英人寿', '健康险', '重疾险', '性别', '年龄', '缴费期限', '费率', '', '', '', ''), (9, '星满意', '复星保德信', '健康险', '重疾险', '性别', '年龄', '缴费期限', '费率', '', '', '', ''), (10, '御享人生', '工银安盛', '健康险', '重疾险', '性别', '年龄', '缴费期限', '费率', '', '', '', ''), (11, '星悦', '复星保德信', '健康险', '重疾险', '性别', '年龄', '缴费期限', '费率', '', '', '', ''), (12, '多倍', '弘康人寿', '健康险', '重疾险', '性别', '年龄', '缴费期限', '费率', '', '', '', ''), (13, '爱加倍', '爱心人寿', '健康险', '重疾险', '性别', '年龄', '缴费期限', '保险期间', '费率', '', '', ''), (14, '吉康人生', '长城人寿', '健康险', '重疾险', '性别', '年龄', '缴费期限', '保险期间', '费率', '', '', ''), (15, '乐享一生', '复星联合', '医疗险', '百万医疗', '投保方式', '社保状态', '年龄', '免赔额', '缴费期限', '费率', '', '');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
