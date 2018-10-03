// Ajax-ный Сабмит
function apxAjaxSubmit(pEvent) {
  $x('pRequest').value = pEvent+'_AJAX';
  var v_msg = '';

  $.ajax({
      type  : "POST"
    , url   : "wwv_flow.accept"
    , data  : $('form').serialize()
    , dataType : "json"
    , beforeSend:function(){
        v_msg = new Message(new MESSAGE_CONST.WAIT_TRANS());
      }
    , success : function(data){
        if (data.msgStatus!='success'){
          Notification.show(data);
        } else {
          doSubmit(pEvent);
        }
      }
    , complete : function(){
        v_msg.free();
      }
  });
}

// Показать форму с данными об организации
function trdShowContr(p_ref_id, p_object_id) {
  var v_url = "f?p="+$x('pFlowId').value+":2125:"+$x('pInstance').value+
               "::::P2125_REF_ID,P2125_OBJECT_ID:"+p_ref_id+","+p_object_id;
  var v_win = window.open(v_url, "ContrCard", 
                          "resizable=1,width=910px,height=630px");
  v_win.focus();
}

