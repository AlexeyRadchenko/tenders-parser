/*
	HUMANIZED MESSAGES 1.0
	idea - http://www.humanized.com/weblog/2006/09/11/monolog_boxes_and_transparent_messages
	home - http://humanmsg.googlecode.com
*/
var humanMsg = {
		/*инициализация*/
		setup: function(appendTo, logName, msgOpacity) {
			/*идентификаторы элементов*/
			humanMsg.msgID = 'humanMsg';
			humanMsg.logID = 'humanMsgLog';
			/*счетчик сообщений*/
			humanMsg.count   = 0;
			/*последний отображаемый тип сообщений*/
			humanMsg.lastMsgType = -1;
			/*к чему добавлять лог сообщений*/
			if (appendTo == undefined)
				appendTo = 'body';
			/*текст загловка лога сообщений*/
			humanMsg.logName   = logName||'Message Log';
			/*прозрачность отображаемых сообщений*/
			humanMsg.msgOpacity = 1;
			if (msgOpacity != undefined) 
				humanMsg.msgOpacity = parseFloat(msgOpacity);
			/*добавляем лог сообщений*/
			jQuery(appendTo).append('<div id="'+humanMsg.msgID+'" class="humanMsg"></div><div id="'+humanMsg.logID+'"><p>'+logName+'</p><ul></ul></div>');
			/*назначаем событие открытия и закрытия лога*/
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
		/*отображение сообщения. Короткое сообщение, Полное сообщение, Приоритет*/
	,	displayMsg: function(shortMsg,msg,msgType) {
			/*если не проинициализировано, инитим*/
			if (!humanMsg.logID){
				humanMsg.setup('body', GLOBAL_MSG.get("message_log"));
			}
			/*при пустом сообщении выходим*/
			if (msg == '')
				return;
			/*наверно важная строка оО*/
			//clearTimeout(humanMsg.t2);
			/*обработчик добавления сообщения в журнал*/
			var handler=function() {
				jQuery('#'+humanMsg.logID)
					.show()												/*показываем журнал*/
					.children('ul')								/*находим дочерний список*/
					.prepend('<li>'+msg+'</li>')	/*добавляем а начало списка*/
					.children('li:first')					/*для добавленного элемента*/
					.slideDown(200)								/*делаем выезд*/
				/*увеличиваем счетчик сообщений*/
				humanMsg.count++;
				/*переинициализируем заголовок жрнала сообщений*/
				$('#'+humanMsg.logID+' p').text(humanMsg.logName+' ('+humanMsg.count+')');
			}
			/*признак необходимости назначения событий для скрития сообщения. не срабатывает, когда уже что то показывается*/
			var need_set=(jQuery('#'+humanMsg.msgID+':visible').size()==0);
			/*элемент для отображаемого сообщения*/
			var msg_obj=jQuery('#'+humanMsg.msgID);
			/*ели приоритет нового сообщения больше чем того, которое уже сейчас показывается, то покахываем приоритетное*/
			if (this.lastMsgType<msgType){
				/*запоминаем последний приоритет*/
				this.lastMsgType=msgType
				/*вставляем сообщение*/ 
				jQuery('#'+humanMsg.msgID).html(shortMsg)
				/*показываем сообщение*/
				msg_obj.show().animate({ opacity: humanMsg.msgOpacity}, 200, handler)
			}else{
				/*респауним сообщение*/
				msg_obj.show().animate({opacity: humanMsg.msgOpacity},200,handler)
			}
			/*если надо, то назначаем события*/
			if (need_set){
				/*следим за клавишами - при нажатии удаляем сообщение*/
				humanMsg.t1 = setTimeout("humanMsg.bindEvents()", 100);
				/*удаляем сообщение после 5 сек. */
				humanMsg.t2 = setTimeout("humanMsg.removeMsg()", 5000);
			}
		}
		/*назначение событий для скрытия сообщения*/
	,	bindEvents: function() {
			/*при клике и при нажатии клавиши дропаем сообщение*/
			jQuery(document)
				.bind('click', humanMsg.removeMsg)
				.bind('keypress', humanMsg.removeMsg)

				// .click(humanMsg.removeMsg)
				// .keypress(humanMsg.removeMsg)
		}
		/*удаляем сообщение*/
	,	removeMsg: function(){
			/*убираем слушателей*/
			clearTimeout(humanMsg.t2);
			jQuery(document)
				.unbind('click', humanMsg.removeMsg)
				.unbind('keypress', humanMsg.removeMsg)
			/*если месадж показывается, то скрываем его*/
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
				/*переинициализируем последний тип отображаемого сообщения*/
				this.lastMsgType=-1;
			}
		}
}