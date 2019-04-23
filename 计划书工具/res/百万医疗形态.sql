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

 Date: 17/04/2019 12:19:50
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for 百万医疗形态
-- ----------------------------
DROP TABLE IF EXISTS `百万医疗形态`;
CREATE TABLE `百万医疗形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `产品名称` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `被保人年龄` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `保障期间` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `缴费方式` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `基本保额` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `续保年龄` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `医疗保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `报销范围` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `保障区域` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `医院范围` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `年免赔额` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `赔付比例` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `特色服务` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  `投保条件` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of 百万医疗形态
-- ----------------------------
BEGIN;
INSERT INTO `百万医疗形态` VALUES (1, '长城人寿', '医享无忧百万医疗保险（方案一）', '30天-65周岁', '1年', '年交', '100万', '100岁', '一般医疗保险金\n100种重大疾病医疗保险金', '床位费、膳食费、药品费、材料费、医生费（诊疗费）、治疗费、护理费、检查化验、手术费、器官移植费', '中国大陆', '二级或二级以上公立医院普通部', '1万', '100%（经社保报销）/60%（未经社保报销)', '/', '附加投保'), (2, '长城人寿', '医享无忧百万医疗保险（方案二）', '30天-65周岁', '1年', '年交', '200万', '100岁', '一般医疗保险金\n100种重大疾病医疗保险金', '床位费、膳食费、药品费、材料费、医生费（诊疗费）、治疗费、护理费、检查化验、手术费、器官移植费', '中国大陆', '二级或二级以上公立医院普通部', '1万', '100%（经社保报销）/60%（未经社保报销)', '/', '可独立投保'), (3, '中英人寿', '爱心保卓越医疗保险', '30天-65周岁', '1年', '年交', '200万', '100岁', '一般医疗保险金\n重大疾病医疗保险金', '住院医疗费用、特殊门诊医疗费用、门诊手术医疗费用、住院前后门急诊医疗费用、', '中国大陆（不含港澳台）', '二级或二级以上公立医院普通部', '1万', '100%（经社保报销）60%（未经社保报销)', '/', '可独立投保'), (4, '君康人寿', '百万保医疗保险', '28天-65周岁', '1年', '年交', '200万', '终身', '一般医疗保险金100万 \n 50种重疾医疗保险金100万', '床位费、膳食费、护理费、检查检验费、治疗费、药品费（含进口药）、救护车使用费、手术费、器官移植后的门诊抗排异治疗费用、住院前后各7日内急诊费用、门诊恶性肿瘤放化疗费用、门诊肾透析费用', '中国大陆（不含港澳台）', '二级或二级以上公立医院普通部', '1万（经社保报销）/2万未经社保报销）', '100%（经社保报销）/60%（未经社保报销)', '就医绿通', '可独立投保'), (5, '和谐健康', '尊崇佰万医疗保险', '28天-65周岁', '1年', '年交', '100万', '75周岁', '100万一般医疗保险金\n100万元恶性肿瘤医疗保险金\n1万元重大疾病保险金', '床位费、膳食费、手术费、药品费、治疗费、护理费、检查检验费、救护车使用费', '中国大陆（不含港澳台）', '二级或二级以上公立医院普通部', '1万', '100%（经社保报销）/60%（未经社保报销)', '/', '可独立投保'), (6, '复星保德信', '悦享守护医疗保险', '30天-55周岁', '1年', '年交', '100万', '99周岁', '100万一般医疗保险金', '床位费、膳食费、床位费、膳食费、护理费、手术费、诊疗费、检查检验费、治疗费、药品费、物理治疗费', '中国大陆（不含港澳台）', '二级或二级以上公立医院普通部', '1万', '100%（经社保报销）/60%（未经社保报销)', '/', '可独立投保'), (7, '复星联合', '乐享一生医疗保险', '30天-60周岁', '5年', '1/3/5年', '200万', '80周岁', '住院医疗保险金\n特殊门诊医疗保险金\n恶性肿瘤医疗保险金', '床位费、膳食费、护理费、重症监护室费、检查检验费、手术费、麻醉费、药品费、材料费、医疗机构拥有的医疗设备使用费、治疗费、医生费、会诊费、陪床费、住院前或住院期间转诊时发生的同城急救车费', '中国大陆（不含港澳台）', '二级或二级以上公立医院普通部', '0/5千/1万', '100%（经社保报销）/60%（未经社保报销)', '/', '可独立投保');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
