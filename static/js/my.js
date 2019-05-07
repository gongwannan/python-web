function $(id){
	return document.getElementById(id);
}
function scroll(){
		if(window.pageYOffset != null){
			//ie9+和各种最新浏览器，注意：为什么使用！=null,因为加载完页面pageYOffset就是0
			return {
				left: window.pageXOffset,
				top: window.pageYOffset
			}
		}else if(document.compatMode == "CSS1Compat"){
			//不是怪异模式(即声明了DTD)
			return {
				left: document.documentElement.scrollLeft,
				top: document.documentElement.scrollTop
			}
		}else{
			//怪异模式(未声明DTD)
			return {
				left: document.body.scrollLeft,
				top: document.body.scrollTop
			}
		}
	}