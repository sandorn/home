/*
 Navicat Premium Data Transfer

 Source Server         : 阿里云
 Source Server Type    : MySQL
 Source Server Version : 50720
 Source Host           : rm-8vbdh9h80t8m9smmuqo.mysql.zhangbei.rds.aliyuncs.com:3306
 Source Schema         : bxflb

 Target Server Type    : MySQL
 Target Server Version : 50720
 File Encoding         : 65001

 Date: 29/04/2019 12:05:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `ID` int(8) NOT NULL AUTO_INCREMENT,
  `username` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `password` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `手机` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `代理人编码` varchar(24) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `会员级别` int(1) NULL DEFAULT NULL,
  `会员到期日` date NULL DEFAULT NULL,
  `登陆次数` int(1) UNSIGNED ZEROFILL NULL DEFAULT 0,
  `备注` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`ID`, `手机`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 3201 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
BEGIN;
INSERT INTO `users` VALUES (1001, 'sand', '123456', '13910110123', NULL, 9, '9999-12-31', NULL, NULL), (1002, 'sandorn', '123456', '13910110222', NULL, 9, '9999-12-31', NULL, NULL), (1003, 'lxj', '123456', '13910110111', NULL, 9, '9999-12-31', NULL, NULL), (2001, 'xhy', '123456', '13910110333', NULL, 9, '9999-12-31', NULL, NULL);
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
