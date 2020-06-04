$(function(){
	//中间内容距尾部导航的距离
	$(".main").css("padding-bottom",$(".footerNav").outerHeight()+8+"px");
	CountSize();
	
	//复选框选中样式
	$(".checkedNum").each(function(i){
		var InputVal=$(this).parent().siblings().find("p:first-child span").text();
		$(this).attr({"id":"checked"+i,"value":InputVal});	
		$(this).next("label").attr("for","checked"+i);
	})
	//星级评分
	$(".star").on("click",function(){
		var StarIndex=$(".star").index(this);
		$(this).find("img").attr("src","img/star_05.png");
		$(this).prevAll(".star").each(function(i){
			$(this).find("img").attr("src","img/star_05.png");
		})
		$(this).nextAll(".star").each(function(i){
			$(this).find("img").attr("src","img/star_03.png");
		})
	})
	//验证是否为我司保险持有人
	$(".ModularTitle .OptInfoL input").on("click",function(){
		if($(this).prop("checked")){
			$("#registerBtn .BigBtn").hide().eq(0).show();
		}else{
			$("#registerBtn .BigBtn").hide().eq(1).show();
		}
	})
	////////////////验证码倒计时/////////////////	
	var validCode=true;
	$(".yanzhengBtn,.validateBtn").on("click",function  () {
		var time=60;
		var code=$(this);
		if (validCode) {
			validCode=false;
			code.addClass("yanzhengNumOn");
			var t=setInterval(function  () {
				time--;
				code.html(time+"秒");
				if (time==0) {
					clearInterval(t);
					code.html("重新获取");
					validCode=true;
					code.removeClass("yanzhengNumOn");
				}
			},1000)
		}
	})
	//下拉框样式
	$(".DeInfoInput select").change(function(){
		var seleVal=$(this).val();
		$(this).prev().text(seleVal);
	})
	//添加保单
	$(".switchMode").on("click",function(){
		if($(".DeInfoIphone").is(':visible')){
			$(".DeInfoEmail").show();
			$(".DeInfoIphone").hide();
		}else{
			$(".DeInfoEmail").hide();
			$(".DeInfoIphone").show();
		}
		CountSize();
	})
	createCode();

})
function CountSize(){
	//计算input宽度
	$(".DeInfoInput .DeInfo_text").each(function(){
		var DeInfoLabel=$(this).parent().find("label").outerWidth(true);
		$(this).css("width",$(this).parent().width()-DeInfoLabel-6+"px");
	})
	//计算input宽度
	$(".LoginInput .DeInfo_text").each(function(){
		var DeInfoLabel=$(this).parent().find("label").outerWidth(true);
		$(this).css("width",$(this).parent().width()-DeInfoLabel-25+"px");
	})
}


//图片验证码
var code;
var checkCodeInner=0;
function createCode() {
	code = "";
	var codeLength = 4; //验证码的长度
	var checkCode = document.getElementById("checkCode");            
	var codeChars = new Array(0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 
	'a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
	'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z'); //所有候选组成验证码的字符，当然也可以用中文的
	for (var i = 0; i < codeLength; i++) 
	{
		var charNum = Math.floor(Math.random() * 52);
    	code += codeChars[charNum];
	}
	if (checkCode) 
	{
    	//checkCode.className = "code";
		var p= checkCode.childNodes[0];
		p.innerHTML=code;; 
		$(p).hide();
		var pLength=p.innerHTML;
		var span= checkCode.getElementsByTagName("span"); 
		for(var i = 0; i < pLength.length; i++){ 
	    	span[i].innerHTML=pLength[i];  
		}                
	}
}
function validateCode() 
{
	var inputCode = $("#RegPic").val();
	if (inputCode.length <= 0) 
	{
		$(".errorShow").show().text("验证码不能为空");
		return false;
    }
    else if (inputCode.toUpperCase() != code.toUpperCase()) 
   {
        $(".errorShow").show().text("验证码不正确，请重新输入");
        createCode();
        return false;   
    }
    $(".errorShow").hide()
    return true;      
}   
