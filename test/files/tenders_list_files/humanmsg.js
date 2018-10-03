/*
	HUMANIZED MESSAGES 1.0
	idea - http://www.humanized.com/weblog/2006/09/11/monolog_boxes_and_transparent_messages
	home - http://humanmsg.googlecode.com
*/
var humanMsg = {
		/*�������������*/
		setup: function(appendTo, logName, msgOpacity) {
			/*�������������� ���������*/
			humanMsg.msgID = 'humanMsg';
			humanMsg.logID = 'humanMsgLog';
			/*������� ���������*/
			humanMsg.count   = 0;
			/*��������� ������������ ��� ���������*/
			humanMsg.lastMsgType = -1;
			/*� ���� ��������� ��� ���������*/
			if (appendTo == undefined)
				appendTo = 'body';
			/*����� �������� ���� ���������*/
			humanMsg.logName   = logName||'Message Log';
			/*������������ ������������ ���������*/
			humanMsg.msgOpacity = 1;
			if (msgOpacity != undefined) 
				humanMsg.msgOpacity = parseFloat(msgOpacity);
			/*��������� ��� ���������*/
			jQuery(appendTo).append('<div id="'+humanMsg.msgID+'" class="humanMsg"></div><div id="'+humanMsg.logID+'"><p>'+logName+'</p><ul></ul></div>');
			/*��������� ������� �������� � �������� ����*/
			jQuery('#'+humanMsg.logID+' p').click(
				function() {
					var t = jQuery(this).siblings('ul');
					if (t.filter(':visible').size()){
						t.hide();
						if ($.browser.msie){
							t.css("height","")
						}
					} else {
						if ($.browser.msie){
							//t.css("height",Math.min(180,t.height()+2))
							//t.css("height",Math.min(180,t.height()+2)+"px")
						}
						if ($.browser.msie){t.show()}else{t.slideDown()};
					}
				}
			)
		}
		/*����������� ���������. �������� ���������, ������ ���������, ���������*/
	,	displayMsg: function(shortMsg,msg,msgType) {
			/*���� �� �������������������, ������*/
			if (!humanMsg.logID){
				humanMsg.setup('body', GLOBAL_MSG.get("message_log"));
			}
			/*��� ������ ��������� �������*/
			if (msg == '')
				return;
			/*������� ������ ������ ��*/
			//clearTimeout(humanMsg.t2);
			/*���������� ���������� ��������� � ������*/
			var handler=function() {
				jQuery('#'+humanMsg.logID)
					.show()												/*���������� ������*/
					.children('ul')								/*������� �������� ������*/
					.prepend('<li>'+msg+'</li>')	/*��������� � ������ ������*/
					.children('li:first')					/*��� ������������ ��������*/
					.slideDown(200)								/*������ �����*/
				/*����������� ������� ���������*/
				humanMsg.count++;
				/*������������������ ��������� ������ ���������*/
				$('#'+humanMsg.logID+' p').text(humanMsg.logName+' ('+humanMsg.count+')');
			}
			/*������� ������������� ���������� ������� ��� ������� ���������. �� �����������, ����� ��� ��� �� ������������*/
			var need_set=(jQuery('#'+humanMsg.msgID+':visible').size()==0);
			/*������� ��� ������������� ���������*/
			var msg_obj=jQuery('#'+humanMsg.msgID);
			/*��� ��������� ������ ��������� ������ ��� ����, ������� ��� ������ ������������, �� ���������� ������������*/
			if (this.lastMsgType<msgType){
				/*���������� ��������� ���������*/
				this.lastMsgType=msgType
				/*��������� ���������*/ 
				jQuery('#'+humanMsg.msgID).html(shortMsg)
				/*���������� ���������*/
				msg_obj.show().animate({ opacity: humanMsg.msgOpacity}, 200, handler)
			}else{
				/*��������� ���������*/
				msg_obj.show().animate({opacity: humanMsg.msgOpacity},200,handler)
			}
			/*���� ����, �� ��������� �������*/
			if (need_set){
				/*������ �� ��������� - ��� ������� ������� ���������*/
				humanMsg.t1 = setTimeout("humanMsg.bindEvents()", 100);
				/*������� ��������� ����� 5 ���. */
				humanMsg.t2 = setTimeout("humanMsg.removeMsg()", 5000);
			}
		}
		/*���������� ������� ��� ������� ���������*/
	,	bindEvents: function() {
			/*��� ����� � ��� ������� ������� ������� ���������*/
			jQuery(document)
				.bind('click', humanMsg.removeMsg)
				.bind('keypress', humanMsg.removeMsg)

				// .click(humanMsg.removeMsg)
				// .keypress(humanMsg.removeMsg)
		}
		/*������� ���������*/
	,	removeMsg: function(){
			/*������� ����������*/
			clearTimeout(humanMsg.t2);
			jQuery(document)
				.unbind('click', humanMsg.removeMsg)
				.unbind('keypress', humanMsg.removeMsg)
			/*���� ������ ������������, �� �������� ���*/
			if (jQuery('#'+humanMsg.msgID).css('opacity') == humanMsg.msgOpacity){
				var t=jQuery('#'+humanMsg.msgID).css('top');
				var w=jQuery('#'+humanMsg.msgID).css('width');
				var l=jQuery('#'+humanMsg.msgID).css('left');
				jQuery('#'+humanMsg.msgID).animate(
						{
								top: 0
							,	width:220
							,	left:document.body.clientWidth/2-110
							,	opacity:0.1
						}
					, 500
					, function(){
							jQuery(this)
							.hide()
							.css("top",t)
							.css("width",w)
							.css("left",l)
						}
				)
				//jQuery('#'+humanMsg.msgID).animate({ opacity: 0 }, 500, function() { jQuery(this).hide() })
				/*������������������ ��������� ��� ������������� ���������*/
				this.lastMsgType=-1;
			}
		}
}