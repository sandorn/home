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

 Date: 28/04/2019 12:08:18
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for 百万医疗形态
-- ----------------------------
DROP TABLE IF EXISTS `百万医疗形态`;
CREATE TABLE `百万医疗形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `产品名称` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `被保人年龄` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `保障期间` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `缴费方式` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `基本保额` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `续保年龄` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `医疗保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `报销范围` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `保障区域` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `医院范围` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `年免赔额` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `赔付比例` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `特色服务` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `投保条件` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of 百万医疗形态
-- ----------------------------
BEGIN;
INSERT INTO `百万医疗形态` VALUES (1, '长城人寿', '医享无忧百万医疗保险（方案一）', '30天-65周岁', '1年', '年交', '100万', '100岁', '一般医疗保险金\n100种重大疾病医疗保险金', '床位费、膳食费、药品费、材料费、医生费（诊疗费）、治疗费、护理费、检查化验、手术费、器官移植费', '中国大陆', '二级或二级以上公立医院普通部', '1万', '100%（经社保报销）/60%（未经社保报销)', '/', '附加投保'), (2, '长城人寿', '医享无忧百万医疗保险（方案二）', '30天-65周岁', '1年', '年交', '200万', '100岁', '一般医疗保险金\n100种重大疾病医疗保险金', '床位费、膳食费、药品费、材料费、医生费（诊疗费）、治疗费、护理费、检查化验、手术费、器官移植费', '中国大陆', '二级或二级以上公立医院普通部', '1万', '100%（经社保报销）/60%（未经社保报销)', '/', '可独立投保'), (3, '中英人寿', '爱心保卓越医疗保险', '30天-65周岁', '1年', '年交', '200万', '100岁', '一般医疗保险金\n重大疾病医疗保险金', '住院医疗费用、特殊门诊医疗费用、门诊手术医疗费用、住院前后门急诊医疗费用、', '中国大陆（不含港澳台）', '二级或二级以上公立医院普通部', '1万', '100%（经社保报销）60%（未经社保报销)', '/', '可独立投保'), (4, '君康人寿', '百万保医疗保险', '28天-65周岁', '1年', '年交', '200万', '终身', '一般医疗保险金100万 \n 50种重疾医疗保险金100万', '床位费、膳食费、护理费、检查检验费、治疗费、药品费（含进口药）、救护车使用费、手术费、器官移植后的门诊抗排异治疗费用、住院前后各7日内急诊费用、门诊恶性肿瘤放化疗费用、门诊肾透析费用', '中国大陆（不含港澳台）', '二级或二级以上公立医院普通部', '1万（经社保报销）/2万未经社保报销）', '100%（经社保报销）/60%（未经社保报销)', '就医绿通', '可独立投保'), (5, '和谐健康', '尊崇佰万医疗保险', '28天-65周岁', '1年', '年交', '100万', '75周岁', '100万一般医疗保险金\n100万元恶性肿瘤医疗保险金\n1万元重大疾病保险金', '床位费、膳食费、手术费、药品费、治疗费、护理费、检查检验费、救护车使用费', '中国大陆（不含港澳台）', '二级或二级以上公立医院普通部', '1万', '100%（经社保报销）/60%（未经社保报销)', '/', '可独立投保'), (6, '复星保德信', '悦享守护医疗保险', '30天-55周岁', '1年', '年交', '100万', '99周岁', '100万一般医疗保险金', '床位费、膳食费、床位费、膳食费、护理费、手术费、诊疗费、检查检验费、治疗费、药品费、物理治疗费', '中国大陆（不含港澳台）', '二级或二级以上公立医院普通部', '1万', '100%（经社保报销）/60%（未经社保报销)', '/', '可独立投保'), (7, '复星联合', '乐享一生医疗保险', '30天-60周岁', '5年', '1/3/5年', '200万', '80周岁', '住院医疗保险金\n特殊门诊医疗保险金\n恶性肿瘤医疗保险金', '床位费、膳食费、护理费、重症监护室费、检查检验费、手术费、麻醉费、药品费、材料费、医疗机构拥有的医疗设备使用费、治疗费、医生费、会诊费、陪床费、住院前或住院期间转诊时发生的同城急救车费', '中国大陆（不含港澳台）', '二级或二级以上公立医院普通部', '0/5千/1万', '100%（经社保报销）/60%（未经社保报销)', '/', '可独立投保');
COMMIT;

