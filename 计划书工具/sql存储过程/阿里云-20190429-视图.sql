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

 Date: 29/04/2019 12:06:48
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- View structure for v中华福
-- ----------------------------
DROP VIEW IF EXISTS `v中华福`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v中华福` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '中华福');

-- ----------------------------
-- View structure for v中华行
-- ----------------------------
DROP VIEW IF EXISTS `v中华行`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v中华行` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`保险期间` AS `保险期间`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '中华行');

-- ----------------------------
-- View structure for v乐享一生
-- ----------------------------
DROP VIEW IF EXISTS `v乐享一生`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v乐享一生` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`投保方式` AS `投保方式`,`费率表`.`社保状态` AS `社保状态`,`费率表`.`年龄` AS `年龄`,`费率表`.`免赔额` AS `免赔额`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '乐享一生');

-- ----------------------------
-- View structure for v乐安心
-- ----------------------------
DROP VIEW IF EXISTS `v乐安心`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v乐安心` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '乐安心');

-- ----------------------------
-- View structure for v北肿防癌b款
-- ----------------------------
DROP VIEW IF EXISTS `v北肿防癌b款`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v北肿防癌b款` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`保险期间` AS `保险期间`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '北肿防癌B款');

-- ----------------------------
-- View structure for v吉康人生
-- ----------------------------
DROP VIEW IF EXISTS `v吉康人生`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v吉康人生` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`保险期间` AS `保险期间`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '吉康人生');

-- ----------------------------
-- View structure for v多倍
-- ----------------------------
DROP VIEW IF EXISTS `v多倍`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v多倍` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '多倍');

-- ----------------------------
-- View structure for v多倍保至尊版
-- ----------------------------
DROP VIEW IF EXISTS `v多倍保至尊版`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v多倍保至尊版` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '多倍保至尊版');

-- ----------------------------
-- View structure for v大白定期寿险
-- ----------------------------
DROP VIEW IF EXISTS `v大白定期寿险`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v大白定期寿险` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`保险期间` AS `保险期间`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '大白定期寿险');

-- ----------------------------
-- View structure for v安行保
-- ----------------------------
DROP VIEW IF EXISTS `v安行保`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v安行保` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`保险期间` AS `保险期间`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '安行保');

-- ----------------------------
-- View structure for v安行无忧
-- ----------------------------
DROP VIEW IF EXISTS `v安行无忧`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v安行无忧` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`保险期间` AS `保险期间`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '安行无忧');

-- ----------------------------
-- View structure for v御享人生
-- ----------------------------
DROP VIEW IF EXISTS `v御享人生`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v御享人生` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '御享人生');

-- ----------------------------
-- View structure for v星悦
-- ----------------------------
DROP VIEW IF EXISTS `v星悦`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v星悦` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '星悦');

-- ----------------------------
-- View structure for v星满意
-- ----------------------------
DROP VIEW IF EXISTS `v星满意`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v星满意` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '星满意');

-- ----------------------------
-- View structure for v爱加倍
-- ----------------------------
DROP VIEW IF EXISTS `v爱加倍`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v爱加倍` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`保险期间` AS `保险期间`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '爱加倍');

-- ----------------------------
-- View structure for v爱守护
-- ----------------------------
DROP VIEW IF EXISTS `v爱守护`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v爱守护` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '爱守护');

-- ----------------------------
-- View structure for v百万保
-- ----------------------------
DROP VIEW IF EXISTS `v百万保`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v百万保` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`年龄` AS `年龄`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '百万保');

-- ----------------------------
-- View structure for v百万安行
-- ----------------------------
DROP VIEW IF EXISTS `v百万安行`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v百万安行` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`保险期间` AS `保险期间`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限`,`费率表`.`费率` AS `费率` from `费率表` where (`费率表`.`产品名称` = '百万安行');

-- ----------------------------
-- View structure for v百万畅行(计划一)
-- ----------------------------
DROP VIEW IF EXISTS `v百万畅行(计划一)`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v百万畅行(计划一)` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`保险期间` AS `保险期间`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限` from `费率表` where (`费率表`.`产品名称` = '百万畅行(计划一)');

-- ----------------------------
-- View structure for v百万畅行(计划二)
-- ----------------------------
DROP VIEW IF EXISTS `v百万畅行(计划二)`;
CREATE ALGORITHM = UNDEFINED DEFINER = `sandorn`@`%` SQL SECURITY DEFINER VIEW `v百万畅行(计划二)` AS select `费率表`.`ID` AS `ID`,`费率表`.`产品名称` AS `产品名称`,`费率表`.`保险公司` AS `保险公司`,`费率表`.`产品大类` AS `产品大类`,`费率表`.`产品小类` AS `产品小类`,`费率表`.`保险期间` AS `保险期间`,`费率表`.`性别` AS `性别`,`费率表`.`年龄` AS `年龄`,`费率表`.`缴费期限` AS `缴费期限` from `费率表` where (`费率表`.`产品名称` = '百万畅行(计划二)');

SET FOREIGN_KEY_CHECKS = 1;
