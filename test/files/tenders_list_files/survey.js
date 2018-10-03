

// Сделать запить об отказе в участии в опросе
function RefuseSurvey(p_svy_id) {
  $.ajax({
     type  : "POST"
    ,url   : "wwv_flow.show"
    ,async : true
    ,data  : {
        x01            : p_svy_id
      , p_flow_id      : $x('pFlowId').value
      , p_flow_step_id : $x('pFlowStepId').value
      , p_instance     : $x('pInstance').value
      , p_request      : 'APPLICATION_PROCESS=SVY_REFUSE'
    }
  });
}


// Проверка наличия незавершенного опроса 
function CheckAvailableSurvey() {
  var pn = $v('pFlowStepId');
  if (pn == '1' || pn == '101' || pn == '2220' || pn == '2225') {
    return;
  }

  if ($v('pFlowStepId') == '1') {
    return;
  }
  $.ajax({
     type  : "POST"
    ,url   : "wwv_flow.show"
    ,async : true
    ,data  : {
        p_flow_id       : $x('pFlowId').value
      , p_flow_step_id  : $x('pFlowStepId').value
      , p_instance      : $x('pInstance').value
      , p_request       : 'APPLICATION_PROCESS=SVY_CHECK_AVAILABLE'
    }
    ,success : function(data) {
      if (data == null || data == '') {
        return;
      }
      var ss = data.split(':#:');
      if (ss.length < 7) {
        return;
      }
      var v_id      = ss[0]; // ID Опроса
      var v_coninue = ss[1]; // Флаг продолжения опроса
      var v_title   = ss[2]; // Наименование опроса
      var v_url     = ss[3]; // url для открытия окна с опросом
      var v_msg     = ss[4]; // Приглашение к участию
      var v_part_btn_title   = ss[5]; // Надпись кнопки "Открыть"
      var v_delay_btn_title  = ss[6]; // Надпись кнопки "Отложить"
      var v_refise_btn_title = ss[7]; // Надпись кнопки "Отказаться"
    
      new Message({
        title:   v_title,
        padding: "10",
        icon:    "question",
        content: v_msg,
        maxWidth: 500,
        contentStyle: {"white-space":"normal"},
        buttons: [
          {
            title: v_part_btn_title,
            handle: function(){
              OpenSurveyWindow(v_id, v_coninue);
            }
          },{
            title: v_delay_btn_title
          },{
            title: v_refise_btn_title,
            handle:function(){
              RefuseSurvey(v_id);
            }
          }
        ]
      });
    }

  });
}


// Открыть окно с опросом
// Если p_CONTINUE = 'Y', то будет отображен первый неотвеченный вопрос 
function OpenSurveyWindow(p_SVY_ID, p_CONTINUE, p_WIDTH, p_HEIGHT) {
  var w = p_WIDTH;
  if (w===null || w===undefined) w = 800;
  var h = p_HEIGHT;
  if (h===null || h===undefined) h = 600;

  var l = (screen.width - w) / 2;
  var t = (screen.height - h) / 2;
  
  window.open(
    'f?p='+$x('pFlowId').value+':2225:'+$x('pInstance').value+'::::P2225_SVY_ID,P2225_CONTINUE:'+p_SVY_ID+','+p_CONTINUE, 
    '', 
    'Toolbar=0, Location=0, Directories=0, Status=0, Menubar=0, Scrollbars=0, Resizable=1, Copyhistory=1, Width='+w+', Height='+h+', Left='+l+', Top='+t
  );

}


setTimeout("CheckAvailableSurvey()", 3000);

