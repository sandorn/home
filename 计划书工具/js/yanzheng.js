$(function(){

RegInputDiv($("#groupForm"),$("#yanzheng"));
	RegInputDiv($("#oneForm"),$("#yanzheng2"));
	RegInputDiv($("#validateForm"),$("#validateReg"));
	RegInputDiv($("#zhuceForm"),$("#ZhuceYanzheg"));
	RegInputDiv($("#zhuceForm2"),$("#ZhuceYanzheg2"));
	
var pwdAnswer="";	
	function RegInputDiv(formId,yanzhengDiv){
	formId.find(".DeInfoInput .DeInfo_text").on("blur",function(){
		RegInput($(this),formId);
	})
	//判断input不能为空
	yanzhengDiv.on("click",function(){
		formId.find(".DeInfoInput .DeInfo_text").each(function(){
			return RegInput($(this),formId);
		})
	})
}
function RegInput(InputThis,formId){
	var errorTishi=InputThis.parent().find("label").text();
	var testVal=new RegExp(InputThis[0].dataset.regtest);
	var Regshow=InputThis.is(":visible");
	if(Regshow==false){
		return true;
	}else if(errorTishi=="图形验证码"){
		validateCode();
		return true;
	}else if(errorTishi=="证件类型" || errorTishi=="性别" || errorTishi=="找回密码问题"){
		return codeType(InputThis,errorTishi,formId);
		return true;
	}else if(errorTishi=="证件号码"){
		var codeSelect=$("#codeSelect option:selected").val();
		if(codeSelect=="身份证"){			
			return validateIdCard($("#codeNum input").val(),formId)
		}
		return true;
	}else if(errorTishi=="找回密码答案"){
		pwdAnswer=$("#pwdAnswer").val();
		return true;
	}
	if(testVal.test(InputThis.val())){
		formId.find(".errorShow").hide();
		return true;
	}else{
		formId.find(".errorShow").show().text("请输入正确的"+errorTishi);
		return false;
	};
}
//证件类型
function codeType(InputThis,errorTishi,formDiv){
	var codeSelect=InputThis.find(".codeSelect option:selected").val();
	if(codeSelect=="请选择"){
		formDiv.find(".errorShow").show().text("请选择"+errorTishi);
		return false;
	}else{
		formDiv.find(".errorShow").hide();
		return true;
	}
}
/*匹配身份证*/
function validateIdCard(idCard,formDiv) {
    //15位和18位身份证号码的正则表达式
    var regIdCard = /^(^[1-9]\d{7}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])\d{3}$)|(^[1-9]\d{5}[1-9]\d{3}((0\d)|(1[0-2]))(([0|1|2]\d)|3[0-1])((\d{4})|\d{3}[Xx])$)$/;

    //如果通过该验证，说明身份证格式正确，但准确性还需计算
    if (regIdCard.test(idCard)) {
        if (idCard.length == 18) {
            var idCardWi = new Array(7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2); //将前17位加权因子保存在数组里
            var idCardY = new Array(1, 0, 10, 9, 8, 7, 6, 5, 4, 3, 2); //这是除以11后，可能产生的11位余数、验证码，也保存成数组
            var idCardWiSum = 0; //用来保存前17位各自乖以加权因子后的总和
            for (var i = 0; i < 17; i++) {
                idCardWiSum += idCard.substring(i, i + 1) * idCardWi[i];
            }
            var idCardMod = idCardWiSum % 11;//计算出校验码所在数组的位置
            var idCardLast = idCard.substring(17);//得到最后一位身份证号码

            //如果等于2，则说明校验码是10，身份证号码最后一位应该是X
            if (idCardMod == 2) {
                if (idCardLast == "X" || idCardLast == "x") {
                	formDiv.find(".errorShow").hide();
                    return true;
                } else { 
                	formDiv.find(".errorShow").show().text("请输入正确的证件号码");
                    return false;
                }
            } else {
                //用计算出的验证码与最后一位身份证号码匹配，如果一致，说明通过，否则是无效的身份证号码
                if (idCardLast == idCardY[idCardMod]) {
                } else {
                	formDiv.find(".errorShow").show().text("请输入正确的证件号码");
                    return false;
                }
            }
        } else if (idCard.length == 15) {
        	formDiv.find(".errorShow").hide();
			return true;
        }
    } else {
    	formDiv.find(".errorShow").show().text("请输入正确的证件号码");
        return false;
    }
}
})