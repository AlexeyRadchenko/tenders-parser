// ������ ��� ������ � ������������� �����������
var GLOBAL_MSG={

    data: {
          "Yes": {"ru":"��",  "en":"Yes"},
          "No":  {"ru":"���", "en":"No"},
          
          // all_zero.js
          "htmldb_delete_message": {"ru":"������� ������?",  "en":"Delete record?"},
          "htmldb_delete_message2": {"ru":"������� ������?",  "en":"Delete records?"},
          "htmldb_only_one_message": {"ru":"������ ���� ������ <u>����</u> ������!",  "en":"<u>One</u> row must be selected!"},
          "htmldb_one_n_more_message": {"ru":"������ ���� ������ <u>���� �� ����</u> ������!",  "en":"<u>One or more</u> rows must be selected!"},
          "htmldb_one_or_nothing_message": {"ru":"����������� ������� �� ����� ������ �������",  "en":"You can select only one object"},
          
          "server_bad_answer": {"ru":"�������� ����� �� �������",  "en":"Invalid response from server."},
          "server_reports": {"ru":"������ ��������",  "en":"Server reports"},
          "editing_text_field": {"ru":"�������������� ���������� ����",  "en":"Editing text field"},
          
          // message.js
          "confirmation": {"ru":"�������������", "en":"Confirmation"},
          "cancel": {"ru":"������", "en":"Cancel"},
          "search_criteria": {"ru":"�������� �������� ������", "en":"Select search criteria"},
          "confirm_oper": {"ru":"����������� ���������� ��������",  "en":"Confirm the operation"},
          "warning": {"ru":"��������������",  "en":"Warning"},
          "message": {"ru":"���������",  "en":"Message"},
          "error": {"ru":"������",  "en":"Error"},
          "wait": {"ru":"���������",  "en":"Please wait"},
          "choose_file": {"ru":"������� ����� ����",  "en":"Choose a new file"},
          "select_file": {"ru":"����� �����",  "en":"Select file"},
          "load_file": {"ru":"��������� ����", "en":"Load file"},
          "to_cancel": {"ru":"��������", "en":"Cancel"},
          "delete_current": {"ru":"������� ������������", "en":"Delete current file"},

          // auction.js
          "auction_confirm": {"ru":"����������� ���� ����������� ����:", "en":"Confirm your price offer:"},
          "to_confirm": {"ru":"�����������", "en":"Confirm"},
          "spec_offer_warning":  
           {"ru": "����� ������ ������������ ����������� �� <br>"+
                  "������ �� ������� ������ ����������� ���� <br>"+
                  "� ������ ��������. <br><br>����������?", 
            "en": "You will not be able to continue bidding <br>"+ 
                  "in the auction after you have made <br>"+ 
                  "a special offer. Continue?"},
          "holland_confirm": {"ru":"����������� ���� �������� �� ���������� ��������� � �����:", "en":"Confirm that you accept the following contract price:"},
            
          // trdChOffer.js
          "report_and_prolongation": 
           {"ru": "����� ��������� ������ ��������� ����� ����������.<br>�������� �����?",  
            "en": "You will not be able to prolong the tender<br>after you have run the report.<br>Run the report?"}, 
          "select_partic_for_sap":  
           {"ru": "��� �������� ������ �� �������� � ��<br/>���������� ������� ����������", 
            "en": "You must select participants for sending data to SAP"},
          "sending_error":  
           {"ru": "������ �������� ������", 
            "en": "Sending data error"},                                     
          "send_to_sap_without_pos_1":  
           {"ru": "� ������������ �����������<br/>", 
            "en": "Offers of"},                                     
          "send_to_sap_without_pos_2":  
           {"ru": "��������� �� ��� �������. ��������� �� ������?", 
            "en": "have not all position. Send this data?"},

          // ecp.js
          "sign": 
           {"ru": "���������",  
            "en": "Sign"}, 
          "java_not_supported":  
           {"ru": "Java-������� �� ��������������.<br>���������� Java", 
            "en": "Java-applets are not supported.<br>Install Java"}, 
          "eds_name":  
           {"ru": "����������� �������� �������", 
            "en": "Electronic digital signature"}, 
			
          // Page 2111  
		  "comment":
			{"ru": "�����������:", 
            "en": "Comment:"},
		  "calendar":
			{"ru": "����� ���������", 
            "en": "Open calendar"},
		  "abandon":
			{"ru": "���������� �� �������?", 
            "en": "Abandon tender?"},
		  "reason":
			{"ru": "�������:", 
            "en": "Reason:"},
		  "confirm":
			{"ru": "�������������", 
            "en": "Confirmation"},
		  "cancel":
			{"ru": "������", 
            "en": "Cancel"},
			
          // Page 2112
          "clear_prepayment":  
           {"ru": '��� ������ � ������� "�����" ����� �������.<br><br>'+      
                  "����������?", 
            "en": 'All data of "Prepayment" column will be removed.<br><br>'+
                  'Continue?'},
          "position_offer":  
           {"ru": "����������� �� ������ ������� <br>������������� ������?",  
            "en": "Does the offer for this position comply with the order?"},
          "alt_offer":  
           {"ru": "������� �������������� �����������?",  
            "en": "Create alternative offer?"},
          "name":  
           {"ru": "������������",  
            "en": "Name"},
          "rename_offer":  
           {"ru": "������������� �����������?",  
            "en": "Rename offer?"},
          "delete_offer":  
           {"ru": "������� �����������?",  
            "en": "Delete offer?"},

          // ecp.js
          "message_log": 
           {"ru": "������ ���������",  
            "en": "Messages"},
            
          // ToolTip.js
          "show": 
           {"ru": "����������",  
            "en": "show"},
	    
	  // mail_room.js
	   "date_send": 
           {"ru": "����� �����������",  
            "en": "Date"},
	   "mail_sender": 
           {"ru": "�����������",  
            "en": "Sender"},           
	   "mail_recipient": 
           {"ru": "����������",  
            "en": "Recipient "},      
           "mail_subject": 
	   {"ru": "����",  
            "en": "Subject"},
           "mail_error": 
	   {"ru": "������",  
            "en": "Error"}		    
    }
  
    // �������� ��������
  , get: function(p_code)
    {
      return this.data[p_code][GLOBAL.LANG_CODE];
    }
}

