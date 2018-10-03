// Объект для работы с многоязычными сообщениями
var GLOBAL_MSG={

    data: {
          "Yes": {"ru":"Да",  "en":"Yes"},
          "No":  {"ru":"Нет", "en":"No"},
          
          // all_zero.js
          "htmldb_delete_message": {"ru":"Удалить запись?",  "en":"Delete record?"},
          "htmldb_delete_message2": {"ru":"Удалить записи?",  "en":"Delete records?"},
          "htmldb_only_one_message": {"ru":"Должен быть выбран <u>один</u> объект!",  "en":"<u>One</u> row must be selected!"},
          "htmldb_one_n_more_message": {"ru":"Должен быть выбран <u>хотя бы один</u> объект!",  "en":"<u>One or more</u> rows must be selected!"},
          "htmldb_one_or_nothing_message": {"ru":"Разрешается выбрать не более одного объекта",  "en":"You can select only one object"},
          
          "server_bad_answer": {"ru":"Неверный ответ от сервера",  "en":"Invalid response from server."},
          "server_reports": {"ru":"Сервер сообщает",  "en":"Server reports"},
          "editing_text_field": {"ru":"Редактирование текстового поля",  "en":"Editing text field"},
          
          // message.js
          "confirmation": {"ru":"Подтверждение", "en":"Confirmation"},
          "cancel": {"ru":"Отмена", "en":"Cancel"},
          "search_criteria": {"ru":"Выберите критерий поиска", "en":"Select search criteria"},
          "confirm_oper": {"ru":"Подтверждаю выполнение операции",  "en":"Confirm the operation"},
          "warning": {"ru":"Предупреждение",  "en":"Warning"},
          "message": {"ru":"Сообщение",  "en":"Message"},
          "error": {"ru":"Ошибка",  "en":"Error"},
          "wait": {"ru":"Подождите",  "en":"Please wait"},
          "choose_file": {"ru":"Укажите новый файл",  "en":"Choose a new file"},
          "select_file": {"ru":"Выбор файла",  "en":"Select file"},
          "load_file": {"ru":"Загрузить файл", "en":"Load file"},
          "to_cancel": {"ru":"Отменить", "en":"Cancel"},
          "delete_current": {"ru":"Удалить существующий", "en":"Delete current file"},

          // auction.js
          "auction_confirm": {"ru":"Подтвердите Ваше предложение цены:", "en":"Confirm your price offer:"},
          "to_confirm": {"ru":"Подтвердить", "en":"Confirm"},
          "spec_offer_warning":  
           {"ru": "После подачи специального предложения Вы <br>"+
                  "больше не сможете делать предложения цены <br>"+
                  "в данном аукционе. <br><br>Продолжить?", 
            "en": "You will not be able to continue bidding <br>"+ 
                  "in the auction after you have made <br>"+ 
                  "a special offer. Continue?"},
          "holland_confirm": {"ru":"Подтвердите Ваше согласие на заключение контракта с ценой:", "en":"Confirm that you accept the following contract price:"},
            
          // trdChOffer.js
          "report_and_prolongation": 
           {"ru": "После получения отчета продление будет невозможно.<br>Получить отчет?",  
            "en": "You will not be able to prolong the tender<br>after you have run the report.<br>Run the report?"}, 
          "select_partic_for_sap":  
           {"ru": "Для отправки данных по аукциону в ЭМ<br/>необходимо выбрать участников", 
            "en": "You must select participants for sending data to SAP"},
          "sending_error":  
           {"ru": "Ошибка отправки данных", 
            "en": "Sending data error"},                                     
          "send_to_sap_without_pos_1":  
           {"ru": "В предложениях поставщиков<br/>", 
            "en": "Offers of"},                                     
          "send_to_sap_without_pos_2":  
           {"ru": "заполнены не все позиции. Отправить их данные?", 
            "en": "have not all position. Send this data?"},

          // ecp.js
          "sign": 
           {"ru": "Подписать",  
            "en": "Sign"}, 
          "java_not_supported":  
           {"ru": "Java-апплеты не поддерживаются.<br>Установите Java", 
            "en": "Java-applets are not supported.<br>Install Java"}, 
          "eds_name":  
           {"ru": "Электронная цифровая подпись", 
            "en": "Electronic digital signature"}, 
			
          // Page 2111  
		  "comment":
			{"ru": "Комментарий:", 
            "en": "Comment:"},
		  "calendar":
			{"ru": "Вызов календаря", 
            "en": "Open calendar"},
		  "abandon":
			{"ru": "Отказаться от участия?", 
            "en": "Abandon tender?"},
		  "reason":
			{"ru": "Причина:", 
            "en": "Reason:"},
		  "confirm":
			{"ru": "Подтверждение", 
            "en": "Confirmation"},
		  "cancel":
			{"ru": "Отмена", 
            "en": "Cancel"},
			
          // Page 2112
          "clear_prepayment":  
           {"ru": 'Все данные в столбце "Аванс" будут очищены.<br><br>'+      
                  "Продолжить?", 
            "en": 'All data of "Prepayment" column will be removed.<br><br>'+
                  'Continue?'},
          "position_offer":  
           {"ru": "Предложение по данной позиции <br>соответствует заказу?",  
            "en": "Does the offer for this position comply with the order?"},
          "alt_offer":  
           {"ru": "Создать альтернативное предложение?",  
            "en": "Create alternative offer?"},
          "name":  
           {"ru": "Наименование",  
            "en": "Name"},
          "rename_offer":  
           {"ru": "Переименовать предложение?",  
            "en": "Rename offer?"},
          "delete_offer":  
           {"ru": "Удалить предложение?",  
            "en": "Delete offer?"},

          // ecp.js
          "message_log": 
           {"ru": "Журнал сообщений",  
            "en": "Messages"},
            
          // ToolTip.js
          "show": 
           {"ru": "показывать",  
            "en": "show"},
	    
	  // mail_room.js
	   "date_send": 
           {"ru": "Время отправления",  
            "en": "Date"},
	   "mail_sender": 
           {"ru": "Отправитель",  
            "en": "Sender"},           
	   "mail_recipient": 
           {"ru": "Получатель",  
            "en": "Recipient "},      
           "mail_subject": 
	   {"ru": "Тема",  
            "en": "Subject"},
           "mail_error": 
	   {"ru": "Ошибки",  
            "en": "Error"}		    
    }
  
    // Получить значение
  , get: function(p_code)
    {
      return this.data[p_code][GLOBAL.LANG_CODE];
    }
}