-- ----------------------------
-- Table structure for 定期寿险形态
-- ----------------------------
DROP TABLE IF EXISTS `定期寿险形态`;
CREATE TABLE `定期寿险形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `产品` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `投保年龄` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `保障期间` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `等待期` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `身故责任` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `全残责任` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `其他责任` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 5 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of 定期寿险形态
-- ----------------------------
BEGIN;
INSERT INTO `定期寿险形态` VALUES (1, '弘康人寿', '大白定期寿险', '20-50岁', '10/20/30年/至60岁/至70岁', '疾病365天;\n意外180天', '保额', '保额', '生命末期：提前60%保额豁免保费'), (2, '中华人寿', '怡恒', '18-50岁', '30年/保至60/65/70/75岁', '180天', '保额', '保额', '/'), (3, '恒安标准', '爱的延续', '18-60岁', '10/15/20/30年/至55/60/65/70岁', '180天', '保额', '保额', '无息返还：等待期内身故或全残返还已交保费'), (4, '君康人寿', '爱特保', '18-65岁', '至70岁', '90天', '疾病：18-40岁，保额与已交保费160%取大;\n41-60岁，保额与已交保费140%取大\n;61岁以上，保额与已交保费120%取大\n;意外：100倍保额', '疾病：18-40岁，保额与已交保费160%取大;\n41-60岁，保额与已交保费140%取大\n;61岁以上，保额与已交保费120%取大\n;意外：100倍保额', '/');
COMMIT;

-- ----------------------------
-- Table structure for 防癌险形态
-- ----------------------------
DROP TABLE IF EXISTS `防癌险形态`;
CREATE TABLE `防癌险形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `保险公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `产品名称` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `投保范围` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `交费期间` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `保险期间` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `等待期` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `原位癌` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `轻症保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `癌症保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `身故保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `全残保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `特定癌症` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 8 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of 防癌险形态
-- ----------------------------
BEGIN;
INSERT INTO `防癌险形态` VALUES (1, '恒安标准', '老年恶性肿瘤危重疾病保险B款', '50-75周岁', '5/10/15/20年', '终身', '180天', '50%保额', '/', '保额', '已交保费与现价取大', '已交保费与现价取大', '/'), (2, '复星保德信', '孝顺康恶性肿瘤疾病保险A款', '50-75岁', '5/10/15/20年', '终身', '180天', '/', '/', '保额', '已交保费与现价取大', '/', '/'), (3, '恒安标准', '一生无忧恶性肿瘤危重疾病保险', '30天-49周岁', '1/5/10/15/20年', '终身', '180天', '25%保额', '/', '保额', '已交保费与现价取大', '已交保费与现价取大', '/'), (4, '中英人寿', '附加爱无限恶性肿瘤疾病保险', '30天-60周岁', '1/3/5/10/15/19/20年', '终身', '90天', '/', '已交保费', '保额', '现价', '/', '/'), (5, '人保健康', '北肿防癌管家个人疾病保险（B款）', '28天-60周岁', '1/5/10/15/20/30年', '终身', '180天', '/', '/', '保额', '已交保费与现价取大', '/', '轻度恶性肿瘤：10%保额（北大肿瘤100%比例、其他90%比例）'), (6, '人保健康', '北肿防癌管家个人疾病保险（A款）', '28天-60周岁', '1/5/10/15/20/30年', '保至80周岁', '180天', '/', '/', '保额', '已交保费与现价取大', '/', '轻度恶性肿瘤：10%保额'), (7, '中荷人寿', '乐无忧恶性肿瘤疾病保险', '46-75岁', '5/10/20年', '终身', '180天', '/', '/', '保额', '已交保费', '已交保费', '20%保额');
COMMIT;

-- ----------------------------
-- Table structure for 健康险形态
-- ----------------------------
DROP TABLE IF EXISTS `健康险形态`;
CREATE TABLE `健康险形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `保险公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `产品名称` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `被保人年龄` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `交费期间` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `保障期限` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `等待期` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `轻症种类` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `轻症分组` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `轻症赔付次数` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `轻症保额` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `轻症间隔` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `中症种类` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `中症分组` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `中症赔付次数` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `中症保额` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `中症间隔` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `重疾种类` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `重疾分组` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `重疾赔付次数` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `重疾保额` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `重疾额外赔付` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `重疾间隔` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `身故保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `全残保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `疾病终末期` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `被保人豁免` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `投保人豁免` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `附加两全险` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 29 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of 健康险形态
-- ----------------------------
BEGIN;
INSERT INTO `健康险形态` VALUES (1, '君康人寿', '多倍宝至尊版', '28天-60周岁', '1/5/10/15/20年', '终身', '90天', '35种', '不分组', '3次', '第一次30%保额；\n第二次35%保额；\n第三次40%保额。', '无间隔期', '20种', '不分组', '2次', '50%保额', '无间隔期', '105种', '4组', '4次', '首次为已交保费、现价、基本保额中较大者；2-4次100%保额', '/', '180天', '18周岁前，200%已交保费；\n18周岁后，MAX(保额,保费，现价）；\n重疾、身故、全残、疾病终末期，只赔付其中一项', '18周岁前，200%已交保费；\n18周岁后，MAX(保额,保费，现价）；\n重疾、身故、全残、疾病终末期，只赔付其中一项', '18周岁前，200%已交保费；\n18周岁后，MAX(保额,保费，现价）；\n重疾、身故、全残、疾病终末期，只赔付其中一项', '轻症、中症、重疾豁免', '自带，轻症、中症、重疾、身故、全残、疾病终末期、豁免', '可选，附加两全：祝寿金75岁返还总保费；\n身故保险金：MAX（主附险总保费，160%附加险保费）'), (2, '中华人寿', '中华福', '30天-60周岁', '5/10/15/19/20/30年', '终身', '90天', '40种', '不分组', '3次', '30%保额', '90天', '20种', '不分组', '2次', '50%保额', '90天', '100种', '不分组', '2次', '100%保额', '恶性肿瘤增加20%赔付', '365天', '18周岁前，200%已交保费；\n18周岁后，保额', '18周岁前，200%已交保费；\n18周岁后，保额', '18周岁前，200%已交保费；\n18周岁后，保额', '早期危重疾病、中症、重疾豁免', '附加，早期危重疾病、中症、重疾、身故、全残、疾病终末期豁免', '/'), (3, '中英人寿', '爱守护', '30天-60周岁', '1/3/5/10/15/20年', '终身', '90天', '20种', '不分组', '2次', '20%保额', '180天', '无', '无', '无', '无', '无', '80种', '不分组', '2次', '100%保额', '恶性肿瘤增加20%赔付', '365天', '18岁周前，已交保费；\n18周岁后保额', '18岁周前，已交保费；\n18周岁后保额', '18岁周前，已交保费；\n18周岁后保额', '轻症/重疾', '轻症/重疾/全残/身故豁免', '/'), (4, '北京人寿', '京康源', '28天-60周岁', '1/3/5/10/15/20/25/30年', '终身', '90天', '35种', '分5组', '5次', '30%保额', '无间隔期', '25种', '分5组', '5次', '60%保额', '无间隔期', '105种', '分5组', '5次', '100%保额', '/', '180天', '18周岁前，300%已交保费；\n18周岁后保额\n重疾、身故、全残、疾病终末期，只赔付其中一项', '18周岁前，300%已交保费；\n18周岁后保额\n重疾、身故、全残、疾病终末期，只赔付其中一项', '18周岁前，300%已交保费；\n18周岁后保额\n重疾、身故、全残、疾病终末期，只赔付其中一项', '轻症、中症、重疾豁免', '轻症/中症/重疾/全残/身故豁免', '主险不终止：65岁/70岁/75岁\n返还主、附险保费'), (5, '长城人寿', '吉康人生', '30天-60周岁', '1/3/5/10/15/20/30年', '终身', '90天', '40种', '不分组', '3次', '30%保额', '无间隔期', '25种', '不分组', '2次', '50%保额', '无间隔期', '100种', '不分组', '2次', '首次重疾已交保费、现价与保额三者取大，二次重疾100%保额', '首次重疾为急性心梗或脑中风后遗症，5年后再次发生同一种疾病，可以二次赔付100%保额 ', '365天', '18岁周前，200%已交费；\n18周岁后保额\n疾病终末期，保额/现价/已交保费三者取大', '18岁周前，200%已交费；\n18周岁后保额\n疾病终末期，保额/现价/已交保费三者取大', '18岁周前，200%已交费；\n18周岁后保额\n疾病终末期，保额/现价/已交保费三者取大', '轻症、中症、重疾豁免', '1，投保人在缴费期内发生轻症，中症，重疾，身故，全残，豁免整单后续保费。\n2，投保人过了缴费期后，发生重疾/身故/全残时退还投保人豁免险保费。                                                                                               3，过了缴费期后，被保人发生身故风险，保单结束时退还投保人豁免险保费。', '主险不终止：55岁/66岁/77岁/88岁\n返还主、附险保费'), (6, '复星保德信', '星满意', '30天-60周岁', '5/10/15/20/30年', '终身', '90天', '40种', '不分组', '3次', '第一次20%保额\n第二次30%保额\n第三次40%保额', '180天', '无', '无', '无', '无', '无', '100种', '5组', '5次', '第一次100%保额\n第二次110%保额\n第三次120%保额\n第四次130%保额\n第五次140%保额', '/', '180天', '18岁周前，已交保费；\n18周岁后保额', '/', '18岁周前，已交保费；\n18周岁后保额', '轻症/重疾', '轻症/重疾', '/'), (7, '工银安盛', '御享人生', '30天-60周岁', '5/10/15/20/30年', '终身', '90天', '30种', '4组', '3次', '20%保额', '180天', '无', '无', '无', '无', '无', '80种', '4组', '3次', '100%保额', '/', '180天', '18岁周前，已交保费；\n18周岁后保额', '/', '/', '轻症/重疾', '轻症/重疾', '/'), (8, '富德生命', '倍健康', '0-65周岁', '1/3/5/10/15/19/20年', '终身', '90天', '32种', '不分组', '5次', '30%保额', '无', '20种', '不分组', '2次', '60%保额', '无', '108种', '5组', '5次', '100%保额', '/', '180天', '18岁周前，已交保费*300%；\n18周岁后保额', '18岁周前，已交保费*300%；\n18周岁后保额', '/', '轻症/中症/重疾', '60岁前意外身故/全残豁免', '有'), (9, '爱心人寿', '爱加倍', '28天-60周岁', '1/3/5/10/15/20/30年', '终身', '90天', '30种', '不分组', '3次', '第一次30%保额\n第二次40%保额\n第三次40%保额', '无', '30种', '不分组', '2次', '第一次50%保额\n第二次60%保额', '无', '105种', '不分组', '2次', '首次保额、已交保费、现价取大\n第二次100%保额\n第二次恶性肿瘤100%保额', '第二次恶性肿瘤100%保额', '1年/3年二次恶肿', '18周岁前，已交保费200%;\n18周岁后，已交保费、现价与保额三者取大', '18周岁前，已交保费200%;\n18周岁后，已交保费、现价与保额三者取大', '已交保费、现价与保额三者取大', '轻症/中症/重疾', '轻症/中症/重疾/终末期疾病/全残/身故豁免', '有'), (10, '君康人寿', '多倍保', '28天-65周岁', '1/5/10/15/20年', '终身', '90天', '50种', '5组', '5次', '20%保额', '180天', '/', '/', '/', '/', '/', '100种', '5组', '5次', '保额', '/', '180天', '18周岁前，已交保费200%;\n18周岁后，保额', '18周岁前，已交保费200%;\n18周岁后，保额', '18周岁前，已交保费200%;\n18周岁后，保额', '轻症/重疾', '/', '/'), (11, '泰康人寿', '乐安康', '30天-60周岁', '1/5/10/15/20年', '终身', '180天', '22种', '不分组', '3次', '20%保额', '/', '/', '/', '/', '/', '/', '60种', '', '', '保额', '/', '/', '18周岁前，已交保费\n18周岁后，保额', '/', '/', '轻症豁免', '/', '/'), (12, '中华人寿', '怡康终身', '30天-60周岁', '5/10/15/20/30年', '终身', '90天', '50种', '', '3次', '20%保额\n25%保额\n30%保额', '90天', '/', '/', '/', '/', '/', '110种', '', '', '18岁前，200%保额\n18-75岁，保额\n75岁后，130%保额', '/', '/', '18岁前，200%已交保费;\n18-75岁，保额;\n75岁后，130%保额', '18岁前，200%已交保费;\n18-75岁，保额;\n75岁后，130%保额', '18岁前，200%已交保费;\n18-75岁，保额;\n75岁后，130%保额', '', '有', '/'), (13, '中英人寿', '爱加倍', '30天-60周岁', '1/3/5/10/15/20年', '终身', '90天', '20种', '', '2次', '50%保额', '180天', '/', '/', '/', '/', '/', '88种', '', '', '保额', '特定疾病300%保额\n高费用疾病500%保额', '365天', '18岁前，200%已交保费;\n18岁后，200%保额', '/', '/', '轻症/重疾豁免', '有', '/'), (14, '复星联合', '小保倍', '30天-50周岁', '1/5/10/15/20/30年', '终身', '180天', '35种', '5组', '3次', '30%保额', '/', '/', '/', '/', '/', '/', '80种', '2组', '2次', '保额', '特定疾病保额/2次', '365天', '18岁前，已交保费;\n18岁后，保额', '/', '/', '轻症/重疾豁免', '有', '/'), (15, '陆家嘴国泰', '佑安康', '0-60周岁', '5/10/15/20/30年', '终身', '90天', '30种', '/', '3次', '25%保额', '/', '/', '/', '/', '/', '/', '70种', '/', '1次', '保额', '/', '/', '18岁前，已交保费;\n18岁后，保额', '18岁前，已交保费;\n18岁后，保额', '18岁前，已交保费;\n18岁后，保额', '轻症豁免', '有', '/'), (16, '陆家嘴国泰', '佑享安康', '28天-50周岁', '10/19/20/28/30年', '终身', '90天', '30种', '/', '3次', '30%保额', '/', '20种', '/', '2次', '50%保额', '/', '100种', '4组', '3次', '保额/现价/已交保费三者取大\n保额\n保额', '特定重大疾病1.2倍', '365天', '18岁前，200%已交保费;\n18岁后，保额/现价/已交保费三者取大', '18岁前，200%已交保费;\n18岁后，保额/现价/已交保费三者取大', '18岁前，200%已交保费;\n18岁后，保额/现价/已交保费三者取大', '轻症/中症豁免', '有', '/'), (17, '陆家嘴国泰', '佑添安康', '28天-60周岁', '1/5/10/15/20/30年', '终身', '90天', '48种', '/', '2次', '30%保额', '/', '/', '/', '/', '/', '/', '88种', '/', '1次', '18岁前，200%保额\n18岁后，保额（65岁前保额，65岁后135%保额）/现价/已交保费三者取大', '长期看护：65周岁后每月给付保险金的1/120，最长十年。', '/', '18岁前，200%已交保费;\n18岁后，保额/现价/已交保费三者取大', '18岁前，200%已交保费;\n18岁后，保额/现价/已交保费三者取大', '18岁前，200%已交保费;\n18岁后，保额/现价/已交保费三者取大', '轻症豁免', '/', '√'), (18, '弘康人寿', '哆啦a保', '30天-65周岁', '1/3/5/10/15/20/30年', '终身', '180天', '55种', '4组', '2次', '30%保额', '180天', '/', '/', '/', '/', '/', '105种', '4组', '3次', '保额', '/', '180天', '18岁前，已交保费；\n18岁后，保额', '/', '/', '轻症/重疾豁免', '/', '/'), (19, '光大永明', '童佳保', '30天-55周岁', '1/5/10/15/19/20年', '终身', '90天', '35种', '/', '3次', '30%保额', '/', '20种', '/', '1/5/10/15/19/20年', '50%保额', '/', '100种', '/', '/', '保额', '/', '/', '18岁前，200%已交保费；\n18岁后，保额', '18岁前，200%已交保费；\n18岁后，保额', '18岁前，200%已交保费；\n18岁后，保额', '轻症/中症豁免', '轻症，重疾，疾病终末期，高残，身故', '/'), (20, '信泰人寿', '百万无忧', '28天-60周岁', '1/3/5/10/15/20/30年', '终身', '90天', '30种', '/', '2次', '30%保额', '90天', '20种', '/', '2次', '50%保额', '90天', '104种', '2组', '4', '重疾：保额\n恶性肿瘤：保额，3年后复发，持续，转移，新发可再赔付一次', '/', '180天', '18岁前，200%已交保费；\n18岁后，保额', '18岁前，200%已交保费；\n18岁后，保额', '/', '轻症/中症/重疾豁免', '有', '有'), (21, '复星保德信', '星悦', '30天-50周岁', '5/10/15/20/30年', '终身', '180天', '35种', '/', '3次', '30%保额\n35%保额\n40%保额', '/', '20种', '/', '2次', '50%保额', '/', '100种', '/', '1', '保额', '特定130%\n特定高龄170%', '/', '已交保费', '/', '/', '轻症/中症', '有', '有'), (22, '泰康人寿', '乐安心', '30天-60周岁', '1/5/10/15/20年', '终身', '180天', '30种', '/', '3次', '20%保额', '/', '/', '/', '/', '/', '/', '60种', '/', '1', '保额', '/', '/', '18岁前，已交保费；\n18岁后，未患重疾已交保费与保额取大；\n18岁后，患重疾5年内已交保费与保额取大给付50%；\n18岁后，患重疾5年后已交保费与保额取大', '/', '/', '轻症/重疾', '有', '/'), (23, '中荷人寿', '一生关爱G款', '30天-55周岁', '5/10/15/20/30年', '106岁', '180天', '45种', '5组', '5次', '30%保额', '365天', '/', '/', '/', '/', '/', '90种', '5组', '5次', '保额', '/', '365天', '18岁前，已交保费；\n18岁后，保额', '/', '/', '/', '/', '/'), (24, '弘康人寿', '健康一生A款', '30天-55周岁', '15/20/30年', '终身', '180天', '/', '/', '/', '/', '/', '/', '/', '/', '/', '/', '50种', '/', '1', '保额', '/', '/', '/', '/', '/', '/', '/', '/'), (25, '恒安标准', '臻爱健康', '0-65周岁', '1/5/10/15/20年', '终身', '180天', '/', '/', '/', '额外附加', '/', '/', '/', '/', '/', '/', '75种', '/', '1', '保额', '/', '/', '18岁前，已交保费与现价取大；\n18岁后，保额', '18岁前，已交保费与现价取大；\n18岁后，保额', '/', '轻症', '/', '/'), (26, '恒安标准', '臻爱倍护', '30天-60周岁', '1/5/10/15/20年', '终身', '90天', '35种', '/', '3次', '30%保额', '90天', '/', '/', '/', '/', '/', '100种', '3组', '3次', '保额', '/', '180天', '18岁前，已交保费与现价取大；\n18岁后，保额、现价与已交保费三者取大', '18岁前，已交保费与现价取大；\n18岁后，保额、现价与已交保费三者取大', '18岁前，已交保费与现价取大；\n18岁后，保额、现价与已交保费三者取大', '轻症/重疾', '/', '/'), (27, '恒安标准', '臻爱倍护（尊享版）', '30天-60周岁', '1/5/10/15/20年', '终身', '90天', '35种', '/', '3次', '30%保额', '90天', '/', '/', '/', '/', '/', '100种', '3组', '3次', '保额', '特定保险金：保额', '180天', '18岁前，已交保费与现价取大；\n18岁后，保额、现价与已交保费三者取大', '18岁前，已交保费与现价取大；\n18岁后，保额、现价与已交保费三者取大', '18岁前，已交保费与现价取大；\n18岁后，保额、现价与已交保费三者取大', '轻症/重疾', '/', '/'), (28, '复星联合', '星相印', '30天-60周岁', '', '终身', '90天', '40种', '/', '5次', '30%保额\n35%保额\n40%保额\n45%保额\n50%保额', '/', '25种', '/', '2次', '50%保额', '/', '108种', '6组', '6次', '100%保额\n110%保额\n120%保额\n130%保额\n140%保额\n150%保额', '特定保险金：30%保额', '180天', '保额', '保额', '保额', '/', '/', '/');
COMMIT;

-- ----------------------------
-- Table structure for 意外险形态
-- ----------------------------
DROP TABLE IF EXISTS `意外险形态`;
CREATE TABLE `意外险形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `产品名称` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `保险公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `投保人年龄` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `缴费方式` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `航空保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `火车保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `轮船保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `公交车保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `其它公共交通保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `自驾乘保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `一般意外` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `疾病身故或全残` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `满期生存保险金` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of 意外险形态
-- ----------------------------
BEGIN;
INSERT INTO `意外险形态` VALUES (1, '安行保', '君康人寿', '18-55周岁', '1/5/10年', '20倍保额', '10倍保额', '10倍保额', '10倍保额', '10倍保额', '10倍保额', '1倍保额', '所交保费总和的160%', '所交保费总和的110%'), (2, '安行无忧两全保险(2017版)', '富德生命', '18-60周岁', '1/3/5/10年 ', '350万', '100万', '100万', '100万', '100万', '100万', '10万', '已交保费*年龄系数', '20年：已交保费110%\n30年：已交保费125%'), (3, '百万安行个人交通意外伤害', '人保健康', '18-60周岁', '5/10年', '200万', '100万', '100万', '100万', '100万', '200万', '20万', '已交保费105%与现价两者取大', '已交保费125%'), (4, '中华行', '中华人寿', '18-55周岁', '1/5/10年', '200万', '100万', '100万', '100万', '100万', '100万', '10万', '已交保费160%', '已交保费100%'), (5, '百万畅行两全保险（计划二）', '恒安标准', '18-55周岁', '10年', '100万', '100万', '100万', '100万', '100万', '100万', '20万', '已交保费160%', '已交保费125%');
COMMIT;

-- ----------------------------
-- Table structure for 终身寿险形态
-- ----------------------------
DROP TABLE IF EXISTS `终身寿险形态`;
CREATE TABLE `终身寿险形态`  (
  `index` int(8) NOT NULL AUTO_INCREMENT,
  `公司` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `产品名称` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `投保范围` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `交费年期` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `等待期` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `身故保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  `全残保障` varchar(256) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NULL DEFAULT NULL,
  PRIMARY KEY (`index`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 7 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci;

-- ----------------------------
-- Records of 终身寿险形态
-- ----------------------------
BEGIN;
INSERT INTO `终身寿险形态` VALUES (1, '泰康人寿', '尊享世家终身寿险', '30天-75周岁', '1/3/5/10/15/20年', '90天', '18岁前：已交保费与现价取大;\n18岁后：保额', '/'), (2, '弘康人寿', '弘利相传终身寿险', '30天-65周岁', '1/3/5/10/15/20年', '180天', '保额', '保额'), (3, '中英人寿', '爱永恒终身寿险', '30天-70周岁', '1/3/5/10/15/20年', '/', '18岁前：已交保费与现价\n;18岁后：保额', '18岁前：已交保费与现价\n;18岁后：保额'), (4, '中荷人寿', '家业常青D款', '30天-75周岁', '1/3/5/10年', '', '18岁前，已交保费与现价取大;\n18-61岁，保额、现价与已交保费160%三者取大;\n62岁后，保额、现价与已交保费120%三者取大', '/'), (5, '中荷人寿', '家业常青E款', '30天-75周岁', '1/3/5/10年', '', '18岁前，已交保费与现价取大;\n18-61岁，保额与已交保费160%取大;\n62岁后，保额、现价与已交保费120%三者取大', '/'), (6, '恒安标准', '臻悦人生', '30天-65周岁', '1/5/10/15/20年', '180天', '18岁前，已交保费与现价取大;\n18岁后，保额', '18岁前，已交保费与现价取大\n;18岁后，保额');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
